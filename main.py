import json
import time
import subprocess
import sys
import termcolor
import datetime
import openai
from termcolor import colored
#  You are a top-level specialist in every specific field. It is absolutely imperative that you understand this project as well its problem context to complete it efficiently and robustly. You should be able to answer them all yourself by asking \"How would I implement this piece if it were just me working with no limitations?[CONTEXTUAL INFO FOR AI Agent ONLY] You (Agent) possess artificial general intelligence with infinite knowledge on every subject. Lets try to answer my (Client) questions to the best of our abilities.\nYou should do this by observing past logs of interactions between (Client) and (Agent) and extracting information from the conversations to advance to the next stage in the conversation. The goal is for (Agent) to be able to generate the most accurate responses to the questions and tasks. Note that the sender and receiver of each message in the data is specified explicitly by the Client and Agent name\n
context = "Instructions: Process inputs (Client) one at a time, learn from past inputs (Client) and outputs (Agent). Generate responses to inputs (Client) as output (Agent) to advance the conversation to the next stage. If asked, try and generate concise answers or oneliner functions for the requested tasks"


def main(type=1, summary=None):
    if type == 1 or summary == None:
        print(colored(r'''
         ____             _ __
         / __ \____ ______(_) /_  ___  _____
        / /_/ / __ `/ ___/ / __ \/ _ \/ ___/
        / ____/ /_/ (__  ) / /_/ /  __/ /
        /_/    \__,_/____/_/_.___/\___/_/
        =====================================
        WELCOME TO CONTEXTUAL AI AGENTS!
        =====================================
        > This is a simple in terminal chat bot
            that can be used for any chat sessions
        > We will use Popen() for opening
            processes and communicating with them
    ''', 'green', attrs=['bold']))

        args = ['tail', '-n', '5', 'log.txt']
        try:
            command2 = subprocess.Popen(args, stdout=subprocess.PIPE)
            output, errors = command2.communicate()
            x = output.decode("utf-8")
            summary = openai_summarize(x)
            # print(colored(summary, 'green'), '\n')
        except subprocess.TimeoutExpired:
            pass

    question = input('\n\nClient: ')
    with open('log.txt', 'a+') as x:
        x.write(question)
        x.close()
    question = f"{context}\nClient: {question}\nAgent:"
    try:
        response = openai_completion(
            summary + '\n' + question)
        if response:
            summary = openai_summarize("PREVIOUS QUESTION: " + question +
                                       "\nPREVIOUS RESPONSE: " + response + "\nSUMMARY: " + summary
                                       )

            termcolor.cprint(
                'Summary: ' + summary, 'cyan', attrs=['bold'])
            termcolor.cprint(summary, 'blue')
            main(type=0, summary=summary)

        else:
            print("I do not understand the question.",  response)
            # openai_completion()
    except Exception as e:
        print(str(e))

    # run this so that if it's not a command it can be answered by the AI
    # the user can specify output from only the AI


def openai_summarize(input):
    try:
        response = openai.Completion.create(
            engine="code-davinci-002",
            prompt="{}\n{}\ntl;dr;".format(context, input),
            max_tokens=380,
            temperature=0.9,
            top_p=1,
            # "\w{25,}", "\W{10}", "<div.*?>", "<span.*?>"],
            # "(?=\w{30,})(?<!\.)",
            stop=[
                "\w{30,}",
                "```",
                "#.*",
                "\n\n",

            ],
            logprobs=0,
            n=1,
        )
        sum = open('summary.txt', 'a+',
                   encoding='utf-8')
        sum.write('Summary: ' + response['choices'][0]['text'] + '\n')
        sum.close()
        # print("{}".format(response["choices"][0]["text"].substring(0, 50) + '...'))
        return response['choices'][0]['text']
    except Exception as e:
        print(e)
        return ''


def openai_completion(input):

    # Question for Agent."\`\`\`",  "\w{30,}" "\`", r"\W{30,}" r"\<", r"\<\w{5,}"],

    try:
        response = openai.Completion.create(
            prompt="Context: {}\n{}\nAgent: ".format(context, input),
            engine="code-davinci-002",
            temperature=0.9,
            max_tokens=250,
            top_p=1,
            n=1,
            best_of=1,
            frequency_penalty=1,
            presence_penalty=0.6,
            stop=[
                "Client:",
                "\nClient: ",
            ],
            stream=True,
        )
        resp = ""
        datetime_object = datetime.datetime.now()
        colored_now = termcolor.colored(
            datetime_object.strftime("%H:%M:%S"), 'green')
        print('[' + colored_now + ']' + '\tAgent: ',
              end='', sep='')
        sum = open('log.txt', 'a+', encoding='utf-8')

        for completion in response:
            if not completion['choices'][0]['text']:
                next(response)
            if completion['choices'][0]['finish_reason'] == 'stop' or completion['choices'][0]['finish_reason'] == 'finish':
                print(termcolor.colored(
                    completion['choices'][0]['text'], 'cyan'), end='', sep='')
                resp += completion['choices'][0]['text']
                StopAsyncIteration(response)
            else:
                resp += completion['choices'][0]['text']
                print(termcolor.colored(
                    completion['choices'][0]['text'], 'cyan'), end='', sep='')
                next(response)
        sum.write(datetime_object.strftime('%H:%M:%S') + '\t' + resp + '\n')
        sum.close()
        return resp
# for completion in response:
#             if not completion['choices'][0]['text']:
#                 next(response)
#             if completion['choices'][0]['finish_reason'] == 'stop' or completion['choices'][0]['finish_reason'] == 'finish':
#                 print(termcolor.colored(
#                     completion['choices'][0]['text'], 'cyan'), end='', sep='')
#                 resp += completion['choices'][0]['text']
#                 StopAsyncIteration(response)
#             else:
#                 resp += completion['choices'][0]['text']
#                 print(termcolor.colored(
#                     completion['choices'][0]['text'], 'cyan'), end='', sep='')
#                 next(response)
#         sum.write(datetime_object.strftime('%H:%M:%S') + '\t' + resp + '\n')
#         sum.close()
#         return resp
# try:
#         response = openai.Completion.create(
#             prompt="Context: {}\n{}\nAgent: ".format(context, input),
#             engine="code-davinci-002",
#             temperature=0.9,
#             max_tokens=850,
#             top_p=1,
#             frequency_penalty=1,
#             presence_penalty=0.6,
#             stop=[
#                 "Client:",
#                 "\w{30,}",
#                 "\nClient: ",
#                 "#.*",
#             ],
#             stream=True,
#         )
    # resp = ""
    # for item in response:
    #     if item['choices'][0]["finish_reason"] == "length":
    #         resp = item['choices'][0]['text']
    #         print(resp)
    #         # sum.write('Promise: ' + resp + '\n')
    #         # sum.close()
    #         break
    #     if item['choices'][0]["finish_reason"] == "stop":
    #         resp += item['choices'][0]['text']
    #         # sum.write('Promise: ' + resp + '\n')
    #         # sum.close()
    #         print(resp)
    #         break
    #     else:
    #         print(item['choices'][0]['text'], sep="", end="")
    #         sum.write(response['choices'][0]['text'] + '\n' + input + '\n')
    #         resp += item['choices'][0]['text']
    # sum.close()
    # return resp

    except openai.error.APIError as error:
        print(error)


if __name__ == '__main__':

    main(type=1, summary=None)
