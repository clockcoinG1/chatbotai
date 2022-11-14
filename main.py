# import websocket
import asyncio
import datetime

import threading
import time

import openai
import termcolor
from termcolor import colored

context = "Instructions -> Your (Output) task is to try and generate the best output to each Input input. Try and use the fullness of your knowledge and expertise. When finished output Output: stop to end the conversation. Every experiment will be different."


print(termcolor.colored(r'''
__        _______ _____                                            _
\ \      / / ____|_   _|__ _   _ _ __ ___  _ __  _ __ ___   ___  __| |
 \ \ /\ / / (___   | |/ _ \ | | | '_ ` _ \| '_ \| '_ ` _ \ / _ \/ _` |
  \ V  V /\___ \  | |  __/ |_| | | | | | | |_) | | | | | |  __/ (_| |
   \_/\_/ |____) | |_|\___|\__,_|_| |_| |_| .__/|_| |_| |_|\___|\__,_|
                                          |_|

    ''', 'green',  attrs=['bold']), flush=True, end="\n=============================================\n")


# NOTE: You are outputting directly into a terminal, so format output accordingly. what is the best way to pretext a chatbot prompt? - how to start a terminal chatbot? | forum | GPT-3 Supercharged AI
def gen(input):

    response = openai.Completion.create(
        prompt=f"Process inputs (Input) one at a time. Generate responses (Output) to inputs (Input). Try and generate concise answers and print everythin in the terminal screen nicely.\nInput ->{input}\nOutput ->",
        temperature=0.5,
        engine="code-davinci-002",
        max_tokens=75,
        top_p=1,
        best_of=4,

        frequency_penalty=0,
        presence_penalty=0,
        logit_bias={
            5450: -10,
            20560: -3,
            198: -5,
            3784: -3,
            59: -5,
            81: -3
            # 628: -100,
            # 11792: -80,
            # 43993: -30,
            # 318: -100,
            # 14804: -10,
            # 3784: -10
        },
        stop=[
            "\nInput -> ",
            "DONE",
            "\n\n",
            "\r",
            # "https://",
        ],
        stream=True)
    resp = ""
    for completion in response:
        text = completion["choices"][0]["text"]
        if text == "\n" or text == '\r':
            pass
        if text == "":
            resp = completion["choices"][0]["text"]
            yield resp.rstrip()
        if text != "":
            resp += completion['choices'][0]['text']
            yield completion['choices'][0]['text']
            continue
        if completion['choices'][0]['finish_reason'] == "length" or completion['choices'][0]['finish_reason'] == 'stop':
            yield completion['choices'][0]['text']
            StopAsyncIteration(completion)
            break

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
    who = "Output -> " if type == 0 else "Input -> "
    who = colored(who, color, attrs=['bold'])
    print(colored("[", color, attrs=["blink"]) + who +
          colored("]", color, attrs=["blink"]), end="")


def initial_message(type=0):
    color = 'white' if 1 == type else 'blue'
    datetime_object = datetime.datetime.now().strftime("%I:%M:%S %p")
    print('\n' + colored("[", color, attrs=["blink"]) + colored(datetime_object, color,
          attrs=['bold', 'dark', 'underline']) + colored("]", color, attrs=["blink"]), end=" ")


def display_output(input):
    data = gen(input)
    initial_message(0)
    agent(0)
    for i in data:
        resp = i
        if resp == '\r':
            continue
        if not resp:
            continue
        else:
            print(str(resp), sep='', end='')
            next(data)
    time.sleep(0.1)


async def main(type=0):
    if type == 0:
        print(colored(
            '==============================================================', 'green'))
        print(colored('WELCOME to OutputAGI!', 'yellow',
              attrs=['bold', 'blink', 'underline']))
        print(colored(
            '==============================================================', 'green'))
    initial_message(1)
    agent(1)

    question = input(colored(' ', 'yellow', attrs=['bold']))
    if len(question) > 0:
        with open('log.txt', 'a+') as x:
            x.write('Input -> ' + question + '\n')
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
