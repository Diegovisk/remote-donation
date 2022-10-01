import cv2
from time import sleep, time

from remote_donation.models.enums.Classes import Classes
from remote_donation.models.enums.States import States
from remote_donation.states.shared_utils.format_image import format_image

def _get_max_frequency(detected, percentage=1):
    freq = 0
    class_ = None
    max_n = int(len(detected) * percentage)
    i = 0
    for c, f in detected.items():
        if i > max_n:
            break
        i += 1
        if f > freq:
            freq = f
            class_ = c
    return freq, class_

def waiting_donation(state_machine):    
    state_machine.detection_queue.clear()

    # - Detecção
    # AGUARDANDO
    # ITEM NA CAMERA


    # - Info
    # Mostre o Item
    # Para a Câmera

    # Piscar o LED azul
    # criar thread com variavel que checa aqui bacaninha.
 
    # For webcam input:
    cap = cv2.VideoCapture(0)

    last_capture = time()

    while cap.isOpened():
        if time() - last_capture < state_machine.detection_time_threshold:
            sleep(.1)
            continue
        
        detected_freq = {}

        for enum_key in Classes:
            detected_freq[enum_key] = 0

        success, im = cap.read()
        if not success:
            continue

        im = format_image(im, state_machine.image_size)

        results = state_machine.model(im)

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
        
        # frequency of detection for each class
        for det in state_machine.detection_queue:
            detected_freq[Classes(det)] += 1

        # We aim to detect 1/2 of the queue and see if in it we have enough detections
        freq, cls = _get_max_frequency(detected_freq, 0.6)

        # If 60% of the last MAXLEN detections are the same class
        if freq > int(state_machine.detection_queue.maxlen * 0.4) and cls != Classes.NONE:
            # state_machine.state = States.IDENTIFYING
            state_machine.current_class = cls
            print("State changed:", States.WAITING_DONATION, "->", States.IDENTIFYING)
            cap.release()
            while len(state_machine.detection_queue) > freq:
                state_machine.detection_queue.pop()
            return States.IDENTIFYING

    cap.release()
    # cv2.destroyAllWindows()

    # Default state
    return States.WAITING_DONATION
    