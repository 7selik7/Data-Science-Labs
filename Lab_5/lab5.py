import cv2
import numpy as np
from matplotlib import pyplot as plt


def image_read(FileIm):
    image = cv2.imread(FileIm)
    plt.imshow(image)
    plt.show()
    return image


def image_processing(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (3, 3), 1)
    clahe = cv2.createCLAHE(clipLimit=2, tileGridSize=(8, 8))
    enhanced_image = clahe.apply(gray)

    edged = cv2.Canny(enhanced_image, 10, 250)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
    closed = cv2.morphologyEx(edged, cv2.MORPH_CLOSE, kernel)
    plt.imshow(closed)
    plt.show()
    return closed


def distance_between_points(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    distance = np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return distance


def image_contours(image_entrance, min_distance=150):
    cnts, _ = cv2.findContours(image_entrance.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    filtered_cnts = []
    filtered_centers = []

    for c in cnts:
        if cv2.contourArea(c) > 20:
            M = cv2.moments(c)
            ellipse = cv2.fitEllipse(c)
            center, axes, angle = ellipse
            major_axis, minor_axis = axes
            aspect_ratio = minor_axis / major_axis

            if M["m00"] != 0 and 0.9 <= aspect_ratio <= 1.1 and 10 <= len(c) < 800:
                center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                if not any(distance_between_points(center, fc) < min_distance for fc in filtered_centers):
                    filtered_centers.append(center)
                    filtered_cnts.append(c)

    return filtered_cnts


def image_recognition(image_entrance, image_cont, file_name):
    total = 0
    for c in image_cont:
        ellipse = cv2.fitEllipse(c)
        cv2.ellipse(image_entrance, ellipse, (0, 255, 0), 4)
        total += 1

    print("Знайдено {0} сегмент(а) круглих об'єктів".format(total))
    cv2.imwrite(file_name, image_entrance)
    plt.imshow(image_entrance)
    plt.show()
    return


if __name__ == '__main__':
    images_urls = ["img_1", "img_2", "img_3"]
    for url in images_urls:
        image_entrance = image_read(f"{url}.png")
        image_exit = image_processing(image_entrance)
        image_cont = image_contours(image_exit)
        image_recognition(image_entrance, image_cont, f"recognition_{url}.jpg")
