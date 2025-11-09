# # utils/equation_extractor.py

# import os
# import re
# import fitz  # PyMuPDF
# import base64
# import requests
# from openai import OpenAI

# # Initialize OpenAI client (or replace with local model)
# openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# MATHPIX_API_URL = "https://api.mathpix.com/v3/text"
# MATHPIX_APP_ID = os.getenv("MATHPIX_APP_ID")
# MATHPIX_APP_KEY = os.getenv("MATHPIX_APP_KEY")

# def extract_images_from_pdf(pdf_path):
#     """Extracts images from PDF pages to detect equations visually."""
#     doc = fitz.open(pdf_path)
#     images = []
#     for page_index, page in enumerate(doc):
#         for img_index, img in enumerate(page.get_images(full=True)):
#             xref = img[0]
#             pix = fitz.Pixmap(doc, xref)
#             if pix.n < 5:  # Not CMYK
#                 image_bytes = pix.tobytes("png")
#                 images.append((page_index, base64.b64encode(image_bytes).decode("utf-8")))
#             pix = None
#     return images


# def call_mathpix_api(image_base64):
#     """Send image to Mathpix for LaTeX equation detection."""
#     headers = {
#         "app_id": MATHPIX_APP_ID,
#         "app_key": MATHPIX_APP_KEY,
#         "Content-type": "application/json",
#     }

#     payload = {
#         "src": f"data:image/png;base64,{image_base64}",
#         "formats": ["latex_styled", "text"],
#         "data_options": {"include_asciimath": True, "include_latex": True},
#     }

#     response = requests.post(MATHPIX_API_URL, headers=headers, json=payload)
#     response.raise_for_status()
#     data = response.json()

#     return data.get("latex_styled") or data.get("latex_normalized")


# def extract_equations_from_text(text):
#     """Fallback regex-based LaTeX equation extraction (for text PDFs)."""
#     equation_pattern = re.compile(r"(\$\$.*?\$\$|\$.*?\$|\\\[.*?\\\]|\\\(.*?\\\))", re.DOTALL)
#     equations = equation_pattern.findall(text)
#     return list(set(equations))  # Remove duplicates


# def explain_equation_with_llm(equation_latex):
#     """Ask an LLM to explain the equation meaning."""
#     prompt = f"""
#     Explain the following equation in plain language, identifying what it represents and defining each variable:
#     Equation: {equation_latex}
#     """

#     response = openai_client.chat.completions.create(
#         model="gpt-4-turbo",
#         messages=[{"role": "user", "content": prompt}],
#         temperature=0.3,
#     )

#     return response.choices[0].message.content.strip()


# def extract_equations(pdf_path: str):
#     """
#     Full pipeline:
#     1. Extract text-based equations (LaTeX)
#     2. Extract image-based equations (via Mathpix)
#     3. Get LLM-based explanations
#     """

#     # Step 1: Extract text
#     doc = fitz.open(pdf_path)
#     text = ""
#     for page in doc:
#         text += page.get_text()

#     text_equations = extract_equations_from_text(text)

#     # Step 2: Extract image equations
#     images = extract_images_from_pdf(pdf_path)
#     image_equations = []
#     for _, img_b64 in images:
#         try:
#             eq_latex = call_mathpix_api(img_b64)
#             if eq_latex:
#                 image_equations.append(eq_latex)
#         except Exception:
#             continue

#     all_equations = list(set(text_equations + image_equations))

#     # Step 3: Generate explanations via LLM
#     structured_output = []
#     for eq in all_equations:
#         try:
#             explanation = explain_equation_with_llm(eq)
#             structured_output.append({
#                 "latex": eq,
#                 "explanation": explanation
#             })
#         except Exception as e:
#             structured_output.append({
#                 "latex": eq,
#                 "explanation": f"Error explaining equation: {e}"
#             })

#     return structured_output




# utils/equation_extractor.py
import re

def extract_equations(text):
    # Simple LaTeX-style or math pattern detection
    equations = re.findall(r"\$.*?\$|\[.*?\]|\(.*?\)", text)
    return [eq for eq in equations if any(char.isdigit() or char in "+-=*/^" for char in eq)]
