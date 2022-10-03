from time import sleep
from remote_donation.models.enums.States import States
from remote_donation.utils.lcd import clear_det_lcd, clear_info_lcd, print_det_lcd, print_info_lcd
from remote_donation.utils.leds import red_led_off, red_led_on


def id_failure(state_machine):
    print("ID_FAILURE")
    
    red_led_on()

    print_det_lcd([
        "FALHA NA",
        "IDENTIFICACAO.."
    ])

    print_info_lcd([
        "AGUARDE E TENTE",
        "NOVAMENTE!"
    ])
    
    sleep(5)

    clear_det_lcd()
    clear_info_lcd()
    red_led_off()

    print("State changed:", States.ID_FAILURE, "->", States.WAITING_DONATION)
    return States.WAITING_DONATION