import os
from pdfminer.high_level import extract_text
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set API Key
api_key = os.getenv("OPENAI_API_KEY")

# Ensure API key is available
if not api_key:
    raise ValueError("API Key not found. Check your .env file or system variables.")

# OpenAI Client
client = OpenAI(api_key=api_key)

# Function to convert PDF to text
def pdf_to_text(pdf_path):
    """Converts a PDF file to text and saves it as a .txt file in the same directory."""
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")
    
    text = extract_text(pdf_path)
    
    # Generate corresponding .txt filename
    txt_filename = os.path.splitext(os.path.basename(pdf_path))[0] + ".txt"
    txt_path = os.path.join(os.path.dirname(pdf_path), txt_filename)
    
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(text)
    
    return txt_path  # Return the text file path

# Function to read a text file
def read_text_file(file_path):
    """Reads the content of a text file."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

# Define file paths
pdf_path = r"C:\masterp\uvm_project\example_files\DesignSpecificationDocument.pdf"
system_prompt_path = r"C:\masterp\uvm_project\system_prompts\p1.txt"

# Convert PDF to text
txt_path = pdf_to_text(pdf_path)

# Read the extracted design document
design_doc1 = read_text_file(txt_path)
print("Design document loaded successfully.")

# Read the system prompt
system_prompt1 = read_text_file(system_prompt_path)
print("System prompt loaded successfully.")

# Set OpenAI model
model = "gpt-4o-mini"

# Call OpenAI API
completion = client.chat.completions.create(
    model=model,
    messages=[
        {"role": "system", "content": system_prompt1},
        {"role": "user", "content": design_doc1}
    ]
)

# Extract LLM response
content = completion.choices[0].message.content

# Define output filename based on the PDF name
output_filename = f"test_cases_{os.path.splitext(os.path.basename(pdf_path))[0]}.txt"

# Save LLM-generated content
with open(output_filename, "w", encoding="utf-8") as f:
    f.write(content)

print(f"Output saved to {output_filename}")
