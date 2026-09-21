import ollama
from pypdf import PdfReader

# Configuration
pdf_path = "form8_response.pdf"
output_md_path = "form8_response.md"
model_name = "gpt-oss:20b"

def pdf_to_markdown(pdf_path, output_path):
    reader = PdfReader(pdf_path)
    markdown_content = []

    print(f"Starting conversion of {len(reader.pages)} pages using {model_name}...")

    for i, page in enumerate(reader.pages):
        raw_text = page.extract_text()
        
        # Skip empty pages
        if not raw_text.strip():
            continue
            
        print(f"Processing page {i+1}...")

        # Construct the prompt for gpt-oss
        prompt = f"""
        You are an expert document formatter. Convert the following raw text extracted from page {i+1} of a PDF into clean, standard Markdown.
        
        Rules:
        1. Maintain the structural layout (headers, bullet points, paragraphs, tables).
        2. Clean up any broken lines, hyphenations, or bad formatting artifacts caused by PDF extraction.
        3. Do not add any conversational filler, intro, or outro text. Output ONLY the raw Markdown.

        Raw Text:
        {raw_text}
        """

        # Call local Ollama instance
        response = ollama.generate(
            model=model_name,
            prompt=prompt,
            options={"temperature": 0.2} # Low temperature for accurate reconstruction
        )
        
        page_md = response['response']
        markdown_content.append(page_md)

    # Save to file
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n\n".join(markdown_content))
        
    print(f"Success! Saved Markdown file to: {output_path}")

if __name__ == "__main__":
    pdf_to_markdown(pdf_path, output_md_path)
