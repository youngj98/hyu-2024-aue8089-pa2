import math
import numpy as np

from distort_points import distort_points


def undistort_image(img: np.ndarray,
                    K: np.ndarray,
                    D: np.ndarray,
                    bilinear_interpolation: bool = False) -> np.ndarray:
    """
    Corrects an image for lens distortion.

    Args:
        img: distorted image (HxW)
        K: camera matrix (3x3)
        D: distortion coefficients (4x1)
        bilinear_interpolation: whether to use bilinear interpolation or not
    """

    height, width, *_ = img.shape
    undistorted_img = np.zeros_like(img)

    for x in range(width):
        for y in range(height):

            # apply distortion
            x_d = distort_points(np.array([[x, y]]), D, K)
            u, v = x_d[0, :]

            # bilinear interpolation
            u1 = math.floor(u)
            v1 = math.floor(v)      # 왼쪽 위 (u1,v1), 오른쪽 위 (u1+1, v1), 왼쪽 아래 (u1, v1+1), 오른쪽 아래 (u1+1, v1+1)

            in_image = (u1 >= 0) & (u1+1 < width) & (v1 >= 0) & (v1+1 < height) # 점이 이미지 내에 있는지 확인
            if not in_image:
                continue

            if bilinear_interpolation:
                # [TODO] weighted sum of pixel values in img
                a = u - u1
                b = v - v1
                pixel_LU = img[v1, u1]
                pixel_RU = img[v1, u1 + 1]
                pixel_LD = img[v1 + 1, u1]
                pixel_RD = img[v1 + 1, u1 + 1]
                
                weight_LU = (1 - a) * (1 - b)
                weight_RU = a * (1 - b)
                weight_LD = (1 - a) * b
                weight_RD = a * b
                
                weighted_pixel = weight_LU * pixel_LU + weight_RU * pixel_RU + weight_LD * pixel_LD + weight_RD * pixel_RD
                
                undistorted_img[y, x] = weighted_pixel

            else:
                # [TODO] nearest neighbor
                a = u - u1
                b = v - v1
                if (a >= 0.5 and b >= 0.5):
                    pixel_near = img[v1 + 1, u1 + 1]
                elif (a >= 0.5 and b < 0.5):
                    pixel_near = img[v1, u1 + 1]
                elif (a < 0.5 and b >= 0.5):
                    pixel_near = img[v1 + 1, u1]
                else:
                    pixel_near = img[v1, u1]
                
                undistorted_img[y, x] = pixel_near


    return undistorted_img
