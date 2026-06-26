from core.llm import ask_llm
from core.personality import PERSONALITY
from rich import print


def run_chat():
    print("[bold violet]Liblitz est active.[/bold violet]")
    print("Tape 'exit' pour quitter.\n")

    while True:
        user_input = input("Romain > ")

        if user_input.lower() == "exit":
            break

        prompt = f"""{PERSONALITY}

Conversation actuelle :

Romain : {user_input}

Liblitz :
"""

        response = ask_llm(prompt)

        print(f"\n[bold cyan]Liblitz >[/bold cyan] {response}\n")
