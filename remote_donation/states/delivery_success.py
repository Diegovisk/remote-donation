from time import sleep

from remote_donation.models.enums.States import States
from remote_donation.utils.donation_buffer import OfflineDonation, append_buffer
from remote_donation.utils.lcd import clear_info_lcd, print_info_lcd
from remote_donation.utils.leds import green_led_off, green_led_on
import requests
from time import time

def delivery_success(state_machine):
    state_machine.send_cap = True
    state_machine.log_print("DELIVERY_SUCCESS")

    green_led_on()

    print_info_lcd([
        "MUITO OBRIGADO!",
        "DOAÇÃO FEITA."
    ])

    sleep(4)

    green_led_off()
    clear_info_lcd()

    try:
        requests.post(url=state_machine.URL + "/doacao/" + str(state_machine.ID), data={
            "doacao":state_machine.current_class._name_
        })
    except:
        # If failed:
        state_machine.buffer_lock.acquire()
        append_buffer(OfflineDonation(state_machine.current_class._name_, int(time())))
        state_machine.buffer_lock.release()


    sleep(1)

    state_machine.log_print("State changed:", States.DELIVERY_SUCCESS, "->", States.WAITING_DONATION)
    return States.WAITING_DONATION