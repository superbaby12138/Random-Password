import tkinter as tk
from tkinter import messagebox, scrolledtext
import secrets
import string
from datetime import datetime

# 日志文件路径
LOG_FILE = "password_log.txt"

def generate_password():
    # 获取用户选择的字符类型
    use_uppercase = uppercase_var.get()
    use_lowercase = lowercase_var.get()
    use_digits = digits_var.get()
    use_symbols = symbols_var.get()

    # 获取密码长度
    try:
        length = int(length_entry.get())
        if length <= 0:
            raise ValueError("密码长度必须大于0")
    except ValueError:
        messagebox.showerror("错误", "请输入有效的密码长度（正整数）")
        return

    # 定义字符集
    charset = ""
    required_chars = []  # 用于存储必须包含的字符

    if use_uppercase:
        charset += string.ascii_uppercase
        required_chars.append(secrets.choice(string.ascii_uppercase))  # 至少一个大写字母
    if use_lowercase:
        charset += string.ascii_lowercase
        required_chars.append(secrets.choice(string.ascii_lowercase))  # 至少一个小写字母
    if use_digits:
        charset += string.digits
        required_chars.append(secrets.choice(string.digits))  # 至少一个数字
    if use_symbols:
        symbols = "!@#$%^&*_+-="
        charset += symbols
        required_chars.append(secrets.choice(symbols))  # 至少一个特殊符号

    # 检查是否至少选择了一种字符类型
    if not charset:
        messagebox.showerror("错误", "请至少选择一种字符类型")
        return

    # 检查密码长度是否足够
    if length < len(required_chars):
        messagebox.showerror("错误", f"密码长度至少为 {len(required_chars)} 位")
        return

    # 生成密码
    remaining_length = length - len(required_chars)
    password = required_chars + [secrets.choice(charset) for _ in range(remaining_length)]
    secrets.SystemRandom().shuffle(password)  # 打乱顺序
    password = ''.join(password)

    # 显示密码
    password_var.set(password)

    # 记录密码到日志文件
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as log_file:
        log_file.write(f"{timestamp}: {password}\n")

    # 更新历史记录显示
    update_history()

def update_history():
    """读取日志文件并更新历史记录显示"""
    try:
        with open(LOG_FILE, "r") as log_file:
            history = log_file.readlines()
        history_text.delete(1.0, tk.END)  # 清空当前内容
        for line in reversed(history):  # 最新的记录显示在最上面
            history_text.insert(tk.END, line)
    except FileNotFoundError:
        history_text.delete(1.0, tk.END)
        history_text.insert(tk.END, "无历史记录")

# 创建主窗口
root = tk.Tk()
root.title("随机密码生成器")

# 窗口自适应
root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(7, weight=1)

# 密码长度输入框
length_label = tk.Label(root, text="密码长度:")
length_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
length_entry = tk.Entry(root)
length_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
length_entry.insert(0, "8")  # 默认密码长度为8

# 复选框：选择字符类型
uppercase_var = tk.BooleanVar(value=True)
lowercase_var = tk.BooleanVar(value=True)
digits_var = tk.BooleanVar(value=True)
symbols_var = tk.BooleanVar(value=True)

tk.Checkbutton(root, text="大写字母 (A-Z)", variable=uppercase_var).grid(row=1, column=0, padx=10, pady=5, sticky="w")
tk.Checkbutton(root, text="小写字母 (a-z)", variable=lowercase_var).grid(row=2, column=0, padx=10, pady=5, sticky="w")
tk.Checkbutton(root, text="数字 (0-9)", variable=digits_var).grid(row=3, column=0, padx=10, pady=5, sticky="w")
tk.Checkbutton(root, text="特殊符号 (!@#$%^&*_+-=)", variable=symbols_var).grid(row=4, column=0, padx=10, pady=5, sticky="w")

# 生成按钮
generate_button = tk.Button(root, text="生成密码", command=generate_password)
generate_button.grid(row=5, column=0, columnspan=2, pady=10)

# 显示生成的密码
password_var = tk.StringVar()
password_label = tk.Label(root, text="生成的密码:")
password_label.grid(row=6, column=0, padx=10, pady=10, sticky="w")
password_entry = tk.Entry(root, textvariable=password_var, state="readonly")
password_entry.grid(row=6, column=1, padx=10, pady=10, sticky="ew")

# 历史记录显示
history_label = tk.Label(root, text="历史记录:")
history_label.grid(row=7, column=0, padx=10, pady=10, sticky="nw")
history_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=40, height=10)
history_text.grid(row=7, column=1, padx=10, pady=10, sticky="nsew")

# 初始化历史记录
update_history()

# 运行主循环
root.mainloop()