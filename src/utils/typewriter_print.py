import time


def typewriter_print(text, *, delay=0.3, end='\n'):
    for letter in text.split():
        print(letter, end=' ', flush=True)
        time.sleep(delay)

    print(end, end='')
