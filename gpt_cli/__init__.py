from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Padding

import os
import openai
import click

console = Console()
openai.api_key = os.getenv("OPENAI_API_KEY")


state = [{"role": "system", "content": "You are a helpful assistant."}]


@click.command()
@click.argument("text", required=False)
def main(text):
    while True:
        message = console.input("[black on cyan] > [/] ") if not text else text
        if message == "q" or message == "exit":
            exit(0)
        state.append({"role": "user", "content": message})
        with console.status("Thinking..."):
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo", messages=state
            )
        gpt_item = response["choices"][0]["message"]
        renderable = Padding(Markdown(gpt_item["content"]), (1, 1))
        console.print(renderable)
        if text:
            exit()
        state.append(gpt_item)


if __name__ == "__main__":
    main()
