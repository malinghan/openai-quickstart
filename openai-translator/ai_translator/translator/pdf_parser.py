import pdfplumber
from typing import Optional
from book import Book, Page, Content, ContentType, TableContent
from translator.exceptions import PageOutOfRangeException
from utils import LOG


class PDFParser:
    def __init__(self):
        pass
    # pdf解析核心函数。 
    # pdf_file_path文件输入路径，pages页数， Book
    # Book是文档内存加载类型
    def parse_pdf(self, pdf_file_path: str, pages: Optional[int] = None) -> Book:
        book = Book(pdf_file_path)
        # 1. 打开pdf文件
        with pdfplumber.open(pdf_file_path) as pdf:
            # 2. 页码检查，如果超出，则抛错
            if pages is not None and pages > len(pdf.pages):
                raise PageOutOfRangeException(len(pdf.pages), pages)
            # 3. 如果页码数量为空，则解析整个文件
            if pages is None:
                pages_to_parse = pdf.pages
            else:
                pages_to_parse = pdf.pages[:pages]
            # 4.按页码解析
            for pdf_page in pages_to_parse:
                page = Page()
                 # a. 提取每页的原始文本
                # Store the original text content
                raw_text = pdf_page.extract_text()
                # b. 提取表格
                tables = pdf_page.extract_tables()
                # c. 清理表格数据. 去除文本，保留格式
                # Remove each cell's content from the original text
                for table_data in tables:
                    for row in table_data:
                        for cell in row:
                            raw_text = raw_text.replace(cell, "", 1)
                # d.解析原始文本 1. 去除首位空格，创建Content对象，将其加到page中
                # Handling text
                if raw_text:
                    # Remove empty lines and leading/trailing whitespaces
                    raw_text_lines = raw_text.splitlines()
                    cleaned_raw_text_lines = [line.strip() for line in raw_text_lines if line.strip()]
                    cleaned_raw_text = "\n".join(cleaned_raw_text_lines)

                    text_content = Content(content_type=ContentType.TEXT, original=cleaned_raw_text)
                    page.add_content(text_content)
                    LOG.debug(f"[raw_text]\n {cleaned_raw_text}")


                # e. 解析表格信息， 创建tableContent，将其加入表格中
                # Handling tables
                if tables:
                    table = TableContent(tables)
                    page.add_content(table)
                    LOG.debug(f"[table]\n{table}")

                book.add_page(page)

        return book
