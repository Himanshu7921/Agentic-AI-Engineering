"""
Intelligent Agent with Math and Information Tools
-------------------------------------------------

This Python module demonstrates building a LangChain agent using Google Generative AI (Gemini) 
and various utility tools. The agent can:

- Perform arithmetic operations extracted from natural language queries (addition, subtraction, multiplication, division).
- Retrieve simulated weather information for a city.
- Access predefined personal information.
- Provide random fun facts based on a query topic.

Requirements:
- Python 3.10+
- langchain-core
- langchain-google-genai
- Google Gemini API key stored in environment variable 'Gemini_APIKEY'

This script is suitable for educational purposes, serving as a reference for building 
tool-augmented LLM agents.
"""

import os
import re
import random
from langchain_core.tools import tool
from langchain_google_genai import GoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.agents import initialize_agent, Tool, AgentType, AgentExecutor

# -------------------------
# 1. Build the LLM Model
# -------------------------
def build_llm_model() -> GoogleGenerativeAI:
    """
    Initializes the Google Generative AI model (Gemini).

    Returns:
        GoogleGenerativeAI: Configured LLM instance capable of text generation.
    """
    return GoogleGenerativeAI(
        model="gemini-2.5-flash",
        api_key=os.getenv("Gemini_APIKEY"),
    )

# -------------------------
# 2. Defining Mathematical Tools 
# -------------------------

@tool
def add_from_string(query: str) -> int:
    """
    Extracts exactly two numbers from a string and returns their sum.

    Example:
        >>> add_from_string("Add 3 and 5")
        8
    """
    numbers = [int(x) for x in re.findall(r'\d+', query)]
    if len(numbers) != 2:
        raise ValueError("Provide exactly two numbers to add.")
    return numbers[0] + numbers[1]

@tool
def sub_from_string(query: str) -> int:
    """
    Extracts exactly two numbers from a string and returns their difference.

    Example:
        >>> sub_from_string("Subtract 5 from 10")
        5
    """
    numbers = [int(x) for x in re.findall(r'\d+', query)]
    if len(numbers) != 2:
        raise ValueError("Provide exactly two numbers to subtract.")
    return numbers[0] - numbers[1]

@tool
def multiply_from_string(query: str) -> int:
    """
    Extracts exactly two numbers from a string and returns their product.

    Example:
        >>> multiply_from_string("Multiply 3 and 5")
        15
    """
    numbers = [int(x) for x in re.findall(r'\d+', query)]
    if len(numbers) != 2:
        raise ValueError("Provide exactly two numbers to multiply.")
    return numbers[0] * numbers[1]

@tool
def divide_from_string(query: str) -> float:
    """
    Extracts exactly two numbers from a string and returns the division result.

    Example:
        >>> divide_from_string("Divide 15 by 3")
        5.0
    """
    numbers = [int(x) for x in re.findall(r'\d+', query)]
    if len(numbers) != 2:
        raise ValueError("Provide exactly two numbers to divide.")
    if numbers[1] == 0:
        raise ValueError("Cannot divide by zero.")
    return numbers[0] / numbers[1]

# -------------------------
# 3. Weather Information Tool
# -------------------------

@tool
def weather_information(query: str) -> str:
    """
    Returns simulated weather information for a given city.

    Example:
        >>> weather_information("London")
        "The weather in London is currently cloudy with a temperature of 15°C."
    """
    simulated_results = {
        "london": "The weather in London is currently cloudy with a temperature of 15°C.",
        "new york": "The weather in New York is sunny with a temperature of 22°C.",
        "paris": "The weather in Paris is rainy with a temperature of 18°C.",
        "tokyo": "The weather in Tokyo is partly cloudy with a temperature of 20°C.",
        "sydney": "The weather in Sydney is sunny with a temperature of 25°C.",
        "moscow": "The weather in Moscow is snowy with a temperature of -5°C.",
        "mumbai": "The weather in Mumbai is hot and sunny with a temperature of 35°C.",
        "berlin": "The weather in Berlin is windy with a temperature of 16°C.",
        "rio de janeiro": "The weather in Rio de Janeiro is humid with a temperature of 28°C.",
        "cape town": "The weather in Cape Town is clear with a temperature of 19°C.",
        "unknowncity": "No specific information found, but the topic seems interesting."
    }
    return simulated_results.get(query.lower(), simulated_results["unknowncity"])

# -------------------------
# 4. Personal Info Tool
# -------------------------

@tool
def personal_info(query: str) -> str:
    """
    Returns predefined personal information for a specified individual.

    Example:
        >>> personal_info("himanshu")
        "Name: Himanshu Singh, Age: 19, Hobby: Painting, ..."
    """
    personal_info_details = {
        "himanshu": {
            "name": "Himanshu Singh",
            "age": "19",
            "favorite color": "Blue",
            "hobby": "Painting",
            "city": "New Delhi",
            "favorite food": "Pizza",
            "pet": "Dog",
            "profession": "Student",
            "language": "English",
            "sports": "Football"
        },
        "priya": {
            "name": "Priya Sharma",
            "age": "21",
            "favorite color": "Pink",
            "hobby": "Reading",
            "city": "Mumbai",
            "favorite food": "Pasta",
            "pet": "Cat",
            "profession": "Designer",
            "language": "Hindi",
            "sports": "Badminton"
        },
        "rahul": {
            "name": "Rahul Verma",
            "age": "22",
            "favorite color": "Green",
            "hobby": "Photography",
            "city": "Bangalore",
            "favorite food": "Biryani",
            "pet": "Parrot",
            "profession": "Engineer",
            "language": "English",
            "sports": "Cricket"
        }
    }
    return personal_info_details.get(query.lower(), f"No information available for '{query}'.")

# -------------------------
# 5. Random Fun Fact Tool
# -------------------------

@tool
def random_funfact(query: str) -> str:
    """
    Provides a random fun fact based on the query topic.

    Example:
        >>> random_funfact("space")
        "Venus is the hottest planet in our solar system, even hotter than Mercury."
    """
    fun_facts = {
        "space": [
            "Venus is the hottest planet in our solar system, even hotter than Mercury.",
            "A day on Venus is longer than a year on Venus.",
            "There are more stars in the universe than grains of sand on Earth."
        ],
        "animals": [
            "A group of flamingos is called a 'flamboyance'.",
            "Octopuses have three hearts and blue blood.",
            "Sloths can hold their breath longer than dolphins."
        ],
        "history": [
            "Napoleon was once attacked by a horde of bunnies.",
            "The Great Fire of London destroyed over 13,000 homes in 1666.",
            "Cleopatra lived closer in time to the moon landing than to the building of the Great Pyramid."
        ],
        "general": [
            "Honey never spoils. Archaeologists found edible honey in ancient Egyptian tombs.",
            "Bananas are berries, but strawberries are not.",
            "There are more possible iterations of chess than atoms in the universe."
        ]
    }
    category = query.lower() if query.lower() in fun_facts else "general"
    return random.choice(fun_facts[category])

# -------------------------
# 6. Tool Registration
# -------------------------

def get_tools() -> list[Tool]:
    """
    Returns a list of all LangChain tools for agent usage.
    """
    return [
        Tool.from_function(func = add_from_string, name = "add_two_numbers",
                           description = "Extracts two numbers from a string and returns their sum."),
        Tool.from_function(func = sub_from_string, name = "sub_two_numbers",
                           description = "Extracts two numbers from a string and returns their difference."),
        Tool.from_function(func = multiply_from_string, name = "multiply_two_numbers",
                           description = "Extracts two numbers from a string and returns their product."),
        Tool.from_function(func = divide_from_string, name = "divide_two_numbers",
                           description = "Extracts two numbers from a string and returns the division result."),
        Tool.from_function(func = weather_information, name = "weather_information_tool",
                           description = "Provides current weather information for a given city."),
        Tool.from_function(func = personal_info, name = "personal_info_tool",
                           description = "Returns detailed personal information about a specified individual."),
        Tool.from_function(func = random_funfact, name = "random_funfact_tool",
                           description = "Generates a random fun fact based on a query topic.")
    ]

# -------------------------
# 7. Initialize Agent
# -------------------------

def get_agent_executor(llm: GoogleGenerativeAI, tools: list[Tool]) -> AgentExecutor:
    """
    Initializes a LangChain agent executor using the provided LLM and tools.
    """
    return initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True
    )

# -------------------------
# 8. Main Execution
# -------------------------

def main():
    query = "Tell me a fun fact about the city I live in, Mumbai."
    llm = build_llm_model()
    tools = get_tools()
    agent = get_agent_executor(llm, tools)
    response = agent.invoke({"input": query})
    print(response['output'])

if __name__ == "__main__":
    main()