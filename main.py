from remote_donation.models.DonationStateMachine import DonationStateMachine

donation_state_machine = DonationStateMachine(4)

donation_state_machine.run()