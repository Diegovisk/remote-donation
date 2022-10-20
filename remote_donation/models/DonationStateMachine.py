from collections import deque
from datetime import datetime
from threading import Thread
import threading
from time import sleep
from remote_donation.models.enums.States import States
from remote_donation.states.waiting_donation import waiting_donation
from remote_donation.states.identifying import identifying
from remote_donation.states.id_success import id_success
from remote_donation.states.id_failure import id_failure
from remote_donation.states.waiting_delivery import waiting_delivery
from remote_donation.states.delivery_success import delivery_success
from remote_donation.states.delivery_failure import delivery_failure
import os
import requests

from paho.mqtt import client as mqtt_client

import torch
import torch.utils.checkpoint

from remote_donation.utils.distance import distance
from remote_donation.utils.donation_buffer import append_buffer, get_buffer, write_buffer
from remote_donation.utils.lcd import clear_det_lcd, clear_info_lcd
from remote_donation.utils.leds import blue_led_off, green_led_off, red_led_off, yellow_led_off
from remote_donation.utils.solenoid_relay import close_lock

dirname = os.path.dirname(__file__)



class DonationStateMachine:

    MODEL_PATH = os.path.join(dirname,"../artifacts/weights.old.pt")

    STATES = {
        States.WAITING_DONATION : waiting_donation,
        States.IDENTIFYING : identifying,
        States.ID_SUCCESS : id_success,
        States.ID_FAILURE : id_failure,
        States.WAITING_DELIVERY : waiting_delivery,
        States.DELIVERY_SUCCESS : delivery_success,
        States.DELIVERY_FAILURE : delivery_failure
    }

    SERVER = "192.168.0.101"
    URL = "http://"+SERVER+":5000"

    def __init__(self, ID, queue_size=10, image_size=(600, 600), detection_time_threshold=0.25, debug=True):
        self.__state = States.WAITING_DONATION
        self.ID = ID
        self.DEBUG = debug
        self.model = torch.hub.load('../yolov5', 'custom', path=self.MODEL_PATH, source='local')  # or yolov5n - yolov5x6, custom
        self.detection_queue = deque(maxlen=queue_size)
        self.image_size = image_size
        self.detection_time_threshold = detection_time_threshold
        # Filled to compare with...
        # self.closed_bucket_level = 0.0
        # ...this queue, to detect if the bucket is closed/open
        # self.opened_bucket_queue = 0.0

        self.current_class = None
        self.halt = False

        # Configurate the model (https://github.com/ultralytics/yolov5/issues/36)
        self.model.max_det = 1
        self.model.conf = 0.5
        self.model.iou = 0.5

        # Start MQTT
        self.client = mqtt_client.Client("CAIXA_" + str(self.ID))
        self.client.on_connect = self.__on_connect
        try:
            self.client.connect(self.SERVER, 1883)
        except: 
            print("Couldn't connect to BROKER, retrying on next log.")
        self.send_cap = True

        self.buffer_lock = threading.Lock()

        blue_led_off()
        green_led_off()
        yellow_led_off()
        red_led_off()

        clear_det_lcd()
        clear_info_lcd()

        close_lock()


        # TODO: CHANGE PRINTS TO LOGS AND MQTT MESSAGES
        self.log_print("STATE MACHINE STARTED!")

    def run(self):
        T = Thread(target=self.__capacity_daemon)
        T.setDaemon(True)
        T.start()
        
        T2 = Thread(target=self.__handle_offline)
        T2.setDaemon(True)
        T2.start()
        
        self.__loop()

    def log_print(self, *msgs):
        if self.DEBUG:
            msg = ""
            for m in msgs:
                msg += str(m) + " "
            msg = str(msg)
            msg = "[" + str(datetime.now()) + "] " + msg
            print(msg)
            try:
                self.client.publish("/caixas/" + str(self.ID) + "/debug", msg)
            except:
                print("Could not publish to MQTT broker. Check your connection and restart the State Machine.")
                try:
                    self.client.connect(self.SERVER, 1883)
                finally:
                    pass

    def __capacity_daemon(self):
        sleep_secs = 10
        while True:
            if not self.send_cap:
                sleep(sleep_secs)
                continue    
            current_cap = distance()
            
            try:
                self.client.publish("/caixas/" + str(self.ID) + "/capacidade", str(round(current_cap,2)) + "cm")
            except:
                print("Could not publish to MQTT broker. Check your connection and restart the State Machine.")
            try:
                    self.client.connect(self.SERVER, 1883)
                finally:
                    pass
            try:
                requests.post(url=self.URL + "/capacidade/" + str(self.ID), data={
                    "capacidade": current_cap
                })
            except:
                print("Something went wrong with your POST to the server.")

            sleep(sleep_secs)

    def __handle_offline(self):
        sleep_secs = 30
        while True:
            # Try to connect
            self.buffer_lock.acquire()
            # Try to push as many as you can
            buffer = get_buffer()
            while len(buffer) > 0:
                donation = buffer.pop()
                try:
                    requests.post(url=self.URL + "/doacao/" + str(self.ID), data={
                        "doacao":donation.name,
                        "timestamp":donation.time
                    })
                except:
                    buffer.append(donation)
                    break
            print("Remaining offline buffer:", buffer)
            # Write back the array (even if empty)
            write_buffer(buffer)
            self.buffer_lock.release()
            sleep(sleep_secs)


    def __on_connect(client, user, flags, rc):
        if rc == 0:
            print("connected to mqtt")
        else:
            print("error, %d", rc)

    def __get_state(self, state):
        return self.STATES[state](self)

    def __loop(self):
        while True:
            self.__state = self.__get_state(self.__state)