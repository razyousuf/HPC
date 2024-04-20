#########################################################################
#   Project Name: Sobel Algorithm Perforance improvement using Cython   #
#   Author:       Raz Yousufi                                           #
#   Supervisor:   Professor David Reid                                  #
#   Date Created: February 11, 2024                                     #
#########################################################################

# 1. Import libraries
import numpy as np
import matplotlib.pyplot as plt
import time
import threading
import imageio.v2 as imageio
from sobel_pycode import sobel_edge_detection
from sobel_cycode import sobel_edge_detection_cy

# 2. The Function to convert image into grayscale (Frequency domain)
def rgb2gray(rgb):
    return np.dot(rgb[...,:3], [0.2989, 0.5870, 0.1140])

# 3. Read the image and convet it to grayscale
color_image = imageio.imread('img4.png') 
# Convert the image into its grayscale using the rgb2gray function
gray_image = rgb2gray(color_image).astype(np.float64)

##==========================================================================================
# 4. Function for edge detection processes by python and cython
def process_and_time(function, image, label):
    start_time = time.time()
    result = None
    completed = False

    def process_image():
        nonlocal result, completed
        result = function(image)
        completed = True
    
    print("")
    print(f"Sobel algorithm has started to detect the edges in the image using [{label}] ...")
    print("")
    
    # Start the edge detection in a separate thread
    processing_thread = threading.Thread(target=process_image)
    processing_thread.start()

    while processing_thread.is_alive():
        processing_thread.join(timeout=1)
        elapsed_time = time.time() - start_time
        print(f"{label}: {int(elapsed_time)} second(s) passed.")
    print("")
    print(f"{label} has detected all the edges in ({elapsed_time:.2f}) seconds.")
    print("===========================================================")
    return result, elapsed_time

##==========================================================================================
# 5. Process the image using Python
python_result, python_time = process_and_time(sobel_edge_detection, gray_image, "Python")

# 5. Process the image using Cython
cython_result, cython_time = process_and_time(sobel_edge_detection_cy, gray_image, "Cython")

##==========================================================================================
# 6. Plotting the original and edge-detected images
fig, ax = plt.subplots(2, 2, figsize=(10, 8), gridspec_kw={'height_ratios': [2, 3]})


fig.delaxes(ax[0][1]) # Remove the empty subplot (top right)
# Original image on the top
ax[0][0].imshow(color_image)
ax[0][0].set_title('Original Image')
ax[0][0].axis('off')

# Edges detected by Python code on the bottom left
ax[1][0].imshow(python_result, cmap='inferno') # cmap='OrRd', 'Dark2', 'viridis', 
ax[1][0].set_title('Python Sobel-detected Edges')
ax[1][0].axis('off')

# Edges detected by Cython code on the bottom right
ax[1][1].imshow(cython_result, cmap='inferno')
ax[1][1].set_title('Cython Sobel-detected Edges')
ax[1][1].axis('off')


# Plotting Timing information for Python and Cython Codes
ax[1][0].text(0.5, -0.3, f"(a) Python Time: {python_time:.2f} seconds",
              horizontalalignment='center', verticalalignment='center', fontsize=12, transform=ax[1][0].transAxes)
ax[1][1].text(0.5, -0.3, f"(b) Cython Time: {cython_time:.2f} seconds",
              horizontalalignment='center', verticalalignment='center', fontsize=12, transform=ax[1][1].transAxes)

plt.tight_layout()
plt.show()
