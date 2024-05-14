import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt


def get_size(image: np.ndarray, thresh=255):
    lw = 0
    rw = image.shape[1]

    th = 0
    bh = image.shape[0]

    while all([pixel[0] >= thresh for pixel in image[th:][0]]):
        th += 1

    while all([pixel[0] >= thresh for pixel in image[bh - 1:][0]]):
        bh -= 1

    while all([image[pixel, lw][0] >= thresh for pixel in range(image.shape[0])]):
        lw += 1

    while all([image[pixel, rw - 1][0] >= thresh for pixel in range(image.shape[0])]):
        rw -= 1

    return (lw, rw, th, bh)


image = cv.imread('mail_images/12447682014154883968.png')
im_gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

lw, rw, th, bh = get_size(image, 255)

img = image[th:bh, lw:rw]

ret, th1 = cv.threshold(img, 127, 255, cv.THRESH_BINARY)
th2 = cv.adaptiveThreshold(img, 255, cv.ADAPTIVE_THRESH_MEAN_C, \
                           cv.THRESH_BINARY, 11, 2)
th3 = cv.adaptiveThreshold(img, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, \
                           cv.THRESH_BINARY, 11, 2)
titles = ['Original Image', 'Global Thresholding (v = 127)',
          'Adaptive Mean Thresholding', 'Adaptive Gaussian Thresholding']
images = [img, th1, th2, th3]
for i in range(4):
    plt.subplot(2, 2, i + 1), plt.imshow(images[i], 'gray')
    plt.title(titles[i])
    plt.xticks([]), plt.yticks([])
plt.show()
# w = rw - lw
# h = bh - th
#
# parts = 2
#
# for i in range(parts):
#     crop_img = image[th:bh, lw + i * (w // parts):lw + (i + 1) * (w // parts)]
#     cv.imshow(f'char{i}', crop_img)

# cv.waitKey(0)
# cv.destroyAllWindows()

# cv.imshow('Image', image)
# cv.imshow('trash', im_thresh_gray)
# cv.imshow('with_line', with_line)
#
# # Wait for a key press and close the window
# cv.waitKey(0)
# cv.destroyAllWindows()
