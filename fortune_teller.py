"""Interactive terminal chat with the fortune-teller agent."""


from langchain_core.messages import HumanMessage

from agent import build_agent, tools_used


def main() -> None:
    agent = build_agent()
    history = []
    print("🔮 Madame Mystica is ready. Ask about your future (type 'quit' to leave).\n")

    while True:
        question = input("You: ").strip()
        if not question:
            continue
        if question.lower() in {"quit", "exit"}:
            print("\n🔮 Madame Mystica: The stars will be waiting for you. Farewell!")
            break

        history.append(HumanMessage(content=question))
        result = agent.invoke({"messages": history})
        new_messages = result["messages"][len(history):]
        history = result["messages"]

        for name in tools_used(new_messages):
            print(f"   ✨ [tool] {name}")

        print(f"\n🔮 Madame Mystica: {history[-1].content}\n")


if __name__ == "__main__":
    main()