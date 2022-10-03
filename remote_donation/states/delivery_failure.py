from time import sleep

from remote_donation.models.enums.States import States
from remote_donation.utils.lcd import clear_info_lcd, info_backlight_off, info_backlight_on, print_info_lcd
from remote_donation.utils.leds import red_led_off, red_led_on


def delivery_failure(state_machine):
    state_machine.send_cap = True
    state_machine.log_print("DELIVERY_FAILURE")
    
    red_led_on()

    print_info_lcd([
        "ENTREGA N FEITA,",
        "TENTE NOVAMENTE!"
    ])

    # LED Vermelho ativo
    for _ in range(5):
        #################
        info_backlight_off()
        sleep(.5)
        info_backlight_on()
        sleep(.5)
    
    clear_info_lcd()
    red_led_off()


    state_machine.log_print("State changed:", States.DELIVERY_FAILURE, "->", States.WAITING_DONATION)
    return States.WAITING_DONATION