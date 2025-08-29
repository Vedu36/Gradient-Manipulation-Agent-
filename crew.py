from crewai import Crew
import json
from agents import parser, modifier, checker
from tasks import get_tasks
from tools import read_svg, write_svg

# Taking Input
user_prompt = "Change the red rectangle to have a vertical gradient from #ff0000 to #0000ff."
input_svg = read_svg("input.svg")

# Building Crew 
tasks = get_tasks(user_prompt, input_svg, parser, modifier, checker)
crew = Crew(agents=[parser, modifier, checker], tasks=tasks)

# Running the Workflow
result = crew.kickoff()

# Saved Output
write_svg("output.svg", result)

# Logs
workflow_log = {
    "user_prompt": user_prompt,
    "steps": [
        {"agent": "Gradient Parser", "task": tasks[0].description},
        {"agent": "SVG Modifier", "task": tasks[1].description},
        {"agent": "Integrity Checker", "task": tasks[2].description},
    ]
}

print("\n==== Workflow Log ====")
print(json.dumps(workflow_log, indent=2))
print("\nBefore SVG:\n", input_svg[:500])
print("\nAfter SVG:\n", result[:800])
print("\nSaved output.svg")
