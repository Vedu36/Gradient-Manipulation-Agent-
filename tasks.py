from crewai import Task

def get_tasks(user_prompt, input_svg, parser, modifier, checker):
    parse_task = Task(
        description=f"Parse this instruction: '{user_prompt}'",
        agent=parser,
        expected_output="JSON with gradient_type, direction, stops [{offset,color}], and target element."
    )

    modify_task = Task(
        description="Using the parsed JSON config, modify this SVG:\n" + input_svg,
        agent=modifier,
        expected_output="Updated SVG with gradient defs and modified fills."
    )

    check_task = Task(
        description="Check the updated SVG for correctness and gradient reference validity.",
        agent=checker,
        expected_output="A valid SVG or suggestions for fixes."
    )

    return [parse_task, modify_task, check_task]
