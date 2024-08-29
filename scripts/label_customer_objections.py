import os
import re

# Define the categories and their labels
categories = {
    "1": "Refurbishment Quality",
    "2": "Car Issues",
    "3": "Price Issues",
    "4": "Customer Experience Issues",
    "5": "No Label",
}


def chunk_text(text: str, chunk_size: int = 2) -> list[str]:
    """Chunk the text into specified number of sentences while preserving the dialogue format."""
    # Split by speaker turns
    dialogue_entries = re.split(r"(Salesperson:|Customer:)", text)

    # Reconstruct the dialogue with speakers
    dialogue = [
        f"{dialogue_entries[i]}{dialogue_entries[i + 1]}".strip()
        for i in range(1, len(dialogue_entries) - 1, 2)
    ]

    # Chunk the dialogue into specified number of entries
    return [
        "\n".join(dialogue[i : i + chunk_size])
        for i in range(0, len(dialogue), chunk_size)
    ]


def prompt_for_labels(chunks: list[str], output_dir: str, input_filename: str) -> None:
    """Prompt user to label each chunk and save data incrementally."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    counters = {label: 1 for label in categories.values()}

    for i, chunk in enumerate(chunks):
        print(f"\nChunk {i + 1}:")
        print(chunk)
        print("\nLabels:")
        for key, value in categories.items():
            print(f"{key}. {value}")
        label = input("Enter the number of the label (or '5' for No Label): ").strip()
        if label not in categories:
            print("Invalid label. Using 'No Label' by default.")
            label = "5"

        # Create and save the labeled data incrementally
        file_path = os.path.join(
            output_dir,
            f"{categories[label].replace(' ', '_')}_{counters[categories[label]]}_{input_filename}",
        )
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(chunk)  # Write only the chunk

        # Increment the counter for the label
        counters[categories[label]] += 1


def main() -> None:
    input_file = r"transcripts/conv11.txt"  # Replace with your file path
    output_dir = r"labeled_data"  # Replace with your output directory path

    input_filename = os.path.basename(input_file)  # Extract base file name
    with open(input_file, encoding="utf-8") as file:
        text = file.read()

    chunks = chunk_text(text)
    prompt_for_labels(chunks, output_dir, input_filename)
    print("Labeled data saved.")


if __name__ == "__main__":
    main()
