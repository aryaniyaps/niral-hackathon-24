import json
from io import BytesIO
from typing import Any

import gradio as gr

from app.constants import InputType
from app.extract_data import extract_data
from app.utils.bulk_file_to_text import bulk_file_to_text
from app.utils.pdf_to_text import pdf_bytes_to_text, pdf_ocr_to_text
from app.utils.save_temp_file import save_to_temp_file

gr.set_static_paths(paths=["../public/"])


def extract_from_text(text_input: str) -> list[str | gr.DownloadButton]:
    extracted_data = extract_data(audio_transcript=text_input)
    output = extracted_data.model_dump_json(indent=4)
    return [
        gr.JSON(output),
        gr.DownloadButton(
            label="Download JSON Output",
            value=save_to_temp_file(output),
            interactive=True,
        ),
    ]


def extract_from_pdf(
    file_input: bytes, perform_ocr: bool
) -> list[str | gr.DownloadButton]:
    content = (
        pdf_ocr_to_text(pdf_bytes=file_input)
        if perform_ocr
        else pdf_bytes_to_text(pdf_bytes=file_input)
    )
    extracted_data = extract_data(audio_transcript=content)
    output = extracted_data.model_dump_json(indent=4)
    return [
        output,
        gr.DownloadButton(
            label="Download JSON Output",
            value=save_to_temp_file(output),
            interactive=True,
        ),
    ]


def extract_from_bulk_csv(
    file_input: bytes, delimiter: str
) -> list[str | gr.DownloadButton]:
    contents = bulk_file_to_text(file_bytes=file_input, delimiter=delimiter)
    # serial execution - change to parallel if needed
    extracted_data = [
        extract_data(audio_transcript=audio_transcript) for audio_transcript in contents
    ]
    output = json.dumps(extracted_data, indent=4)
    return [
        output,
        gr.DownloadButton(
            label="Download JSON Output",
            value=output,
            interactive=True,
        ),
    ]


# Creating Gradio Interface
with gr.Blocks(
    title="Car Sales Transcript Extractor", css="footer {visibility: hidden}"
) as demo:
    gr.Markdown("## Car Sales Transcript Extractor")
    input_type = gr.Radio(
        choices=[InputType.TEXT, InputType.PDF, InputType.BULK],
        label="Select Transcript Upload Type",
        value=InputType.TEXT,
    )
    text_input = gr.Textbox(
        label="Enter Transcript:",
        lines=12,
        visible=True,
        key="text_input",
    )

    file_input = gr.File(
        label="Upload PDF file:",
        file_types=[".pdf"],
        visible=False,
        key="pdf_upload_input",
        type="binary",
    )

    bulk_input = gr.File(
        label="Upload bulk file:",
        file_types=[".csv", ".txt"],
        visible=False,
        key="bulk_upload_input",
        type="binary",
    )

    # Hidden OCR checkbox, initially hidden
    perform_ocr_field = gr.Checkbox(
        value=False,
        label="Perform OCR",
        visible=False,
        interactive=True,
    )

    # Hidden delimiter text field, initially hidden
    delimiter_field = gr.Textbox(
        label="Transcript Delimiter",
        max_lines=1,
        visible=False,
        interactive=True,
        value=",",
    )

    generate_button = gr.Button(
        "Extract from transcript",
        interactive=False,
        variant="primary",
    )

    # Show the correct input field based on the radio button selection
    def render_input_box(selected_input: InputType) -> list[dict[str, Any]]:
        match selected_input:
            case InputType.TEXT:
                return [
                    gr.update(visible=True),
                    gr.update(visible=False),
                    gr.update(visible=False),
                    gr.update(visible=False),  # Delimiter hidden
                    gr.update(visible=False),  # Perform OCR hidden
                    gr.update(value="Extract from transcript"),  # Change button text
                ]
            case InputType.PDF:
                return [
                    gr.update(visible=False),
                    gr.update(visible=True),
                    gr.update(visible=False),
                    gr.update(visible=False),  # Delimiter hidden
                    gr.update(visible=True),  # Perform OCR visible
                    gr.update(value="Extract from transcript"),  # Change button text
                ]
            case InputType.BULK:
                return [
                    gr.update(visible=False),
                    gr.update(visible=False),
                    gr.update(visible=True),
                    gr.update(visible=True),  # Delimiter visible
                    gr.update(visible=False),  # Perform OCR hidden
                    gr.update(value="Extract from transcripts"),  # Change button text
                ]

    input_type.change(
        fn=render_input_box,
        inputs=input_type,
        outputs=[
            text_input,
            file_input,
            bulk_input,
            delimiter_field,
            perform_ocr_field,
            generate_button,
        ],
    )

    # Enable/disable button and radio based on input state
    def update_button_and_radio_interactivity(
        text: str | None, pdf_file: BytesIO | None, bulk_file: BytesIO | None
    ) -> tuple[dict[str, Any], dict[str, Any]]:
        # Check if any input has a value
        is_interactive = bool(text or pdf_file or bulk_file)
        return (
            gr.update(interactive=is_interactive),  # For button
            gr.update(interactive=not is_interactive),  # For radio buttons
        )

    # Call the function when any input changes
    text_input.change(
        fn=update_button_and_radio_interactivity,
        inputs=[text_input, file_input, bulk_input],
        outputs=[generate_button, input_type],
    )
    file_input.change(
        fn=update_button_and_radio_interactivity,
        inputs=[text_input, file_input, bulk_input],
        outputs=[generate_button, input_type],
    )
    bulk_input.change(
        fn=update_button_and_radio_interactivity,
        inputs=[text_input, file_input, bulk_input],
        outputs=[generate_button, input_type],
    )

    output_json = gr.JSON(label="Extracted data", scale=1, show_indices=False)
    download_button = gr.DownloadButton(
        label="Download JSON Output", interactive=False
    )  # Initially hidden

    # Button click handler
    generate_button.click(
        fn=lambda text=None,
        pdf_file=None,
        perform_ocr_field=None,
        bulk_file=None,
        delimiter=None: extract_from_text(text)
        if text
        else extract_from_pdf(pdf_file, perform_ocr=perform_ocr_field)
        if pdf_file
        else extract_from_bulk_csv(bulk_file, delimiter=delimiter),
        inputs=[
            text_input,
            file_input,
            perform_ocr_field,
            bulk_input,
            delimiter_field,
        ],
        outputs=[output_json, download_button],
    )

if __name__ == "__main__":
    # Launch the Gradio app
    demo.launch(favicon_path="public/favicon.ico", inbrowser=True, show_api=False)
