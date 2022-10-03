from collections import deque
from threading import Thread
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

from paho.mqtt import client as mqtt_client

import torch
import torch.utils.checkpoint

from remote_donation.utils.distance import distance

dirname = os.path.dirname(__file__)



class DonationStateMachine:

    MODEL_PATH = os.path.join(dirname,"../artifacts/weights.pt")

    STATES = {
        States.WAITING_DONATION : waiting_donation,
        States.IDENTIFYING : identifying,
        States.ID_SUCCESS : id_success,
        States.ID_FAILURE : id_failure,
        States.WAITING_DELIVERY : waiting_delivery,
        States.DELIVERY_SUCCESS : delivery_success,
        States.DELIVERY_FAILURE : delivery_failure
    }

    SERVER = "192.168.15.11"
    URL = "http://"+SERVER+":5000"

    def __init__(self, ID, queue_size=14, image_size=(600, 600), detection_time_threshold=0.5):
        self.__state = States.WAITING_DONATION
        self.ID = ID
        self.model = torch.hub.load('ultralytics/yolov5', 'custom', path=self.MODEL_PATH)  # or yolov5n - yolov5x6, custom
        self.detection_queue = deque(maxlen=queue_size)
        self.image_size = image_size
        self.detection_time_threshold = detection_time_threshold
        # Filled to compare with...
        # self.closed_bucket_level = 0.0
        # ...this queue, to detect if the bucket is closed/open
        # self.opened_bucket_queue = 0.0

        self.current_class = None

        # Configurate the model (https://github.com/ultralytics/yolov5/issues/36)
        self.model.max_det = 1
        self.model.conf = 0.5
        self.model.iou = 0.5

        # TODO: CHANGE PRINTS TO LOGS AND MQTT MESSAGES
        print("STATE MACHINE STARTED!")

        # Start MQTT
        self.client = mqtt_client.Client("CAIXA_" + str(self.ID))
        self.client.on_connect = self.__on_connect
        self.client.connect(self.SERVER, 1883)
        self.send_cap = True

        T = Thread(target=self.__capacity_daemon)
        T.setDaemon(True)
        T.start()

    def __capacity_daemon(self):
        sleep_secs = 10
        while True:
            if not self.send_cap:
                sleep(sleep_secs)
                continue    
            current_cap = distance()
            self.client.publish("/caixas/" + str(self.ID) + "/capacidade", str(round(current_cap,2)) + "cm")
            sleep(sleep_secs)


    def __on_connect(client, user, flags, rc):
        if rc == 0:
            print("connected to mqtt")
        else:
            print("error, %d", rc)

    def __get_state(self, state):
        return self.STATES[state](self)

    def run(self):
        while True:
            self.__state = self.__get_state(self.__state)
