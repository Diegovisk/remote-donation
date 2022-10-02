import cv2
from time import sleep, time
from remote_donation.models.enums.Classes import Classes
from remote_donation.models.enums.States import States
from remote_donation.states.shared_utils.format_image import format_image


def _get_class_frequency(cls, detected_q):
    freq = 0
    for c in detected_q:
        if cls == c:
            freq += 1
    return freq

def identifying(state_machine):
    # LED amarelo ativo

    # - Detecção
    # IDENTIFICANDO

    # - Info
    # Não mova o item

    # For webcam input:
    cap = cv2.VideoCapture(0)

    last_capture = time()

    while cap.isOpened():
        if time() - last_capture < state_machine.detection_time_threshold:
            sleep(.1)
            continue
        
        success, im = cap.read()
        if not success:
            continue

        im = format_image(im, state_machine.image_size)

        results = state_machine.model(im)

        results.print()

        last_capture = time()

    	# Check if there is a detection
        if(len(results.tolist()[0].pred[0]) > 0):
            detected = int(results.tolist()[0].pred[0][0][5])

            # Empty the queue
            while len(state_machine.detection_queue) > state_machine.detection_queue.maxlen:
                state_machine.detection_queue.pop()

            state_machine.detection_queue.appendleft(Classes(detected))
        else:
            state_machine.detection_queue.appendleft(Classes.NONE)

        # PRINT THE QUEUE
        print(state_machine.detection_queue)

        chosen_freq = _get_class_frequency(state_machine.current_class, state_machine.detection_queue)
        
        # If 60% of the last MAXLEN detections are the same class
        if chosen_freq < int(state_machine.detection_queue.maxlen * 0.2):
            state_machine.current_class = None
            print("State changed:", States.IDENTIFYING, "->", States.ID_FAILURE)
            cap.release()
            return States.ID_FAILURE
        elif chosen_freq >= int(state_machine.detection_queue.maxlen * 0.8):
            print("State changed:", States.IDENTIFYING, "->", States.ID_SUCCESS)
            cap.release()
            return States.ID_SUCCESS 

    cap.release()

    # Default state
    return States.IDENTIFYING