import cv2

def format_image(im, image_size):
    im.flags.writeable = False
    im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)    

    # Crop and square image
    h, w, _ = im.shape
    if h > w:
        im = im[(h - w) // 2:(h - w) // 2 + w, :]
    else:
        im = im[:, (w - h) // 2:(w - h) // 2 + h]

    im = cv2.resize(im, image_size)
    return im
