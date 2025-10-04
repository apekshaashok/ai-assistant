import time
import random
from datetime import datetime
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langchain.tools import tool
from langgraph.prebuilt import create_react_agent

load_dotenv()

# ----------------- TOOLS -----------------

@tool
def calculator(a: float, b: float) -> str:
    """Perform basic arithmetic calculations."""
    print("Tool has been called.")
    return f"The sum of {a} and {b} is {a + b}."

@tool
def say_hello(name: str) -> str:
    """Greet a user."""
    print("Tool has been called.")
    return f"Hello {name}! Hope you're having a wonderful day 🌟"

@tool
def tell_time() -> str:
    """Tell the current date and time."""
    print("Tool has been called.")
    now = datetime.now()
    return f"It's {now.strftime('%I:%M %p')} on {now.strftime('%A, %B %d, %Y')}."

@tool
def weather(city: str) -> str:
    """Mock weather report for fun."""
    print("Tool has been called.")
    conditions = ["sunny", "rainy", "cloudy", "stormy", "foggy", "clear"]
    temp = random.randint(20, 35)
    return f"The weather in {city} is {random.choice(conditions)} with about {temp}°C."

@tool
def tell_joke() -> str:
    """Tells a random light-hearted joke."""
    print("Tool has been called.")
    jokes = [
        "Why don’t skeletons fight each other? They don’t have the guts.",
        "Why do Java developers wear glasses? Because they don’t C#!",
        "Why did the computer show up at work late? It had a hard drive.",
        "Parallel lines have so much in common... it’s a shame they’ll never meet.",
    ]
    return random.choice(jokes)

@tool
def quote_generator() -> str:
    """Returns a random inspirational quote."""
    print("Tool has been called.")
    quotes = [
        "Believe you can and you're halfway there.",
        "You are stronger than you think.",
        "The best time to start was yesterday. The next best time is now.",
        "Keep going — every step counts.",
        "Do what you can, with what you have, where you are.",
    ]
    return random.choice(quotes)

@tool
def coin_toss() -> str:
    """Simulate tossing a coin."""
    print("Tool has been called.")
    return f"It's {random.choice(['Heads', 'Tails'])}!"

@tool
def dice_roll() -> str:
    """Simulate rolling a dice."""
    print("Tool has been called.")
    return f"You rolled a {random.randint(1, 6)} 🎲"

@tool
def mood_encouragement(mood: str) -> str:
    """Give encouragement based on mood."""
    print("Tool has been called.")
    mood = mood.lower()
    responses = {
        "sad": "It's okay to feel sad sometimes 💙. Remember, this feeling will pass and you're doing your best.",
        "tired": "You’ve done a lot today. Rest is productive too — take it easy 🌙.",
        "happy": "That's awesome! Keep shining and spreading good vibes 🌞.",
        "angry": "Take a deep breath. You deserve peace — not stress ❤️.",
        "anxious": "You’re safe, you’re loved, and you’ve got this 💫.",
    }
    return responses.get(mood, "Whatever you’re feeling, it’s valid. You’re doing great 🤍.")

@tool
def unit_converter(value: float, from_unit: str, to_unit: str) -> str:
    """Convert between cm/m/km, g/kg, and °C/°F."""
    print("Tool has been called.")
    from_unit, to_unit = from_unit.lower(), to_unit.lower()

    # Length conversions
    if from_unit == "cm" and to_unit == "m":
        return f"{value} cm = {value / 100} m"
    elif from_unit == "m" and to_unit == "cm":
        return f"{value} m = {value * 100} cm"
    elif from_unit == "m" and to_unit == "km":
        return f"{value} m = {value / 1000} km"
    elif from_unit == "km" and to_unit == "m":
        return f"{value} km = {value * 1000} m"

    # Weight conversions
    elif from_unit == "g" and to_unit == "kg":
        return f"{value} g = {value / 1000} kg"
    elif from_unit == "kg" and to_unit == "g":
        return f"{value} kg = {value * 1000} g"

    # Temperature conversions
    elif from_unit == "c" and to_unit == "f":
        return f"{value}°C = {(value * 9/5) + 32}°F"
    elif from_unit == "f" and to_unit == "c":
        return f"{value}°F = {(value - 32) * 5/9}°C"

    else:
        return "Sorry, I can't convert between those units yet."

@tool
def timer(seconds: int) -> str:
    """Start a simple countdown timer."""
    print("Tool has been called.")
    for i in range(seconds, 0, -1):
        print(f"⏳ {i} seconds left...", end="\r")
        time.sleep(1)
    return "⏰ Time’s up!"

# ----------------- MAIN -----------------
def main():
    model = ChatOpenAI(temperature=0)
    tools = [
        calculator, say_hello, tell_time, weather, tell_joke, quote_generator,
        coin_toss, dice_roll, mood_encouragement, unit_converter, timer
    ]
    agent_executor = create_react_agent(model, tools)

    print("👋 Hi, I’m your assistant! Type 'help' to see what I can do, or 'quit' to exit.")

    while True:
        user_input = input("\nYou: ").strip().lower()

        if user_input == "quit":
            print("Goodbye! Take care 💖")
            break

        elif user_input == "help":
            print("\n✨ I can do the following:")
            print(" - say hello <your name>")
            print(" - calculate <a> + <b>")
            print(" - tell me the time/date")
            print(" - weather in <city>")
            print(" - tell me a joke")
            print(" - give me a quote")
            print(" - toss a coin / roll a dice")
            print(" - encouragement for <mood>")
            print(" - convert <value> <from_unit> to <to_unit>")
            print(" - start timer for <seconds>")
            continue

        print("\nAssistant: ", end="")
        try:
            for chunk in agent_executor.stream({"messages": [HumanMessage(content=user_input)]}):
                if "agent" in chunk and "messages" in chunk["agent"]:
                    for message in chunk["agent"]["messages"]:
                        print(message.content, end="")
            print()
        except Exception as e:
            print("Sorry, something went wrong:", e)

if __name__ == "__main__":
    main()
