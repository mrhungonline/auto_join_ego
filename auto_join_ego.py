import pygetwindow as gw
import pyautogui
import time
import opencv_controller
import threading
from pynput import keyboard
import keyboard

app_title = "EGOPlay"

pyautogui.FAILSAFE = False
def click(x,y):
    app_window = gw.getWindowsWithTitle(app_title)[0]  # Thay "Tiêu đề cửa sổ ứng dụng" bằng tiêu đề cửa sổ thực tế
    window_x, window_y = app_window.left, app_window.top
    pyautogui.click(window_x+x, window_y+y)

y_tat_ca_cac_kenh = 239
x_tat_ca_cac_kenh = 980
def get_room_y(phong_so):
    phong_0_y = 300
    gap = 61
    return phong_0_y + gap*(phong_so-1)

def auto_join_single(phong_so):
    time_gap  = 1
     # tất cả các kênh
    # click(922, 239)
    click(x_tat_ca_cac_kenh, y_tat_ca_cac_kenh)
    time.sleep(0.3)

    #kênh trống
    click(x_tat_ca_cac_kenh, 375)
    time.sleep(time_gap)

    #click vào phòng theo thứ tự
    click(x_tat_ca_cac_kenh, get_room_y(phong_so))
    time.sleep(time_gap)
    #hủy khi ko vào dc
    click(710, 500)
    time.sleep(time_gap)
    
def auto_join(phong_so):
    global  ego_thread_running
    for _ in range(2000):
        if not ego_thread_running:
            print("Truy cập vào chế độ Ranking AOE và ấn phím F3 để bắt đầu, Nhấn F4 để tạm dừng chương trình")
            time.sleep(2)
            continue
        # print(_)
        auto_join_single(phong_so)
        is_conatain_ego = opencv_controller.find_with_model(opencv_controller.model_path_icon_ego)
        print("Still in Ego: ", is_conatain_ego)
        if is_conatain_ego: 
            is_joined = opencv_controller.find_with_model(opencv_controller.model_path_btn_vao)
            print("Join Result: ", is_joined)
            if is_joined :
                break
        else:
            break

ego_thread_running = False
ego_thread = None 

def on_key_event(event):
    global  ego_thread_running, ego_thread
    if event.name == 'f3': 
        print("Đã nhấn phím F3")
        if ego_thread is None or not ego_thread.is_alive():
            ego_thread_running = True
    elif event.name == 'f4':  # Phát hiện phím F4
        print("Đã nhấn phím F4.")
        ego_thread_running = False
    elif event.name == 'f5':  # Phát hiện phím F4
        print("Đã nhấn phím F5.")

# Yêu cầu người dùng nhập một số
so_nhap = input("Phòng số mấy(ví dụ 3): ")
# so_nhap = 2




keyboard_thread = threading.Thread(target=keyboard.hook, args=(on_key_event,))
keyboard_thread.start()
ego_thread = threading.Thread(target= auto_join(int(so_nhap)))
ego_thread.start()
keyboard_thread.join()
ego_thread.join()