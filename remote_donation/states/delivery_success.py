from time import sleep

from remote_donation.models.enums.States import States


def delivery_success(state_machine):
    print("DELIVERY_SUCCESS")
    
    sleep(1)
    return States.DELIVERY_SUCCESS