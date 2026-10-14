# fortune-teller 🔮

Madame Mystica is an AI fortune-teller agent built with [LangChain](https://www.langchain.com/) and a model hosted on [Groq](https://groq.com/). She answers questions about the future, drawing tarot cards and reading zodiac signs along the way.

Available as an interactive terminal chat and as an HTTP API packaged in a Docker container.

## How it works

The agent decides on its own when to call these tools:

| Tool | Description |
|------|-------------|
| `draw_tarot_card` | Draws a random Major Arcana card, upright or reversed |
| `get_zodiac_sign` | Returns the zodiac sign for a birth date (`YYYY-MM-DD`) |
| `get_today` | Returns today's date |

## Project structure

```
agent.py           # System prompt, tools and agent factory
fortune_teller.py  # Interactive terminal chat
api.py             # HTTP API (FastAPI)
Dockerfile         # Container image for the API
requirements.txt   # Python dependencies
```

## Setup

Requires Python 3.10+ and a [Groq API key](https://console.groq.com/keys).

```bash
git clone https://github.com/chabrowa/fortune-teller.git
cd fortune-teller
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file in the project root:

```
GROQ_API_KEY=your_key_here
GROQ_MODEL=openai/gpt-oss-20b
```

## Usage

### Terminal chat

```bash
python fortune_teller.py
```

### HTTP API

```bash
uvicorn api:app --reload
```

Interactive API docs are available at http://localhost:8000/docs.

Example request:

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"question": "Will I travel next year?"}'
```

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/predict` | Returns a prediction and the list of tools used |
| `GET` | `/health` | Liveness check |

### Docker

```bash
docker build -t fortune-teller .
docker run --rm -p 8000:8000 --env-file .env fortune-teller
```