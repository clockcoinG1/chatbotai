import argparse
import asyncio
import signal
import sys
import threading
import time
from argparse import ArgumentParser

import termcolor
from colorama import Fore, Style, init
from termcolor import colored

from chatbot import _agent, _gen, _initial_message, _loaded_message

parser = argparse.ArgumentParser()
init()

# mkdir t2v_app && cd t2v_app && python3 -m venv venv && source venv/bin/activate && echo 'venv' >.gitignore && touch main.py;


async def main(type=0):
    def signal_handler(sig, frame):
        from termcolor import colored
        print(colored('\n[INFO] You pressed Ctrl+C!',
              'red', attrs=['bold', 'blink']))
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    if type == 0:
        print(colored(
            '==============================================================', 'green'))
        print(colored('ヽ༼ຈل͜ຈ༽ﾉ RIOT ヽ༼ຈل͜ຈ༽ﾉ RITE KILL STEAL ヽ༼ຈل͜ຈ༽ﾉ Get dunked on PSYduckAGI ☠️☠️☠️💀⚰️👻→ !', 'yellow',
              attrs=['bold', 'blink', 'underline']))
        print(colored(
            '==============================================================', 'green'))
        _loaded_message(1)
    _initial_message(0)
    _agent(1)
    question = input(colored(' ', 'yellow', attrs=['bold']))
    if len(question) > 0:
        with open('log.txt', 'a+') as x:
            x.write('Input -> ' + question + '\n')
            try:
                t = threading.Thread(target=_display_output(question))
                t.start()

            except Exception as e:
                termcolor.cprint('\n[ERROR] ' + str(e))
        await main(type=1)


def _display_output(input):
    data = _gen(input)
    _initial_message(0)
    _agent(0)
    ret = ""
    for i in data:
        resp = i
        if resp == '\r' or resp == '\n':
            ret += resp
            print('\n')
            pass
        else:
            ret += resp
            print(str(resp), sep='', end='')
    time.sleep(0.1)
    with open('log.txt', 'a+') as source:
        source.write('Output -> ' + ret + '\n')
        source.close()


if __name__ == '__main__':
    main_coro = main()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main_coro)

# def main(type=0):
#     def signal_handler(sig, frame):
#         print('\n[INFO] You pressed Ctrl+C!')
#         sys.exit(0)
#     signal.signal(signal.SIGINT, signal_handler)
#     if type == 0:
#         print(colored(
#             '==============================================================', 'green'))
#         print(colored('WELCOME to OutputAGI!', 'yellow',
#               attrs=['bold', 'blink', 'underline']))
#         print(colored(
#             '==============================================================', 'green'))
#     _initial_message(1)
#     _agent(1)
#     question = ''
#     typing = True
#     #  = ..., buffering: int = ..., encoding: str | None = ..., errors: str | None = ..., newline: str | None = ..., closefd: bool = ..., opener: _Opener | None = ...) -> TextIOWrapper
#     while typing:
#         prev_len = len(question)
#         with open('/dev/tty', 'r') as stdin:
#             key = stdin.read(1)
#         if key == '\n':
#             typing = False
#             break
#         elif key in '\x7f\x08\x7f':
#             question = question[:-1]
#         elif key in '^[b':
#             _word_left()
#         elif key in '^[[D':
#             _cursor_left()
#         else:
#             question += key
#         if typing:
#             sys.stdout.write(question[prev_len:] + ' ')
#             sys.stdout.flush()
#     print('\n', end='')

#     if len(question.strip()) > 0:
#         _display_output(question)
#         main(type=1)


# main_coro = main()
# loop = asyncio.get_event_loop()
# loop.run_until_complete(main_coro)

def _cursor_left(n=1):
    print('\033[{}D'.format(n), end='')


def _word_left(n=1):
    # add '^[b' handling for back one word
    # replace with '^[B' to go forward one word
    print('\033[{}b'.format(n), end='')
