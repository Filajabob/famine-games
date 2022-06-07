import time


def typewriter_input(text, *, delay=0.3):
    for letter in text.split():
        print(letter, end=' ', flush=True)
        time.sleep(delay)

    return input('')

