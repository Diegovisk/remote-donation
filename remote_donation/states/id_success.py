from time import sleep
from turtle import distance

from remote_donation.models.enums.States import States
from remote_donation.utils.lcd import clear_det_lcd, print_det_lcd, print_info_lcd
from remote_donation.utils.leds import green_led_off, green_led_on


def id_success(state_machine):
    state_machine.log_print("ID_SUCCESS")

    #################
    # - Detecção
    print_det_lcd([
        "IDENTIFICADO!",
        "ITEM: "+state_machine.current_class._name_
    ])

    # LED Verde Ativo
    green_led_on()

    closed_bucket_levels = []

    # TODO: try to do the mean another way
    # while len(closed_bucket_levels) < 10:
    #     sensor_level = distance()
    #     closed_bucket_levels.append(sensor_level)
    #     sleep(.05)
    
    # state_machine.closed_bucket_level = sum(closed_bucket_levels) / len(closed_bucket_levels)
    i = 5
    while i >= 0:
        green_led_off()
        sleep(.5)
        green_led_on()
        sleep(.5)
        i -= 1

    green_led_off()
    # clear_det_lcd() # we dont turn it off for our next state

    state_machine.log_print("State changed:", States.ID_SUCCESS, "->", States.WAITING_DELIVERY)
    return States.WAITING_DELIVERY