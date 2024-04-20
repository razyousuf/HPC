# 1. Imporping the required libraries
import numpy as np
cimport numpy as np
cimport cython
from libc.math cimport sqrt

# 2. Define a typed memory view for 2D double arrays
ctypedef double[:, :] double2D

##==============================================================================
# 3. Define Sobel filter function in Cython
cdef double2D sobel_filter_cy(double2D image):
    cdef:
        int rows = image.shape[0]  # Number of rows in the image
        int cols = image.shape[1]  # Number of columns in the image
        double2D edge_map = np.zeros((rows, cols), dtype=np.float64)  # Initialize an array to store edge map
        int i, j, dx, dy  # Loop variables
        double sx, sy  # Variables to store horizontal and vertical gradients
        # Define Gx and Gy arrays as 3x3 matrices
        double Gx[3][3]
        double Gy[3][3]

    # Initialize Sobel filter kernels Gx and Gy
    Gx[0][0] = -1; Gx[0][1] = 0; Gx[0][2] = 1
    Gx[1][0] = -2; Gx[1][1] = 0; Gx[1][2] = 2
    Gx[2][0] = -1; Gx[2][1] = 0; Gx[2][2] = 1

    Gy[0][0] = -1; Gy[0][1] = -2; Gy[0][2] = -1
    Gy[1][0] =  0; Gy[1][1] =  0; Gy[1][2] =  0
    Gy[2][0] =  1; Gy[2][1] =  2; Gy[2][2] =  1

    # Apply Sobel filter to compute edge map
    for i in range(1, rows - 1):
        for j in range(1, cols - 1):
            sx = 0
            sy = 0
            # Convolve image with Sobel filter kernels
            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    sx += Gx[dx + 1][dy + 1] * image[i + dx, j + dy]
                    sy += Gy[dx + 1][dy + 1] * image[i + dx, j + dy]
            # Compute gradient magnitude using Euclidean distance formula
            edge_map[i, j] = sqrt(sx**2 + sy**2)

    return edge_map

##==============================================================================
# 4. Define thresholding function in Cython
# Cython decorator for array access optimizations
@cython.boundscheck(False)  # Disable bounds checking for array access
@cython.wraparound(False)   # Disable negative index wrapping for array access
cpdef np.ndarray apply_threshold_cy(double2D edge_map, int threshold=150):
    cdef:
        int rows = edge_map.shape[0]  # Number of rows in the edge map
        int cols = edge_map.shape[1]  # Number of columns in the edge map
        cdef unsigned char[:, :] thresholded = np.zeros((rows, cols), dtype=np.uint8)  # Initialize thresholded image
        int i, j  # Loop variables

    # Apply thresholding to the edge map
    for i in range(rows):
        for j in range(cols):
            # Set pixel to 255 (white) if gradient magnitude is above threshold, else 0 (black)
            thresholded[i, j] = 255 if edge_map[i, j] > threshold else 0

    return np.asarray(thresholded)  # Convert thresholded image to NumPy array

##==============================================================================
# 5. Define Sobel edge detection function in Cython
# Cython decorator for array access optimizations
@cython.boundscheck(False)  # Disable bounds checking for array access
@cython.wraparound(False)   # Disable negative index wrapping for array access
cpdef np.ndarray sobel_edge_detection_cy(np.ndarray image):
    cdef double2D img_view = image  # Create a typed memory view for the input image
    cdef double2D edges = sobel_filter_cy(img_view)  # Apply Sobel filter to the input image
    cdef np.ndarray thresholded_edges = apply_threshold_cy(edges)  # Apply thresholding to the resulting edge map
    return thresholded_edges  # Return the thresholded edge map as a NumPy array
