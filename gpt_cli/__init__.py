from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Padding

import os
import openai
import click

console = Console()

state = [{"role": "system", "content": "You are a helpful assistant."}]


@click.command()
@click.argument("text", required=False)
@click.option(
    "--token",
    default=lambda: os.environ.get("OPENAI_API_KEY", ""),
    help="Your OpenAI API token",
)
def main(text, token):
    if not token:
        console.print(
            "[bold red]No token provided.[/] Pass --token or set OPENAI_API_KEY in your environment."
        )
        exit(1)

    while True:
        message = console.input("[cyan]>[/] ") if not text else text
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
