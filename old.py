import os
import json
import re
import time
import sys
import logging
import numpy as np
import requests
import asyncio
import websockets
import typing
from typing import Dict, List, Tuple, Union, Optional


class Choice(typing.NamedTuple):
    text: str
    index: int
    finish_reason: str
    logprobs: Dict[str, Union[List[float], int]]

def splitLines(chunk):
    lines = chunk.split('\n')
    lastLine = lines.pop()
    return [lines, lastLine]


async def get_chunks( body: asyncio.StreamReader, remainder: str, solutions: Dict[int, Choice], codex_channel: logging.Logger, ) -> asyncio.StreamReader:
    fs_stream = open(
        os.path.join(os.homedir(), "oai", f"oai-LOG-{time.strftime('%Y-%m-%d-%H-%M-%S')}.json"),
        "a+",
    )
    for chunk in body:
        lines, last_line = splitLines(remainder + chunk.decode())
        remainder = last_line
        for line in lines:
            trimmed_line = line[5:].strip()
            if "[DONE]" in trimmed_line:
                fs_stream.write(json.dumps(solutions))
                for item, solution in solutions.items():
                    if solution is not None:
                        codex_channel.info(f"DONE\n\n{solution.text}\n")
                        body.pipe(fs_stream, {end: True})
                        yield {
                            "text": solution.text,
                            "index": int(item),
                            "finish_reason": solution.finish_reason,
                            "logprobs": {
                                "tokens": solution.tokens,
                                "text_offset": solution.text_offset,
                                "top_logprobs": solution.top_logprobs,
                            },
                        }
            try:
                parsed_line = json.loads(trimmed_line)
            except json.JSONDecodeError:
                codex_channel.info(f"Error parsing JSON stream data {type(parsed_line)} {line}")
                continue
            if parsed_line.get("choices") is not None or parsed_line.get("error") is None:
                tokens = parsed_line["choices"][0]["logprobs"]["tokens"]
                text_offset = parsed_line["choices"][0]["logprobs"]["text_offset"]
                token_logprobs = parsed_line["choices"][0]["logprobs"]["token_logprobs"]
                top_logprobs = parsed_line["choices"][0]["logprobs"].get("top_logprobs")
                text = parsed_line["choices"][0]["text"]
                index_number = int(parsed_line["choices"][0]["index"])
                if not solutions[index_number]:
                    solutions[index_number] = parsed_line["choices"][0]
                else:
                    solutions[index_number]["logprobs"]["tokens"] = (
                        solutions[index_number]["logprobs"]["tokens"] + tokens
                    )
                    solutions[index_number]["logprobs"]["text_offset"] = (
                        solutions[index_number]["logprobs"]["text_offset"] + text_offset
                    )
                    solutions[index_number]["logprobs"]["token_logprobs"] = (
                        solutions[index_number]["logprobs"]["token_logprobs"] + token_logprobs
                    )
                    if top_logprobs and solutions[index_number]["logprobs"]["top_logprobs"]:
                        solutions[index_number]["logprobs"]["top_logprobs"] = (
                            solutions[index_number]["logprobs"]["top_logprobs"] + top_logprobs
                        )
                    solutions[index_number]["text"] += text
                    solutions[index_number]["index"] = index_number
    yield body
