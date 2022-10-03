from collections import deque
from time import sleep, time
from remote_donation.models.enums.States import States
from remote_donation.utils.distance import distance
from remote_donation.utils.lcd import clear_det_lcd, clear_info_lcd, print_info_lcd
from remote_donation.utils.leds import blue_led_off, blue_led_on
from remote_donation.utils.solenoid_relay import close_lock, open_lock
from statistics import stdev


def waiting_delivery(state_machine):
    state_machine.send_cap = False
    #################
    # - Info
    print_info_lcd([
        "Abra a tampa e",
        "coloque o item"
    ])

    # Destrava a tampa
    open_lock()

    # LED Azul
    blue_led_on()

    distance_queue = deque(maxlen=15)

    for _ in range(15):
        distance_queue.appendleft(distance())
        sleep(.1)
    
    current_time = time()
    max_wait = current_time + 10

    while current_time < max_wait:
        distance_queue.pop()
        distance_queue.appendleft(distance())
        box_distance_stdev = stdev(distance_queue)
        sleep(.1)
        if box_distance_stdev >= 10:
            blue_led_off()
            clear_info_lcd()
            # DET LCD was open from our last state
            clear_det_lcd()

            print("State changed:", States.WAITING_DELIVERY, "->", States.DELIVERY_SUCCESS)
            return States.DELIVERY_SUCCESS
        current_time = time()

    blue_led_off()
    clear_info_lcd()
    # DET LCD was open from our last state
    clear_det_lcd()

    close_lock()

    print("State changed:", States.WAITING_DELIVERY, "->", States.DELIVERY_FAILURE) 
    return States.DELIVERY_FAILURE