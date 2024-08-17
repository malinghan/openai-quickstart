# sys 和 os 用于处理文件路径和系统特定的参数
import sys
import os

# 
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# ArgumentParser, ConfigLoader, LOG 来自 utils 模块，用于解析命令行参数、加载配置文件和记录日志。
from utils import ArgumentParser, ConfigLoader, LOG
# GLMModel 和 OpenAIModel 来自 model 模块，代表不同的模型。
from model import GLMModel, OpenAIModel
# PDFTranslator 来自 translator 模块，用于翻译PDF文件。
from translator import PDFTranslator

#
if __name__ == "__main__":
    # 脚本首先创建一个 ArgumentParser 对象来解析命令行参数。
    argument_parser = ArgumentParser()
    args = argument_parser.parse_arguments()
    
     # ConfigLoader 用于从配置文件中加载配置信息。
    config_loader = ConfigLoader(args.config)
    config = config_loader.load_config()

    # 根据命令行参数或配置文件，选择使用 OpenAIModel。
    # model_name 和 api_key 用于初始化 OpenAIModel 实例。
    model_name = args.openai_model if args.openai_model else config['OpenAIModel']['model']
    api_key = args.openai_api_key if args.openai_api_key else config['OpenAIModel']['api_key']
    #
    model = OpenAIModel(model=model_name, api_key=api_key)

    # 根据命令行参数或配置文件，确定PDF文件的路径和输出文件格式。
    #  实例化 PDFTranslator 类，并使用模型实例进行翻译。
    pdf_file_path = args.book if args.book else config['common']['book']
    file_format = args.file_format if args.file_format else config['common']['file_format']

    # 调用 translate_pdf 方法，传入PDF文件路径和文件格式，进行翻译。
    # 实例化 PDFTranslator 类，并调用 translate_pdf() 方法
    translator = PDFTranslator(model)
    translator.translate_pdf(pdf_file_path, file_format)