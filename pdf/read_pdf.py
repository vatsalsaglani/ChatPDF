import PyPDF2
import requests
import io


def is_url_or_file_path(string: str):
    return (
        string.startswith("http://")
        or string.startswith("https://")
        or string.startswith("www.")
    )


def read_pdf_from_url(url: str):
    response = requests.get(url)

    if response.status_code == 200:
        pdf = io.BytesIO(response.content)
        pdf_reader = PyPDF2.PdfReader(pdf)

        return pdf_reader
    return None

def read_pdf_from_content(content: bytes):
    pdf = io.BytesIO(content)
    pdf_reader = PyPDF2.PdfReader(pdf)
    return pdf_reader

def get_pdf_content_from_bytes(content, pdf_url: str):
    pdf_data = []
    pdf_reader = read_pdf_from_content(content)
    if not pdf_reader:
        raise Exception("Invalid Content")
    num_pages = len(pdf_reader.pages)

    for page_num in range(num_pages):
        page_obj = pdf_reader.pages[page_num]

        text = page_obj.extract_text()

        pdf_data.append({"page_no": page_num+1, "content": text, "src": pdf_url})

def read_pdf_from_local(file_path: str):
    with open(file_path, "rb") as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        return pdf_reader


def get_pdf_content_from_url(url: str):
    pdf_data = []
    pdf_reader = read_pdf_from_url(url)
    if not pdf_reader:
        raise Exception("Invalid URL")
    num_pages = len(pdf_reader.pages)

    for page_num in range(num_pages):
        page_obj = pdf_reader.pages[page_num]

        text = page_obj.extract_text()

        pdf_data.append({"page_no": page_num + 1, "content": text, "src": url})

    return pdf_data


def get_pdf_content_from_local(file_path: str):
    pdf_data = []

    with open(file_path, "rb") as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)

        num_pages = len(pdf_reader.pages)

        for page_num in range(num_pages):
            page_obj = pdf_reader.pages[page_num]

            text = page_obj.extract_text()

            pdf_data.append(
                {
                    "page_no": page_num + 1,
                    "content": text,
                    "src": file_path.split("/")[-1],
                }
            )

        return pdf_data


def get_pdf_content(path: str):
    if is_url_or_file_path(path):
        return get_pdf_content_from_url(path)
    return get_pdf_content_from_local(path)
