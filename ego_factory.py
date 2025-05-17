import pygetwindow as gw
import pyautogui

# # Lấy danh sách các cửa sổ đang mở
# windows = gw.getAllTitles()

# # In ra tiêu đề của các cửa sổ
# for window in windows:
#     print(window)
app_title = "EGOPlay"

def take_screenshot_with_path(temp_file_path):
    app_window = gw.getWindowsWithTitle(app_title)[0]  
    screenshot = pyautogui.screenshot(region=(app_window.left, app_window.top, app_window.width, app_window.height)) 
    screenshot.save(temp_file_path)