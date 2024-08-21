import sys
import os
os.environ["OPENAI_API_KEY"] = "sk-E0y9LTOvDNUAiMvy2h_bFVEmM2qwIL2KERn_Gh8QpMT3BlbkFJdkm7yZShaZQR-0oAPgYo6r_EEL6PYLt1Qar-McvTsA"

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils import ArgumentParser, LOG
from translator import PDFTranslator, TranslationConfig

if __name__ == "__main__":
    # 解析命令行
    argument_parser = ArgumentParser()
    args = argument_parser.parse_arguments()

    # 初始化配置单例
    config = TranslationConfig()
    config.initialize(args)    

    # 实例化 PDFTranslator 类，并调用 translate_pdf() 方法
    translator = PDFTranslator(config.model_name)
    translator.translate_pdf(config.input_file, config.output_file_format, pages=None)
