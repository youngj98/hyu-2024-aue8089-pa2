import numpy as np

from distort_points import distort_points


def project_points(points_3d: np.ndarray,
                   K: np.ndarray,
                   D: np.ndarray) -> np.ndarray:
    """
    Projects 3d points to the image plane, given the camera matrix,
    and distortion coefficients.

    Args:
        points_3d: 3d points (3xN)
        K: camera matrix (3x3)
        D: distortion coefficients (4x1)

    Returns:
        projected_points: 2d points (2xN)
    """

    # [TODO] get image coordinates
    
    points_3d = points_3d.T     # (N,3) -> (3,N)
    homogenous_points = np.dot(K, points_3d)    # (3,3)*(3,N) -> (3,N)
    image_points = homogenous_points[:2, :] / homogenous_points[2, :]   # z좌표로 정규화 (2,N)
    image_points = image_points.T   # (2,N) -> (N,2)

    # [TODO] apply distortion
    projected_points = distort_points(image_points, D, K)

    return projected_points
