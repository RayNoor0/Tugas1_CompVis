# Script to create a proper checkerboard image for camera calibration
import cv2
import numpy as np

def create_checkerboard_image():
    """
    Create a proper checkerboard image suitable for camera calibration.
    """
    # Parameters for checkerboard
    board_width = 8   # Number of internal corners horizontally
    board_height = 6  # Number of internal corners vertically
    square_size = 50  # Size of each square in pixels
    
    # Calculate image dimensions
    img_width = (board_width + 1) * square_size
    img_height = (board_height + 1) * square_size
    
    # Create the checkerboard image
    checkerboard = np.zeros((img_height, img_width), dtype=np.uint8)
    
    # Fill the checkerboard pattern
    for i in range(board_height + 1):
        for j in range(board_width + 1):
            if (i + j) % 2 == 0:
                # White square
                y_start = i * square_size
                y_end = (i + 1) * square_size
                x_start = j * square_size
                x_end = (j + 1) * square_size
                checkerboard[y_start:y_end, x_start:x_end] = 255
    
    return checkerboard

if __name__ == "__main__":
    # Create and save the checkerboard
    checkerboard_img = create_checkerboard_image()
    cv2.imwrite("checkerboard.png", checkerboard_img)
    print("Checkerboard image created and saved as 'checkerboard.png'")
    print(f"Image dimensions: {checkerboard_img.shape}")
    print(f"Pattern size: 8x6 internal corners")
