from crewai import Agent, LLM
import os
from dotenv import load_dotenv
from tools import json_validator, ApplyGradientTool
load_dotenv()

llm = LLM(
    model="groq/llama-3.1-70b-versatile",
    temperature=0.7,
    api_key=os.getenv("GROQ_API_KEY")
)
# The parser agent
modifier = Agent(
    role="SVG Modifier Agent",
    goal="Insert gradient <defs> and update SVG elements based on the parsed config.",
    backstory="Specialist in editing SVG files and applying gradient fills correctly.",
    llm=llm,
    verbose=True,
    tools=[ApplyGradientTool()]  
)
# The modifier agent
modifier = Agent(
    role="SVG Modifier Agent",
    goal="Insert gradient <defs> and update SVG elements based on the parsed config.",
    backstory="Specialist in editing SVG files and applying gradient fills correctly.",
    llm=llm,
    verbose=True,
    tools=[json_validator]  
)
# The checker agent
checker = Agent(
    role="Integrity Checker Agent",
    goal="Validate that the SVG is well-formed and gradients are properly referenced.",
    backstory="Ensures that the final output is valid and renders correctly.",
    llm=llm,
    verbose=True,
    tools=[]
)
