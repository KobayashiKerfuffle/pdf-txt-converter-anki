import PyPDF2
import os
import re

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        # Initialize PDF reader
        pdf = PyPDF2.PdfReader(file)
        
        # Extract title from metadata
        title = pdf.metadata["/Title"] if "/Title" in pdf.metadata else "Unknown Title"

        # Initialize text variable for concatenated content
        text = ""
        
        # Loop through all the pages and extract text
        for page in pdf.pages:
            text += page.extract_text()

    return title, text

def process_and_split_text(title, extracted_text, output_directory, char_limit=8000):
    # Retain only alphanumeric characters, spaces, and periods in the extracted text
    extracted_text = re.sub(r'[^a-zA-Z0-9]', '', extracted_text)

    # Subtracting the standard_prompt length from the char_limit for splitting
    actual_limit = char_limit

    # Splitting the text into chunks that don't exceed the char_limit
    chunks = [extracted_text[i:i+actual_limit] for i in range(0, len(extracted_text), actual_limit)]

    # Save each chunk to a separate text file
    for idx, chunk in enumerate(chunks):
        standard_prompt = (
            f"Role: Expert Anki flashcard engineer, specializing in educational psychology and pedagogical best practices.\n\n Instruction: Analyze the content from the textbook titled '{title}', this is Part {idx + 1} of {len(chunks)}. Transform the vital concepts into Anki cards suitable for optimal retention and recall.\n\n" 
            "General Card Creation Guidelines:\n 1. Hierarchy of Information: Extract core ideas first. Dive into supporting details only if they provide critical context.\n 2. Relevance: Prioritize facts, processes, or concepts that have broad implications or are foundational for understanding other topics.\n 3. Avoid Cognitive Overload: A card should represent a singular, digestible piece of information.\n 4. Repetition: Repetitive concepts should be condensed into singular, impactful cards.\n 5. Special Note on Ambiguity: Ambiguous questions lead to frustration during review. Ensure the answer to a card is unambiguous based on the question provided.\n\n Choosing Between Basic and Cloze Cards:\n 1. Use basic cards for straightforward, fact-based information or definitions.\n 2. Opt for cloze cards for processes, sequences, or multi-layered information.\n 3. Choose basic cards for recognition-based recall (e.g., "'What is X?'").\n 4. Use cloze cards for completion-based recall (filling in a missing piece of info).\n 5. Basic cards are ideal for single-layered info without depth.\n 6. Cloze cards handle multi-layered or contextual information effectively.\n 7. Create both card types for information approachable from multiple valuable perspectives, but avoid redundancy.\n 8. Mix card types to maintain learner engagement and challenge.\n\n Basic Cards Guidelines:\n 1. Structure: Use the pipe character (|) to separate question from answer.\n 2. Concision: Aim for brevity without sacrificing clarity.\n 3. Relevance: Rank cards based on their significance and sequence in the content.\n 4. Complex Ideas: For challenging concepts, break them into multiple basic cards.\n 5. Format: question|answer\n 6. Example of a good basic card: What is photosynthesis?|A process where plants convert sunlight into food.\n 7. Example of a bad basic card: What is photosynthesis, and list its types?|A complex process where plants make food using sunlight. Types include X, Y, Z.\n\n Instructions for creating Cloze Cards:\n 1. Clues: Use contextual clues to hint at the cloze deletion.\n 2. Unique Identifiers: Each cloze deletion should have a unique identifier, even if they are in the same card. Use {{c1::}}, {{c2::}}, {{c3::}}, and so on. Example: The sun is {{c1::hot}} and the moon is {{c2::cold}}.\n 3. Single Deletion: As a general guideline, prefer one cloze deletion per card. However, multiple deletions can be used if they provide contextual or complementary information, ensuring each has a unique identifier.\n 4. Example of a good cloze card: The sun provides {{c1::heat}} while the moon affects {{c2::tides}}.\n 5. Example of a bad cloze card: The {{c1::sun}} provides {{c1::heat}} while the moon affects tides.\n\n Output Instructions:\n 1. Render the cards directly in code block format - one code block for basic cards and another code block for cloze cards.\n 2. Do not output any other text than the cards themselves (eg: titles or list numbers).\n 3. Eschew quotation marks in the output.\n\n Text Content for Analysis:\n\n"
        )

        # Writing the standard prompt and chunk to the output file
        with open(os.path.join(output_directory, f'output_{idx+1}.txt'), 'w', encoding='utf-8') as output_file:
            output_file.write(standard_prompt + chunk)

# Directory where the PDF file will be put
pdf_directory = os.path.join(SCRIPT_DIR, 'pdf_path')
pdf_file_name = next((file for file in os.listdir(pdf_directory) if file.endswith('.pdf')), None)

# If a PDF file is found in the directory, process it; otherwise, print an error
if pdf_file_name:
    pdf_path = os.path.join(pdf_directory, pdf_file_name)
    title, extracted_text = extract_text_from_pdf(pdf_path)

    # Directory to save the split files
    output_dir = os.path.join(SCRIPT_DIR, "output_files")
    process_and_split_text(title, extracted_text, output_dir)
else:
    print("No PDF file found in 'pdf_path' directory.")
