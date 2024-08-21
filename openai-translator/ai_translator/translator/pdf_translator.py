from typing import Optional
from model import Model
from translator.pdf_parser import PDFParser
from translator.writer import Writer
from utils import LOG

class PDFTranslator:
    def __init__(self, model: Model):
        self.model = model
        self.pdf_parser = PDFParser()
        self.writer = Writer()
        
# pdf_file_path 文件输入路径
# file_format  文件输入格式
# target_language  文件输出语言
# output_file_path  文件输出格式 
# pages    需要解析的具体页数
    def translate_pdf(self, pdf_file_path: str, file_format: str = 'PDF', target_language: str = 'Chinese', output_file_path: str = None, pages: Optional[int] = None):
        self.book = self.pdf_parser.parse_pdf(pdf_file_path, pages)
        # 循环按页数解析
        for page_idx, page in enumerate(self.book.pages):
            # 每页按content解析
            for content_idx, content in enumerate(page.contents):
                # 定义translate_prompt
                prompt = self.model.translate_prompt(content, target_language)
                # 1. 日志记录prompt
                LOG.debug(prompt)
                # 调用openai请求,进行请求
                translation, status = self.model.make_request(prompt)
                # 2. 日志记录翻译后的结果：translation
                LOG.info(translation)
                # 将翻译后的结果进行更新
                # Update the content in self.book.pages directly
                self.book.pages[page_idx].contents[content_idx].set_translation(translation, status)
        # 保存输出翻译后的信息
        self.writer.save_translated_book(self.book, output_file_path, file_format)
