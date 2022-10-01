from remote_donation.models.enums.States import States


def id_failure(state_machine):
    print("ID_FAILURE")

    return States.WAITING_DONATION