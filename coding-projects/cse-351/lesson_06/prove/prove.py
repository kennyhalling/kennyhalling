"""
Course: CSE 351
Assignment: 06
Author: [Your Name]

Instructions:

- see instructions in the assignment description in Canvas

""" 

import multiprocessing as mp
import os
import cv2
import numpy as np

from cse351 import *

# Folders
INPUT_FOLDER = "faces"
STEP1_OUTPUT_FOLDER = "step1_smoothed"
STEP2_OUTPUT_FOLDER = "step2_grayscale"
STEP3_OUTPUT_FOLDER = "step3_edges"

# Parameters for image processing
GAUSSIAN_BLUR_KERNEL_SIZE = (5, 5)
CANNY_THRESHOLD1 = 75
CANNY_THRESHOLD2 = 155

# Allowed image extensions
ALLOWED_EXTENSIONS = ['.jpg']

# ---------------------------------------------------------------------------
def create_folder_if_not_exists(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"Created folder: {folder_path}")

# ---------------------------------------------------------------------------
def task_convert_to_grayscale(image):
    if len(image.shape) == 2 or (len(image.shape) == 3 and image.shape[2] == 1):
        return image # Already grayscale
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# ---------------------------------------------------------------------------
def task_smooth_image(image, kernel_size):
    return cv2.GaussianBlur(image, kernel_size, 0)

# ---------------------------------------------------------------------------
def task_detect_edges(image, threshold1, threshold2):
    if len(image.shape) == 3 and image.shape[2] == 3:
        print("Warning: Applying Canny to a 3-channel image. Converting to grayscale first for Canny.")
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    elif len(image.shape) == 3 and image.shape[2] != 1 : # Should not happen with typical images
        print(f"Warning: Input image for Canny has an unexpected number of channels: {image.shape[2]}")
        return image # Or raise error
    return cv2.Canny(image, threshold1, threshold2)

# ---------------------------------------------------------------------------
def worker(input_folder, output_folder, queue, processing_function,
                load_args = None, processing_args = None):
    while True:
        filename = queue.get()
        if filename is None:
            break
        file_ext = os.path.splitext(filename)[1].lower()
        if file_ext not in ALLOWED_EXTENSIONS:
            continue
        input_image_path = os.path.join(input_folder, filename)
        output_image_path = os.path.join(output_folder, filename)

        try:
            if load_args is not None:
                img = cv2.imread(input_image_path, load_args)
            else:
                img = cv2.imread(input_image_path)
            if img is None:
                print(f"Warning: Could not read image '{input_image_path}'. Skipping.")
                continue
            if processing_args:
                processed_img = processing_function(img, *processing_args)
            else:
                processed_img = processing_function(img)
            cv2.imwrite(output_image_path, processed_img)
        except Exception as e:
            print(f"Error processing file '{input_image_path}': {e}")

# ---------------------------------------------------------------------------
def run_image_processing_pipeline():
    print("Starting image processing pipeline...")

    # TODO
    # - create queues
    # - create barriers
    # - create the three processes groups
    # - you are free to change anything in the program as long as you
    #   do all requirements.
    create_folder_if_not_exists(STEP1_OUTPUT_FOLDER)
    WORKERS = 4
    q1 = mp.Queue()
    q2 = mp.Queue()
    q3 = mp.Queue()

    # --- Step 1: Smooth Images ---
    for filename in os.listdir(INPUT_FOLDER):
        q1.put(filename)
    for _ in range(WORKERS):
        q1.put(None)
    print(f"\nProcessing images from '{INPUT_FOLDER}' to '{STEP1_OUTPUT_FOLDER}'...")
    workers1 = []
    for _ in range(WORKERS):
        p = mp.Process(target=worker, args=(INPUT_FOLDER, STEP1_OUTPUT_FOLDER, q1, task_smooth_image, None, (GAUSSIAN_BLUR_KERNEL_SIZE,)))
        p.start()
        workers1.append(p)
    for p in workers1:
        p.join()
    
    # --- Step 2: Convert to Grayscale ---
    create_folder_if_not_exists(STEP2_OUTPUT_FOLDER)
    for filename in os.listdir(STEP1_OUTPUT_FOLDER):
        q2.put(filename)
    for _ in range(WORKERS):
        q2.put(None)
    print(f"\nProcessing images from '{STEP1_OUTPUT_FOLDER}' to '{STEP2_OUTPUT_FOLDER}'...")
    workers2 = []
    for _ in range(WORKERS):
        p = mp.Process(target=worker, args=(STEP1_OUTPUT_FOLDER, STEP2_OUTPUT_FOLDER, q2, task_convert_to_grayscale))
        p.start()
        workers2.append(p)
    for p in workers2:
        p.join()
    # --- Step 3: Detect Edges ---
    create_folder_if_not_exists(STEP3_OUTPUT_FOLDER)
    for filename in os.listdir(STEP2_OUTPUT_FOLDER):
        q3.put(filename)
    for _ in range(WORKERS):
        q3.put(None)
    print(f"\nProcessing images from '{STEP2_OUTPUT_FOLDER}' to '{STEP3_OUTPUT_FOLDER}'...")
    workers3 = []
    for _ in range(WORKERS):
        p = mp.Process(target=worker, args=(STEP2_OUTPUT_FOLDER, STEP3_OUTPUT_FOLDER, q3, task_detect_edges, cv2.IMREAD_GRAYSCALE, (CANNY_THRESHOLD1, CANNY_THRESHOLD2)))
        p.start()
        workers3.append(p)
    for p in workers3:
        p.join()
    step3_count = len([f for f in os.listdir(STEP3_OUTPUT_FOLDER) if f.lower().endswith('.jpg')])

    print("\nImage processing pipeline finished!")
    print(step3_count)
    print(f"Original images are in: '{INPUT_FOLDER}'")
    print(f"Grayscale images are in: '{STEP1_OUTPUT_FOLDER}'")
    print(f"Smoothed images are in: '{STEP2_OUTPUT_FOLDER}'")
    print(f"Edge images are in: '{STEP3_OUTPUT_FOLDER}'")


# ---------------------------------------------------------------------------
if __name__ == "__main__":
    log = Log(show_terminal=True)
    log.start_timer('Processing Images')

    # check for input folder
    if not os.path.isdir(INPUT_FOLDER):
        print(f"Error: The input folder '{INPUT_FOLDER}' was not found.")
        print(f"Create it and place your face images inside it.")
        print('Link to faces.zip:')
        print('   https://drive.google.com/file/d/1eebhLE51axpLZoU6s_Shtw1QNcXqtyHM/view?usp=sharing')
    else:
        run_image_processing_pipeline()

    log.write()
    log.stop_timer('Total Time To complete')
