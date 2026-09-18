from gpiozero import LED, Button
from morse import encode_morse, decode_morse
import time

# --- Timing constants ---
def define_timings() -> None:
    global DOT_DASH, LETTER_SPACE, WORD_SPACE, MESSAGE_END
    DOT_DASH = UNIT * 2
    LETTER_SPACE = UNIT * 2
    WORD_SPACE = UNIT * 5
    MESSAGE_END = UNIT * 10

UNIT = 0.5
define_timings()

def txt_to_morse() -> None:
    originalString = input("Enter text to encode: ")
    if not originalString:
        return
    encoded_morse = encode_morse(originalString)
    print(f"Morse: {encoded_morse}")
    flash_leds(encoded_morse)

def flash_leds(morse_code: str):
    for symbol in morse_code:
        if symbol == ".":
            red_led.on(); time.sleep(0.2); red_led.off()
        elif symbol == "-":
            yellow1_led.on(); yellow2_led.on()
            time.sleep(0.5)
            yellow1_led.off(); yellow2_led.off()
        elif symbol == "/":
            time.sleep(0.4)
        time.sleep(0.2)


def output_letter(curr_letter: list[str]) -> str:
    if not curr_letter:
        return ""
    char = decode_morse("".join(curr_letter))
    print(char, end="", flush=True)
    return char


def wait_with_feedback() -> tuple[str, float]:
    gap_start = time.time()

    pressed = btn.wait_for_press(timeout=LETTER_SPACE)
    if pressed:
        return ("intra", time.time() - gap_start)

    red_led.on(); yellow1_led.on(); yellow2_led.on()
    time.sleep(0.1)
    red_led.off(); yellow1_led.off(); yellow2_led.off()

    pressed = btn.wait_for_press(timeout=WORD_SPACE - LETTER_SPACE)
    if pressed:
        return ("letter", time.time() - gap_start)

    yellow1_led.on(); yellow2_led.on()
    time.sleep(0.15)
    yellow1_led.off(); yellow2_led.off()

    pressed = btn.wait_for_press(timeout=MESSAGE_END - WORD_SPACE)
    if pressed:
        return ("word", time.time() - gap_start)

    return ("end", time.time() - gap_start)

def record_morse() -> str:
    words: list[list[str]] = []
    curr_word: list[str]   = []
    curr_letter: list[str] = []
    first_press: bool = True

    print("Recording...")
    while True:
        event, gap_time = wait_with_feedback()

        if event == "end":
            output_letter(curr_letter)
            if curr_letter:
                curr_word.append("".join(curr_letter))
                curr_letter = []
            if curr_word:
                words.append(curr_word)
            break

        if not first_press:
            if event == "word":
                output_letter(curr_letter)
                print(" ", end="", flush=True)
                if curr_letter:
                    curr_word.append("".join(curr_letter))
                    curr_letter = []
                if curr_word:
                    words.append(curr_word)
                    curr_word = []
            elif event == "letter":          # FIX: correctly inside if not first_press
                output_letter(curr_letter)
                if curr_letter:
                    curr_word.append("".join(curr_letter))
                    curr_letter = []

        first_press = False

        hold_start = time.time()
        btn.wait_for_release()
        hold_time = time.time() - hold_start

        if hold_time < DOT_DASH:
            symbol = "."
            red_led.on(); time.sleep(0.1); red_led.off()
        else:
            symbol = "-"
            yellow1_led.on(); yellow2_led.on()
            time.sleep(0.1)
            yellow1_led.off(); yellow2_led.off()

        curr_letter.append(symbol)

    print()
    print("Morse code parsed.")
    morse_str = " \\ ".join(" ".join(letters) for letters in words)
    return morse_str


def file_to_morse() -> None:
    filename = input("Enter the path of the text file to be encoded: ")
    try:
        # Reads file
        with open(filename, 'r') as file:
            lines = file.readlines()
        print("File found successfully")
        for line in lines:
            line = line.strip()
            if line:
                # Translates file line by line
                encoded = encode_morse(line)
                print(f"Morse: {encoded}")
                flash_leds(encoded)

    except FileNotFoundError:
        print("File not found")


def instructions():
    print("--- Instructions --- \n\n-Mode 1-\n*Make sure you do not use any punctuality, it cannot be translated to morse, otherwise the outcome will be ? \n\n-Mode 2-\n*For the standard setting (short), hold the button briefly (under 0.5s) to input a dot (the red LED will flash) \n*For a dash, hold it longer (0.5s or more, both yellow LEDs will flash) \n*Pause for 1.0s to move to the next letter (all 3 LEDs will flash)\n*Wait 2.5s to start a new word (both yellow LEDs will flash)\n*To finish the message, wait 5.0s \n\n-Mode 4-\n*In option 4, you can change your timings to accomodate your experience \n*The standard setting is short \n\n--- END OF INSTRUCTIONS ---")


def change_timings():
    global UNIT

    choice = input("Short - 0.5s\nMedium - 1s\nLong - 10s\nSelect timing speed: ").lower()
    match choice:
        case "short":
            UNIT = 0.5
        case "medium":
            UNIT = 1
        case "long":
            UNIT = 2
        case _:
            print("Invalid choice. No changes were made.")
            return

    # Recalculate all derived constants
    define_timings()

    print("Timings updated.")


# --- Hardware Setup ---
red_led     = LED(14)
yellow1_led = LED(21)
yellow2_led = LED(20)
btn = Button(3)

# --- Main Logic Loop ---
try:
    while True:
        print("\n--- Morse System ---")
        print("1: Encode & Flash | 2: Physical Button Decode | 3: Translate a text file | 4: Change timings | 5: Help | Blank: Quit")
        choice = input("Enter your choice: ")
        
        match choice:
            case "1":
                txt_to_morse()
            case "2":
                record_morse()  
            case "3":
                file_to_morse()
            case "4":
                change_timings()
            case "5":
                instructions()
            case _:
                break

except KeyboardInterrupt:
    print("\nProgram Exited.")
