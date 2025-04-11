def load_prompt(filepath: str) -> str:
    with open(filepath, "r") as f:
        return f.read()
