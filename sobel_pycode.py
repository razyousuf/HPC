#########################################################################
#   Project Name: Sobel Algorithm Perforance improvement using Cython   #
#   Author:       Raz Yousufi                                           #
#   Supervisor:   Professor David Reid                                  #
#   Date Created: February 11, 2024                                     #
#########################################################################

# 1. Import libraries
import numpy as np

##==============================================================================
# 2. Define a function to apply Sobel filter to the input image
def sobel_filter(image):
    # Sobel filters for horizontal and vertical gradients
    Gx = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])  # Sobel filter for horizontal gradient
    Gy = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])  # Sobel filter for vertical gradient

    # Get dimensions of the input image
    rows, cols = image.shape

    # Initialize an array to store edge map
    edge_map = np.zeros((rows, cols))
    print(f"\n>> Edge-Map is initialized as follows:\n {edge_map}\n")

    # Iterate over each pixel in the image
    for i in range(1, rows - 1):
        for j in range(1, cols - 1):
            # Compute horizontal gradient
            sx = np.sum(np.multiply(Gx, image[i - 1:i + 2, j - 1:j + 2]))
            # Compute vertical gradient
            sy = np.sum(np.multiply(Gy, image[i - 1:i + 2, j - 1:j + 2]))

            # Compute gradient magnitude using Euclidean distance formula
            edge_map[i, j] = np.sqrt(sx**2 + sy**2)

    return edge_map

##==============================================================================
# 3. Define a function to apply threshold to the edge map (control the sensitivity of the edge detection)
def apply_threshold(edge_map, threshold=150):
    # Apply thresholding to the edge map
    thresholded = np.where(edge_map > threshold, 255, 0)
    return thresholded

##==============================================================================
# 4. Define a function to perform Sobel edge detection on the input image
def sobel_edge_detection(image):
    # Apply Sobel filter to the input image
    edges = sobel_filter(image)
    #print(f"\nThe image after Sobel filter is implemented:\n {edges}\n")
    print("\n>> Sobel Algorithm has completed filtering.\n")

    # Apply thresholding to the resulting edge map
    thresholded_edges = apply_threshold(edges)
    return thresholded_edges
    
