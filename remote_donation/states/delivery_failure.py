from time import sleep

from remote_donation.models.enums.States import States


def delivery_failure(state_machine):
    print("DELIVERY_FAILURE")
    
    #################
    # - Detecção clear

    # LED Vermelho ativo

    for i in range(3):
        #################
        # - Info
        # FALHA DURANTE
        # A ENTREGA!
        sleep(1)
        #################
        # - Info
        # TENTE NOVAMENTE
        # EM BREVE
        sleep(1)

    return States.WAITING_DONATION