"""Extract important specs as JSON from a PDF's text with an LLM.

Uses ollama directly since langchain's OllamaLLM does not yet
implement langchain's `llm.with_structured_output()`.
"""

import json
from typing import Dict, Optional

from ollama import chat
from pydantic import BaseModel, Field

with open("data/product_schema.json", "r") as f:
    schema_dict = json.load(f)


class ProductSpecs(BaseModel):
    product_name: str = Field(..., description="The name or model of the lighting product")
    specs: Dict[str, Optional[str]] = Field(..., description="A dictionary of product specifications")


def parse_spec_sheet_text(prompt: str) -> None:
    """Parse a spec sheet and validate it against schema."""
    try:
        response = chat(
            messages=[{'role': 'user', 'content': prompt}],
            model='hf.co/allenai/OLMoE-1B-7B-0125-Instruct-GGUF:Q4_K_M',
            format='json',
        )

        # Parse the JSON response using the Pydantic model
        product_info = ProductSpecs.model_validate_json(response['message']['content'])
        print(product_info)

    except Exception as e:
        print(f"An error occurred: {e}")
        if 'response' in locals() and 'message' in response and 'content' in response['message']:
            print(f"Raw response content: {response['message']['content']}")


def main():
    text_filepath = "data/spec_sheets_text/indoor/Cadiant Dynamic Skylight w-Lutron Athena Spec Sheet.txt"
    with open(text_filepath, "r") as f:
        spec_sheet_text = f.read()

    parse_prompt = f"""Please extract the lighting product specifications from the following text and
    format them as a JSON object according to the schema provided. If you're not
    sure about a field, please mark its value as 'UNK' instead of making something
    up.

    Spec Sheet Text:
    {spec_sheet_text}

    JSON Schema:
    {json.dumps(schema_dict)}
    """

    parse_spec_sheet_text(parse_prompt)


if __name__ == "__main__":
    main()
