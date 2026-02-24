import cv2
import numpy as np
import pyautogui
import time
import os

def find_and_move_to_template(template_path, threshold=0.8, timeout=10):
    """
    Find template on screen and move mouse to it
    """
    if not os.path.exists(template_path):
        print(f"Template not found: {template_path}")
        return False
    
    template = cv2.imread(template_path, 0)
    h, w = template.shape
    
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        screenshot = pyautogui.screenshot()
        screen = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)
        
        result = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(result)
        
        if max_val >= threshold:
            center_x = max_loc[0] + w // 2
            center_y = max_loc[1] + h // 2
            
            print(f"Found at ({center_x}, {center_y}) - Moving mouse")
            pyautogui.moveTo(center_x, center_y, duration=0.5)
            return True
        
        time.sleep(0.3)
    
    print(f"Template not found after {timeout} seconds")
    return False

if __name__ == "__main__":
    template_file = input("Template image file: ")
    find_and_move_to_template(template_file)