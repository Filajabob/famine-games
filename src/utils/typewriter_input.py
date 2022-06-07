import time


def typewriter_input(text, *, delay=0.05):
    for letter in list(text):
        print(letter, end='', flush=True)
        time.sleep(delay)

    return input('')

