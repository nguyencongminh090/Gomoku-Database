import ctypes
import cv2
import mss
import numpy as np


def find_chessboard_from_image(img):
    value = 20
    image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    found_board = False

    kernel_h = np.array([[-1, 1]])
    kernel_v = np.array([[-1], [1]])
    line_horizontales = np.absolute(cv2.filter2D(image.astype('float'), -1, kernel_v))

    ret, thresh1 = cv2.threshold(line_horizontales, 30, 255, cv2.THRESH_BINARY)
    cv2.imwrite('Process_input.jpg', thresh1)

    kernel_small = np.ones((1, 5), np.uint8)
    kernel_big = np.ones((1, 60), np.uint8)

    # Remove holes:
    img_h1 = cv2.dilate(thresh1, kernel_small, iterations=1)
    img_h2 = cv2.erode(img_h1, kernel_small, iterations=1)

    img_h3 = cv2.erode(img_h2, kernel_big, iterations=1)
    img_h4 = cv2.dilate(img_h3, kernel_big, iterations=1)

    lines_starts = cv2.filter2D(img_h4, -1, kernel_h)
    lines_ends = cv2.filter2D(img_h4, -1, -kernel_h)
    lines = lines_starts.sum(axis=0) / 255
    line_start = 0
    nb_line_start = 0
    line_val = 0
    for idx, val in enumerate(lines):
        if val > value:
            nb_line_start += 1
            line_start = idx
            line_val = val
            break
    lines = lines_ends.sum(axis=0) / 255
    line_end = 0
    nb_line_end = 0
    for idx, val in enumerate(lines):
        if val > value:
            nb_line_end += 1
            line_end = idx
    line_vertical = np.absolute(cv2.filter2D(image.astype('float'), -1, kernel_h))
    ret, thresh1 = cv2.threshold(line_vertical, 30, 255, cv2.THRESH_BINARY)

    kernel_small = np.ones((5, 1), np.uint8)
    kernel_big = np.ones((60, 1), np.uint8)

    img_v1 = cv2.dilate(thresh1, kernel_small, iterations=1)
    img_v2 = cv2.erode(img_v1, kernel_small, iterations=1)

    img_v3 = cv2.erode(img_v2, kernel_big, iterations=1)
    img_v4 = cv2.dilate(img_v3, kernel_big, iterations=1)

    column_starts = cv2.filter2D(img_v4, -1, kernel_v)
    column_ends = cv2.filter2D(img_v4, -1, -kernel_v)

    column = column_starts.sum(axis=1) / 255
    column_start = 0
    nb_column_start = 0
    column_val = 0
    for idx, val in enumerate(column):
        if val > value:
            column_start = idx
            nb_column_start += 1
            column_val = val
            break
    column = column_ends.sum(axis=1) / 255
    column_end = 0
    nb_column_end = 0
    for idx, val in enumerate(column):
        if val > value:
            column_end = idx
            nb_column_end += 1

    if (nb_line_start == 1) and (nb_line_end == 1) and (nb_column_start == 1) and (nb_column_end == 1):
        if abs((column_end - column_start) - (line_end - line_start)) <= 3:
            found_board = True

    if found_board:
        line_start -= int(line_val / 14)
        column_start -= int(column_val / 14)
        cv2.imwrite('.\\Output.jpg', image[column_start:column_end, line_start:line_end])
        f = open('.\\config.txt', 'w')
        f.write('{}\n{} {} {} {}'.format((line_end - line_start + column_end - column_start) / 28, line_start,
                                         column_start, line_end - line_start,
                                         column_end - column_start))
        f.close()
        return True
    return False


# noinspection PyTypeChecker
def recognize():
    user32 = ctypes.windll.user32
    screensize = user32.GetSystemMetrics(1), user32.GetSystemMetrics(0)
    while True:
        sct = mss.mss()
        monitor = {'top': 0, 'left': 0, 'width': screensize[1], 'height': screensize[0]}
        img = np.array(np.array(sct.grab(monitor)))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        k = find_chessboard_from_image(img)
        if k:
            break
