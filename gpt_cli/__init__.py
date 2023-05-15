from rich.console import Console
from rich.markdown import Markdown

import os
import openai
import click

console = Console()
openai.api_key = os.getenv("OPENAI_API_KEY")


state = [{"role": "system", "content": "You are a helpful assistant."}]


@click.command()
def main():
    while True:
        message = input("> ")
        if message == "q" or message == "exit":
            exit(0)
        state.append({"role": "user", "content": message})
        with console.status("Thinking..."):
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo", messages=state
            )
        gpt_item = response["choices"][0]["message"]
        console.print(Markdown(gpt_item["content"]))
        state.append(gpt_item)


if __name__ == "__main__":
    main()
