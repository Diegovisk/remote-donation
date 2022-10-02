from time import sleep

from remote_donation.models.enums.States import States


def id_success(state_machine):
    print("ID_SUCCESS")

    #################
    # - Detecção
    # IDENTIFICADO!
    # (ITEM: CLASSE)[:16]

    #################
    # - Info
    # Abra a tampa e 
    # coloque o item

    # LED Verde Ativo

    closed_bucket_levels = []

    while len(closed_bucket_levels) < 10:
        # sensor_level = get_sensor_level()
        # closed_bucket_levels.append(sensor_level)
        sleep(.05)
    
    state_machine.closed_bucket_level = sum(closed_bucket_levels) / len(closed_bucket_levels)

    return States.WAITING_DELIVERY