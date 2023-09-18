# PDF to GPT-4 Prompt Converter for Anki Cards

This script provides functionality to extract text from PDF files, preprocess the extracted text, and convert it into suitable prompts that can be fed to GPT-4 for generating Anki flashcards.

## Requirements

- Python 3.6+
- PyPDF2 library (`pip install PyPDF2`)

## Overview

1. **Text Extraction from PDF**: The text is extracted from the provided PDF file.
2. **Text Preprocessing**: The extracted text is cleaned up to retain only alphanumeric characters, spaces, and periods. The text is then split into manageable chunks.
3. **Prompt Creation**: For each chunk of text, a prompt is created to instruct GPT-4 on generating Anki cards from the content. These prompts contain guidelines on how the cards should be structured, criteria for information inclusion, and some examples.

## How to Use

1. Place your PDF file in the `pdf_path` directory.
2. Run the script.
3. Once executed, prompts suitable for GPT-4 will be generated and saved into the `output_files` directory.

## Key Functions

- `extract_text_from_pdf(pdf_path)`: This function reads the PDF file and extracts its text content. It also fetches the title of the PDF for context.
- `process_and_split_text(title, extracted_text, output_directory, char_limit=8000)`: After cleaning and preprocessing the extracted text, this function divides the text into chunks and appends the standard prompt before each chunk. The processed text is then saved into individual text files for feeding to GPT-4.

## Notes

- Ensure the `pdf_path` directory contains only the desired PDF file. If there are multiple PDF files, only one will be processed.
- The character limit for each chunk is set to 8000 by default, but this can be adjusted based on requirements.
- The generated prompts contain guidelines for both basic and cloze Anki card types.

## Troubleshooting

If you encounter a message stating "No PDF file found in 'pdf_path' directory", ensure that the PDF file is correctly placed in the specified directory and that the file extension is `.pdf`.
