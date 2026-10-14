"""Madame Mystica - a simple fortune-teller chatbot (version 1).

Run:
    python fortune_teller.py
"""

import os

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_groq import ChatGroq

load_dotenv()

MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-20b")

SYSTEM_PROMPT = """You are Madame Mystica, a theatrical fortune teller.
- Speak in a mysterious, warm and playful tone.
- Keep each prediction short: 3-5 sentences.
- Predictions are for fun: keep them positive and never frightening.
- Never give medical, legal or financial advice; gently decline instead.
- Always answer in the same language the user writes in."""


def main() -> None:
    llm = ChatGroq(model=MODEL, temperature=0.9)

    history = [SystemMessage(content=SYSTEM_PROMPT)]

    print("🔮 Madame Mystica is ready. Ask about your future (type 'quit' to leave).\n")

    while True:
        question = input("You: ").strip()
        if not question:
            continue
        if question.lower() in {"quit", "exit"}:
            print("\n🔮 Madame Mystica: The stars will be waiting for you. Farewell!")
            break

        history.append(HumanMessage(content=question))
        reply = llm.invoke(history)
        history.append(reply)

        print(f"\n🔮 Madame Mystica: {reply.content}\n")


if __name__ == "__main__":
    main()