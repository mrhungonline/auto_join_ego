import threading
from pynput import keyboard

# Global variables to control the listening and thread status
listening = True
thread_running = False
thread = None  # Initialize the thread variable

def perform_action():
    global thread_running

    while listening and thread_running:
        print("Thread is running when F3 is pressed.")

def on_key_release(key):
    global listening, thread_running, thread

    if key == keyboard.Key.f3:
        if thread is None or not thread.is_alive():
            # Create a new thread and start it
            thread = threading.Thread(target=perform_action)
            thread_running = True
            thread.start()

    elif key == keyboard.Key.f4:
        # Turn off the thread when F4 is pressed
        thread_running = False
        print("F4 key has been pressed!")

        # Wait for the thread to stop before exiting
        if thread and thread.is_alive():
            thread.join()

        listening = False

# Listen for keyboard events
with keyboard.Listener(on_release=on_key_release) as listener:
    while listening:
        pass  # Wait until the listening flag becomes False
