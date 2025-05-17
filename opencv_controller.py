import cv2
import os
import tempfile
from PIL import Image
import time
import ego_factory

model_path_btn_vao = os.getcwd()+'/models/btn_vao.png'
model_path_btn_day = os.getcwd()+'/models/btn_day.png'
model_path_btn_dangchoi = os.getcwd()+'/models/btn_dangchoi.png'
model_path_icon_ego = os.getcwd()+'/models/icon_ego.png'

def find_image_within(image_path, template_path):
    # Load the main image and the template image
    image = cv2.imread(image_path)
    template = cv2.imread(template_path)

    # Convert the images to grayscale
    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

    # Perform template matching
    result = cv2.matchTemplate(image_gray, template_gray, cv2.TM_CCOEFF_NORMED)

    # Set a threshold for the similarity score
    threshold = 0.8

    # Binarize the result image based on the threshold
    _, binary_result = cv2.threshold(result, threshold, 1, cv2.THRESH_BINARY)

    # Find non-zero locations in the binary result image
    locations = cv2.findNonZero(binary_result)

    # Check if the template was found in the image
    if locations is not None:
        # Process the first location and calculate x, y coordinates
        x, y = locations[0][0]
        template_width = template.shape[1]
        template_height = template.shape[0]
        x += int(template_width / 2)
        y += int(template_height / 2)
        return x, y

    # Template image not found in the main image
    return -1, -1

def sleep(second):
    # print(f"==> sleep: {second} seconds")
    time.sleep(second)
    
def find_with_model(model_path):
    # Create a temporary file with a .jpg extension
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp_file:
        current_time = int(time.time() * 1000)
        temp_file_path = temp_file.name.replace(".png", f"_{current_time}.png")
        temp_file.close()

        # adb_controller.take_screenshot("emulator-5554", temp_file_path)
        ego_factory.take_screenshot_with_path( temp_file_path)
        # image.save(temp_file_path)

        # Print the path to the temporary file
        # print("Image saved to temporary file:", temp_file_path)
        
        # template_path = os.getcwd()+'/models/btn_multi_images.png';
        x, y = find_image_within(temp_file_path, model_path)
    
        os.remove(temp_file_path)

        if x == -1 and y == -1:
            return False
        else:
            return True