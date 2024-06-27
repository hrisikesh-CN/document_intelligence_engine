import os, sys
from src.exception import CustomException
from langchain_text_splitters.base import TextSplitter
from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    UnstructuredWordDocumentLoader,
    UnstructuredExcelLoader,
    UnstructuredCSVLoader,
    UnstructuredMarkdownLoader,
    UnstructuredPowerPointLoader,
    UnstructuredHTMLLoader,
    UnstructuredImageLoader,
    ImageCaptionLoader,
    Docx2txtLoader,
    AmazonTextractPDFLoader)
from langchain_text_splitters import RecursiveCharacterTextSplitter


def load_and_split_document(loader_class, file_path, splitter: TextSplitter, **loader_kwargs):
    """
    Generic function to load and split documents using a specified loader class and text splitter.


    :param loader_class: The document loader class to use.
    :param file_path: The path to the document file.
    :param splitter: The text splitter to use for splitting the document.
    :param loader_kwargs: Additional keyword arguments to pass to the loader.
    :return: Chunks of documents.
    """
    try:
        loader = loader_class(file_path, **loader_kwargs)
        docs = loader.load()
        doc_splits = splitter.split_documents(docs)
        return doc_splits
    except Exception as e:
        raise CustomException(e, sys)


def read_pdf_pypdf(pdf_path, splitter: TextSplitter):
    """Read PDFs, implement OCR for images within PDF, and return a list of chunks of documents."""
    return load_and_split_document(PyPDFLoader, pdf_path, splitter, extract_images=True)

def read_with_aws(file_path, splitter: TextSplitter, **kwargs):
    """Read PDFs,images using amazon texract, and return a list of chunks of documents.
    This can read texts from images,
    images within pdfs,
    text in pdfs,"""
    return load_and_split_document(AmazonTextractPDFLoader, file_path, splitter, **kwargs)


def read_txt(txt_path, splitter: TextSplitter):
    """Read text files and return a list of chunks of documents."""
    return load_and_split_document(TextLoader, txt_path, splitter)

# Additional functions for other document types can be implemented similarly.
def read_excel(excel_path, splitter: TextSplitter):
    """Read Excel files and return a list of chunks of documents."""
    return load_and_split_document(UnstructuredExcelLoader, excel_path, splitter)

def read_csv(csv_path, splitter: TextSplitter):
    """Read CSV files and return a list of chunks of documents."""
    return load_and_split_document(UnstructuredCSVLoader, csv_path, splitter)

def read_markdown(md_path, splitter: TextSplitter):
    """Read Markdown files and return a list of chunks of documents."""
    return load_and_split_document(UnstructuredMarkdownLoader, md_path, splitter)

def read_ppt(ppt_path, splitter: TextSplitter):
    """Read PowerPoint files and return a list of chunks of documents."""
    return load_and_split_document(UnstructuredPowerPointLoader, ppt_path, splitter)

def read_docx(docx_path, splitter: TextSplitter):
    """Read PowerPoint files and return a list of chunks of documents."""
    return load_and_split_document(Docx2txtLoader, docx_path, splitter)

def read_html(html_path, splitter: TextSplitter):
    """Read HTML files and return a list of chunks of documents."""
    return load_and_split_document(UnstructuredHTMLLoader, html_path, splitter)

def read_image(image_path, splitter: TextSplitter):
    """Read image files and return a list of chunks of documents."""
    return load_and_split_document(UnstructuredImageLoader, image_path, splitter)

def read_image_caption(image_path, splitter: TextSplitter):
    """Read image files and return a list of chunks of documents with captions."""
    return load_and_split_document(ImageCaptionLoader, image_path, splitter)
