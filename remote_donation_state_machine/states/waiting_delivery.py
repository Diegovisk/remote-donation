from time import time
from remote_donation.models.enums.States import States


def waiting_delivery(state_machine):
    current_time = time()
    max_wait = current_time + 10
    
    # Destrava a tampa

    # LED Azul

    #################

    return States.WAITING_DELIVERY