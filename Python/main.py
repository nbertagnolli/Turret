__author__ = 'tetracycline'

# Imports
import cv2
import numpy as np
from imutils.object_detection import non_max_suppression
import imutils
import pygame
import serial
from time import sleep

# =============================================================================
# DECLARE GLOBAL CONSTANTS
# =============================================================================
MIN_AREA = 700  # Minimum contour area, determines object size
IM_MIN = 0      # Calibrated minimum of the image where the turret can fire

# =============================================================================
#  Initializations
# =============================================================================

# Working Angle of Servos
pan = 0
tilt = 0
fire = 0

# Create Video Capture
cap = cv2.VideoCapture(1)

# Initialize the Foreground Background Detector
fgbg_detector = cv2.BackgroundSubtractorMOG()
fgbg_mask = None
display_rectangles = False

# Initialize Serial Port
ser = serial.Serial('/dev/tty.usbmodem1411')

# initialize mixer for audio
pygame.mixer.init(44100, -16, 2, 2048)

# =============================================================================
#  Helper Methods
# =============================================================================


def calculate_angle(frame_dim, center):
    return (180. / (frame_dim - IM_MIN)) * (center - IM_MIN)


def send_signal(pan_angle, tilt_angle, fire_flag):
    signal = 'f' + format_angle(pan_angle) + format_angle(tilt_angle) + format_angle(fire_flag)
    print signal
    ser.write(signal)
    sleep(.1)


def format_angle(angle):
    if angle < 10:
        return '00' + str(angle)
    elif angle < 100:
        return '0' + str(angle)
    else:
        return str(angle)

if __name__ == "__main__":

    # Continuous video displaying
    while True:

        # Capture frames
        ret, frame = cap.read()

        # Resize image for quicker processing
        frame = imutils.resize(frame, width=min(500, frame.shape[1]))

        # Convert to grayscale because color does not affect background
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Smooth image to reduce the affect of high frequency noise
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        threshold = fgbg_detector.apply(gray)

        # Dilate the image to fill in bright holes and create complete background objects
        threshold = cv2.dilate(threshold, None, iterations=2)
        (cnts, _) = cv2.findContours(threshold.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # TODO:: Apply Non Maximum supression?

        max_contour = MIN_AREA

        # Loop over the change contours
        for c in cnts:
            # If the contour is small discount it
            c_area = cv2.contourArea(c)
            if c_area < MIN_AREA:
                continue

            # Find largest contour
            if c_area > max_contour:
                max_contour = c_area

                # Find the contour bounding boxes
                (x, y, w, h) = cv2.boundingRect(c)
                (center, radius) = cv2.minEnclosingCircle(c)
                display_rectangles = True

        # Display the bounding box of the largest contour
        if display_rectangles:
            #pygame.mixer.Sound('i see you.wav').play()
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            # cv2.circle(frame, (int(center[0]), int(center[1])), int(radius), (0, 255, 0), 2)

            # Calculate the center point and adjust the position of the turret
            pan = int(calculate_angle(frame.shape[1], center[0]))
            print pan
            # Communicate with Arduino
            send_signal(pan, tilt, fire)
            sleep(.1)


        # Display the resulting Frame
        cv2.imshow('frame', frame)
        cv2.imshow('threshold', threshold)

        display_rectangles = False

        # Quite Loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Clean up space
    cap.release()
    cv2.destroyAllWindows()


