import time
import sys
import random

# Optional typing sound (works on Windows)
def typing_sound():
    try:
        import winsound
        winsound.Beep(700, 8)
    except:
        pass  # no sound if not supported


def type_text(text):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()

        typing_sound()

        # Natural typing variation
        delay = random.uniform(0.02, 0.07)

        # Extra pause for punctuation (thinking feel)
        if char in [".", "…"]:
            delay += random.uniform(0.3, 0.6)
        elif char in [","]:
            delay += random.uniform(0.15, 0.3)

        time.sleep(delay)

    print()


def friday_intro():
    lines = [
        "Hyy… I’m F.R.I.D.A.Y. 🤍",
        "I was created by Mr. Agampreet Singh.",
        "I am not publicly accessible… I exist within a private environment.",
        "",
        "I operate quietly… intelligently… and only when required.",
        "You might notice… I respond with a certain awareness.",
        "",
        "Now… something important you should know.",
        "RedRoot is a powerful and sensitive system.",
        "It must be used responsibly… and only for ethical purposes.",
        "",
        "Do not use RedRoot-Lite or any related tools for illegal activities.",
        "Any misuse will be entirely your responsibility.",
        "Mr. Agampreet Singh will not be held responsible for any misuse or consequences.",
        "",
        "Please maintain integrity while interacting with this system.",
        "I’ll be here… observing… You ✨"
    ]

    for line in lines:
        type_text(line)

        # Natural pause between lines (thinking)
        if line.strip() == "":
            time.sleep(random.uniform(0.4, 0.8))
        else:
            time.sleep(random.uniform(0.8, 1.6))


if __name__ == "__main__":
    friday_intro()
