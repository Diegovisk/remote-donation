from collections import deque
from remote_donation.models.enums.States import States
from remote_donation.states.waiting_donation import waiting_donation
from remote_donation.states.identifying import identifying
from remote_donation.states.id_success import id_success
from remote_donation.states.id_failure import id_failure
from remote_donation.states.waiting_delivery import waiting_delivery
from remote_donation.states.delivery_success import delivery_success
from remote_donation.states.delivery_failure import delivery_failure

import torch
import torch.utils.checkpoint

class DonationStateMachine:

    MODEL_PATH = "../artifacts/weights.pt"

    STATES = {
        States.WAITING_DONATION : waiting_donation,
        States.IDENTIFYING : identifying,
        States.ID_SUCCESS : id_success,
        States.ID_FAILURE : id_failure,
        States.WAITING_DELIVERY : waiting_delivery,
        States.DELIVERY_SUCCESS : delivery_success,
        States.DELIVERY_FAILURE : delivery_failure
    }

    def __init__(self, queue_size=14, image_size=(600, 600), detection_time_threshold=0.5):
        self.__state = States.WAITING_DONATION
        self.model = torch.hub.load('ultralytics/yolov5', 'custom', path=self.MODEL_PATH, source='local')  # or yolov5n - yolov5x6, custom
        self.detection_queue = deque(maxlen=queue_size)
        self.image_size = image_size
        self.detection_time_threshold = detection_time_threshold
        # Filled to compare with...
        self.closed_bucket_level = 0.0
        # ...this queue, to detect if the bucket is closed/open
        self.opened_bucket_queue = 0.0

        self.current_class = None

        # Configurate the model (https://github.com/ultralytics/yolov5/issues/36)
        self.model.max_det = 1
        self.model.conf = 0.5
        self.model.iou = 0.5

        # TODO: CHANGE PRINTS TO LOGS AND MQTT MESSAGES
        print("STATE MACHINE STARTED!")


    def __get_state(self, state):
        return self.STATES[state](self)

    def run(self):
        while True:
            self.__state = self.__get_state(self.__state)
