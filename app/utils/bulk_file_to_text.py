import csv
from io import StringIO


def bulk_file_to_text(file_bytes: bytes, delimiter: str) -> list[str]:
    # Convert bytes to string
    content = file_bytes.decode("utf-8")

    # Determine if the file is a CSV or text file and process accordingly
    if delimiter in content:
        # Handle CSV or delimited text
        result = []
        reader = csv.reader(StringIO(content), delimiter=delimiter)
        for row in reader:
            result.extend(row)
        return result
    # Handle plain text
    return [content]
