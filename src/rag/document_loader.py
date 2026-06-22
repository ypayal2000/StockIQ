from pathlib import Path

from pypdf import PdfReader
from docx import Document

from src.utils.logger import logger


class DocumentLoader:

    def load_text_file(self, file_path: str):

        with open(file_path,"r",encoding="utf-8") as file:
            return file.read()


    def load_pdf(self, file_path: str):

        pdf = PdfReader(file_path)
        text = []

        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text.append(page_text)

        return "\n".join(text)


    def load_docx(self, file_path: str):

        document = Document(file_path)
        paragraphs = []

        for paragraph in document.paragraphs:
            paragraphs.append(paragraph.text)

        return "\n".join(paragraphs)


    def load_document(self, file_path: str):

        logger.info(f"Loading document: {file_path}")
        extension = (Path(file_path).suffix.lower())

        if extension == ".txt":
            text = self.load_text_file(file_path)

        if extension == ".pdf":
            text =  self.load_pdf(file_path)

        if extension == ".docx":
            text =  self.load_docx(file_path)

        return {"file_name": Path(file_path).name,
                "file_path": file_path,
                "document_type": extension.replace(".",""),
                "content": text}


if __name__ == "__main__":

    loader = DocumentLoader()

    text = loader.load_document(
        "data/documents/tcs_profile.txt"
    )

    print(text)