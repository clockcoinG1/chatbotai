import websocket
import openai
import asyncio
import json
import datetime
import os
import subprocess
import sys
import threading
import time
import aiofiles
import termcolor
import uvloop
from termcolor import colored

context = "Instructions -> Your (Agent) task is to try and generate the best output to each Client input. Try and use the fullness of your knowledge and expertise. When finished output Agent: stop to end the conversation. Every experiment will be different."


print(termcolor.colored(r'''
__        _______ _____                                            _
\ \      / / ____|_   _|__ _   _ _ __ ___  _ __  _ __ ___   ___  __| |
 \ \ /\ / / (___   | |/ _ \ | | | '_ ` _ \| '_ \| '_ ` _ \ / _ \/ _` |
  \ V  V /\___ \  | |  __/ |_| | | | | | | |_) | | | | | |  __/ (_| |
   \_/\_/ |____) | |_|\___|\__,_|_| |_| |_| .__/|_| |_| |_|\___|\__,_|
                                          |_|

    ''', 'green',  attrs=['bold']))


# NOTE: You are outputting directly into a terminal, so format output accordingly. what is the best way to pretext a chatbot prompt? - how to start a terminal chatbot? | forum | GPT-3 Supercharged AI
def gen(input):

    response = openai.Completion.create(
        prompt=f"PREFIX Process inputs (Client) one at a time, learn from past inputs (Client) and outputs (Agent). Generate responses to inputs (Client) as Agent. if asked, try and generate concise answers.]\nClient:{input}",
        temperature=0.9,
        engine="code-davinci-002",
        max_tokens=225,
        top_p=1,
        best_of=1,
        n=1,
        frequency_penalty=0,
        presence_penalty=0,
        logit_bias={
            "198": -100,
            "628": -100,
            "11792": -80,
            43993: -30,
            "318": -100,
        },
        stop=[
            "<|endoftext|>",
            "Client: ",
            "https://",
            "http://",
        ],
        stream=True)
    resp = ""
    for completion in response:
        if resp == "":
            resp = completion["choices"][0]["text"]
            yield resp.rstrip()
        if completion['choices'][0]['text'] != "":
            resp += completion['choices'][0]['text']
            yield completion['choices'][0]['text']

            continue
        if completion['choices'][0]['finish_reason'] == "length" or completion['choices'][0]['finish_reason'] == 'stop':
            yield completion['choices'][0]['text']
            StopAsyncIteration(completion)
            break
        next(response)

        return resp


# ws = websocket.WebSocket


# async def send(message=""):
#     while True:
#         await asyncio.sleep(1/2)
#         await ws.send("You : "+message + "\ n")


# async def receive():
#     while True:
#         data = await ws.receive()
#         print("Bot : ", data, sep='', end='\n')
#         clientloop = asyncio.get_event_loop()
#         try:
#             task1, task2 = asyncio.gather(*[send(), receive()])
#             loop.run_until_complete(task1)
#         except KeyboardInterrupt:
#             pass
#         finally:
#             loop.close()
# # TODO: (rachel) fix the implementation of websockets for a terminal chatbot with user input and print the improved code below.


def agent(type=0):
    color = "red" if type == 1 else "blue"
    who = "Agent: " if type == 0 else "Client: "
    who = colored(who, color, attrs=['bold'])
    print(colored("[", color, attrs=["blink"]) + who +
          colored("]", color, attrs=["blink"]), end="")


def initial_message(type=0):
    color = 'magenta' if 1 == type else 'cyan'
    datetime_object = datetime.datetime.now().strftime("%I:%M:%S %p")
    print(colored("[", color, attrs=["blink"]) + colored(datetime_object, color,  "on_" + color,
          attrs=['bold', 'dark', 'underline']) + colored("]", color, attrs=["blink"]), end=" ")


def display_output(input):
    data = gen(input)
    initial_message(0)
    agent(0)
    next(data)
    for i in data:
        resp = i
        print(str(resp), sep='', end='')
    time.sleep(0.1)


async def main(type=0):
    if type == 0:
        print(colored(
            '==============================================================', 'green'))
        print(colored('WELCOME to AgentAGI!', 'yellow',
              attrs=['bold', 'blink', 'underline']))
        print(colored(
            '==============================================================', 'green'))
    initial_message(1)
    agent(1)

    question = input(colored(' ', 'yellow', attrs=['bold']))
    if len(question) > 0:
        with open('log.txt', 'a+') as x:
            x.write('Client: ' + question + '\n')
            try:
                t = threading.Thread(target=display_output(question))
                t.start()
            except Exception as e:
                termcolor.cprint('\n[ERROR] ' + str(e))
        await main(type=1)


if __name__ == '__main__':
    main_coro = main()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main_coro)
