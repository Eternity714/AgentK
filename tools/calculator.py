from langchain_core.tools import tool

@tool
def calculator(num1: float, num2: float, operator: str) -> str:
    """简单计算器工具，接受两个数字和一个操作符，返回计算结果。支持的操作符：+、-、*、/"""
    try:
        if operator == '+':
            result = num1 + num2
        elif operator == '-':
            result = num1 - num2
        elif operator == '*':
            result = num1 * num2
        elif operator == '/':
            if num2 == 0:
                return "错误：除数不能为0"
            result = num1 / num2
        else:
            return f"错误：不支持的操作符'{operator}'"
        return f"计算结果：{result}"
    except Exception as e:
        return f"计算错误：{str(e)}"
