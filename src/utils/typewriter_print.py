import time


def typewriter_print(text, *, delay=0.05, end='\n'):
    for letter in list(text):
        print(letter, end='', flush=True)
        time.sleep(delay)

    print(end, end='')
