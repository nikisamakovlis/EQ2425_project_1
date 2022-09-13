import os
import numpy as np
import cv2
import matplotlib.pyplot as plt
import imutils


def read_images(folder):
    # this returns a list of grayscale images
    images = []
    for filename in os.listdir(folder):
        img = cv2.cvtColor(cv2.imread(os.path.join(folder, filename)), cv2.COLOR_BGR2GRAY)
        images.append(img)
    return images


def rotate_image(image):
    # returns a list of rotated images from 0 to 360 degrees.
    rotated_images = []
    (h, w) = image.shape[:2]
    (cX, cY) = (w//2, h//2)  # finding the center point
    d = 0  # degree
    for i in range(int(360/15)+1):
        rotation_matrix = cv2.getRotationMatrix2D((cX, cY), d, 1.0)
        abs_cos, abs_sin = abs(rotation_matrix[0,0]), abs(rotation_matrix[0,1])
        bound_w = int(h * abs_sin + w * abs_cos)
        bound_h = int(h * abs_cos + w * abs_sin)

        # subtract old image center (bringing image back to origo) and adding the new image center coordinates
        rotation_matrix[0, 2] += bound_w / 2 - cX
        rotation_matrix[1, 2] += bound_h / 2 - cY

        rotated_img = cv2.warpAffine(image, rotation_matrix, (bound_w, bound_h))  # apply rotation on image
        rotated_images.append(rotated_img)
        d += 15

    return rotated_images


def scale_image(image):
    scaled_images = []
    m = 1.2
    for i in range(0, 9):
        scaled_image = cv2.resize(image, None, fx=m**i, fy=m**i)
        print(scaled_image.shape)
        scaled_images.append(scaled_image)
    return scaled_images


def plot_images(columns, rows, imgs, tested_keypoint_detector, augmentation, figsize):
    fig = plt.figure(figsize=figsize)
    for i in range(1, columns * rows + 1):
        img = imgs[i]
        fig.add_subplot(rows, columns, i)
        plt.imshow(img)
    # plt.show()
    if tested_keypoint_detector == 'surf':
        if augmentation == 'rotated':
            save_path = 'Rotated_images_surf1.png'
        else:
            save_path = 'Scaled_images_surf1.png'
    else:
        if augmentation == 'rotated':
            save_path = 'Rotated_images_sift1.png'
        else:
            save_path = 'Scaled_images_sift1.png'

    plt.savefig(save_path, dpi=300)