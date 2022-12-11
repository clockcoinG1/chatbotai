
import datetime
import os
import re
import subprocess
import sys
import time
from argparse import ArgumentParser

import openai
from colorama import init
from pyfiglet import figlet_format
from termcolor import colored, cprint

init(strip=not sys.stdout.isatty())

context = "Instructions -> Your (Output) task is to try and generate the best output to each Input input. Try and use the fullness of your knowledge and expertise. When finished output Output: stop to end the conversation. Every experiment will be different."


cprint(figlet_format('ªºAGIæ', font='speed', width=100, justify="center"),
       'blue', attrs=['bold', 'dark', 'underline'])


def _get_clipboard(prompt):
    with subprocess.Popen(['pbpaste'], stdout=subprocess.PIPE, encoding="utf-8") as p:
        data = p.stdout.read().format("utf-8").strip()
        prompt = prompt.replace(
            '\pb', '') + data[:1200].replace('\r', '\\r').replace('\n', '\\n')
        return prompt


def _gen(input):
    max_tokens = 175
    input = str(input).replace('\r', '\\r').replace('\n', '\\n').strip()
    if '\pb' in input:
        input = _get_clipboard(input)
        cprint(input[:50] + '....\n(output hidden) Prompt length' + str(len(input)),
               "grey", "on_white", attrs=["bold"])
    if '!=' in input:
        max_tokens = int(input.split('!=')[1].split()[0])
        input = input.replace('!=', '')

    response = openai.Completion.create(
        prompt=f"Instructions -> Process inputs (Input) one at a time. Generate responses (Output) to inputs (Input). Try and generate concise answers and print everything in the terminal screen nicely. You will mostly be asked to provide advanced one liner terminal commands for a macOS developer.\nNOTE: Try to stay under 175 characters if possible.\nInput ->{input}\nOutput ->",

        temperature=0.9,
        engine="code-davinci-002",
        max_tokens=max_tokens,
        top_p=1,
        best_of=4,
        n=1,
        frequency_penalty=0,
        presence_penalty=0,
        logit_bias={
            5450: -10,
            20560: -3,
            27: -3,
            8189: -3,
            198: -5,
            3784: -3,
            59: -5,
            81: -3,
            628: -10,
            11792: -80,
            43993: -30,
            318: -100,
            14804: -10,
            3784: -10
        },
        stop=[
            "Input -> ",
            "\n",
            "\r",
            "http*",
        ],
        stream=True)
    resp = ""
    for completion in response:
        text = completion["choices"][0]["text"]
        if text == "\n" or text == '\r':
            pass
        if text == "":
            resp = completion["choices"][0]["text"]
            continue
        if text != "":
            resp += completion['choices'][0]['text']
            yield completion['choices'][0]['text']
            continue
        if completion['choices'][0]['finish_reason'] == "length" or completion['choices'][0]['finish_reason'] == 'stop':
            yield completion['choices'][0]['text']
            StopAsyncIteration(completion)
            break

    return resp


def _agent(type=0):
    color = "red" if type == 1 else "blue"
    who = "Output -> " if type == 0 else "Input -> "
    who = colored(who, color, attrs=['bold'])
    print(colored("[", color, attrs=["blink"]) + who +
          colored("]", color, attrs=["blink"]), end="")


def _initial_message(type=0):
    color = 'white' if 1 == type else 'blue'
    datetime_object = datetime.datetime.now().strftime("%I:%M:%S %p")
    print('\n' + colored("[", color, attrs=["blink"]) + colored(datetime_object, color,
          attrs=['bold', 'dark', 'underline']) + colored("]", color, attrs=["blink"]), end=" ")


def _loaded_message(init):
    time_now = time.ctime()
    print(colored('[INFO] ', 'green', attrs=['bold']) +
          colored('Session started at : ', 'yellow', attrs=['bold']) + str(time_now))
