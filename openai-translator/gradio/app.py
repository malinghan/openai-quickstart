# 1 导入 Gradio 库
import gradio as gr

# 2. 定义主函数
# greet 函数接收两个参数：
#  - name: 用户输入的名字。
#  - intensity: 用于控制“Hello”后感叹号数量的滑动条值。
# 返回值是一个字符串，包含“Hello”和用户的名字，后面跟着根据 intensity 值决定的感叹号数量。
def greet(name, intensity):
    return "Hello, " + name + "!" * int(intensity)

# 创建 Gradio 接口

# fn=greet: 指定要使用的函数。
# inputs=["text", "slider"]: 定义输入组件：
# text: 文本输入框，用于输入名字。
# slider: 滑动条，用于调整问候的强度。
# outputs=["text"]: 定义输出组件：
# text: 文本输出框，用于显示问候信息。
demo = gr.Interface(
    fn=greet,
    inputs=["text", "slider"],
    outputs=["text"],
)

# 启动接口
demo.launch()

