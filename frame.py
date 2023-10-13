import glob
import contextlib
from PIL import Image

import cv2
import time

def stich_frames(prusa_id):
    frames = f'frames/prusa_{prusa_id}/*.png'
    file_out = f'frames/prusa_{prusa_id}/feed.gif'

    # Use exit stack to automatically close opened images
    with contextlib.ExitStack() as stack:

        # Lazily load images
        imgs = (stack.enter_context(Image.open(f)) for f in sorted(glob.glob(frames)))

        # Extract  first image from iterator
        img = next(imgs)

        img.save(fp=file_out, format='GIF', append_images=imgs, save_all=True, duration=200, loop=0)


def get_frames(prusa_id, num_frames=30):
    capture = cv2.VideoCapture(0)
    
    for i in range(num_frames):
        _, frame = capture.read()
        file_name = f'frames/prusa_{prusa_id}/frame_{i}.png'
        cv2.imwrite(file_name, frame)

        time.sleep(0.333)

    capture.release()

    # Convert to .gif
    stich_frames(prusa_id)