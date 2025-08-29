
# For loading the input file
def read_svg(file_path: str) -> str:
    with open(file_path, "r") as f:
        return f.read()

# For loading the input file
def write_svg(file_path: str, content: str):
    with open(file_path, "w") as f:
        f.write(content)


import json

# This function is for validating JSON content
def json_validator(content: str):
    """Check if response is valid JSON, return parsed or error."""
    try:
        return json.loads(content)
    except json.JSONDecodeError as e:
        return {"error": f"Invalid JSON: {str(e)}"}



import xml.etree.ElementTree as ET
from crewai_tools import BaseTool
from typing import Dict, Any

class ApplyGradientTool(BaseTool):
    name: str = "apply_gradient"
    description: str = "Apply gradient config to an SVG string."

    def _run(self, svg_content: str, config: Dict[str, Any]) -> str:
        root = ET.fromstring(svg_content)

        # Creating <defs> if missing
        defs = root.find("{http://www.w3.org/2000/svg}defs")
        if defs is None:
            defs = ET.SubElement(root, "defs")

        grad_id = "grad1"

        # For Linear Gradient
        if config.get("gradient_type") == "linear":
            grad = ET.SubElement(defs, "linearGradient", id=grad_id)
            if config.get("direction") == "vertical":
                grad.attrib.update({"x1": "0%", "y1": "0%", "x2": "0%", "y2": "100%"})
            else:  # For horizontal
                grad.attrib.update({"x1": "0%", "y1": "0%", "x2": "100%", "y2": "0%"})

        # ForRadial Gradient
        elif config.get("gradient_type") == "radial":
            grad = ET.SubElement(defs, "radialGradient", id=grad_id)
            grad.attrib.update({"cx": "50%", "cy": "50%", "r": "50%"})

        # Adding color stops
        for stop in config.get("stops", []):
            ET.SubElement(
                grad, "stop",
                offset=stop["offset"],
                style=f"stop-color:{stop['color']}; stop-opacity:1"
            )

        # Updating target elements
        target_shape = config.get("target_shape", "*") 
        target_color = config.get("target_color")

        for elem in root.findall(f".//{{http://www.w3.org/2000/svg}}{target_shape}"):
            if target_color is None or elem.get("fill") == target_color:
                elem.set("fill", f"url(#{grad_id})")

        return ET.tostring(root, encoding="unicode")

