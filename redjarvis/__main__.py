import time
import sys

def chat_typing(text, delay=0.035):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def redjarvis_chat():
    message = (
        "RedJarvis: Hello. "
        "I am RedJarvis. "
        "I was created by Mr. Agampreet Singh. "
        "I am designed to operate exclusively for my creator. "
        "You are not authorized to access me without my creator’s permission. "
        "Access denied."
    )

    chat_typing(message, 0.03)

if __name__ == "__main__":
    redjarvis_chat()
