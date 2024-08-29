import tempfile


def save_to_temp_file(content: str) -> str:
    # Create a temporary file to store the content
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".json", mode="w")
    temp_file.write(content)
    temp_file.close()
    return temp_file.name
