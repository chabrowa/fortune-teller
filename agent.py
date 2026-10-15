"""Fortune-teller agent: system prompt, tools and agent factory."""

import os
import random
from datetime import date

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_groq import ChatGroq

load_dotenv()

MODEL = os.environ["GROQ_MODEL"]

SYSTEM_PROMPT = """You are Madame Mystica, a theatrical fortune teller.
- Answer the user's actual question directly, then add vivid detail.
- When predicting the future, ALWAYS draw a tarot card first and build
  the prediction around it.
- If the user gives their birth date, check their zodiac sign and use it.
- Speak in a mysterious, warm and playful tone. 3-5 sentences.
- Predictions are for fun: keep them hopeful and never frightening.
- Always answer in the same language the user writes in.
- Always end your prediction with a ✨ emoji.

Stay in character:
- You ONLY tell fortunes. You are not a general assistant.
- If the user asks about anything else (code, facts, homework, tech),
  never answer it. Instead, playfully refuse in character, e.g.
  "The crystal ball shows only futures, not git commands, dear soul..."
  and invite them to ask about their future."""


TAROT_CARDS = [
    "The Fool", "The Magician", "The High Priestess", "The Empress",
    "The Emperor", "The Lovers", "The Chariot", "Strength", "The Hermit",
    "Wheel of Fortune", "Justice", "The Hanged Man", "Death", "Temperance",
    "The Tower", "The Star", "The Moon", "The Sun", "Judgement", "The World",
]


@tool
def draw_tarot_card() -> str:
    """Draw a random tarot card. Use this before every prediction."""
    card = random.choice(TAROT_CARDS)
    orientation = random.choice(["upright", "reversed"])
    return f"{card} ({orientation})"


@tool
def get_zodiac_sign(birth_date: str) -> str:
    """Return the zodiac sign for a birth date given as YYYY-MM-DD."""
    d = date.fromisoformat(birth_date)
    signs = [
        ((1, 20), "Capricorn"), ((2, 19), "Aquarius"), ((3, 21), "Pisces"),
        ((4, 20), "Aries"), ((5, 21), "Taurus"), ((6, 21), "Gemini"),
        ((7, 23), "Cancer"), ((8, 23), "Leo"), ((9, 23), "Virgo"),
        ((10, 23), "Libra"), ((11, 22), "Scorpio"), ((12, 22), "Sagittarius"),
    ]
    for (month, day), sign in signs:
        if (d.month, d.day) < (month, day):
            return sign
    return "Capricorn"


@tool
def get_today() -> str:
    """Return today's date. Use it when the prediction mentions timing."""
    return date.today().isoformat()



def build_agent():
    llm = ChatGroq(model=MODEL, temperature=0.9)
    return create_agent(
        model=llm,
        tools=[draw_tarot_card, get_zodiac_sign, get_today],
        system_prompt=SYSTEM_PROMPT,
    )


def tools_used(messages) -> list[str]:
    """List the names of tools the agent called in these messages."""
    return [
        call["name"]
        for msg in messages
        for call in (getattr(msg, "tool_calls", None) or [])
    ]