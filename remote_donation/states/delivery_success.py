from time import sleep

from remote_donation.models.enums.States import States
from remote_donation.utils.lcd import clear_info_lcd, print_info_lcd
from remote_donation.utils.leds import green_led_off, green_led_on
import requests

def delivery_success(state_machine):
    state_machine.send_cap = True
    print("DELIVERY_SUCCESS")

    green_led_on()

    print_info_lcd([
        "MUITO OBRIGADO!",
        "DOAÇÃO FEITA."
    ])

    sleep(4)

    green_led_off()
    clear_info_lcd()

    requests.post(url=state_machine.URL + "/doacao/" + str(state_machine.ID), data={
        "doacao":state_machine.current_class._name_
    })
    
    sleep(1)

    print("State changed:", States.DELIVERY_SUCCESS, "->", States.WAITING_DONATION)
    return States.WAITING_DONATION