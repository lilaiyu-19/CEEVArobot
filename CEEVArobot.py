import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import SparkLoader

def on_select(event):
    selected_index = listbox.curselection()
    if selected_index:
        selected_value = options[selected_index[0]]
        selected_option.set(selected_value)
        listbox.place_forget()
        update_entry()


def show_listbox():
    if listbox.winfo_viewable():
        listbox.place_forget()
    else:
        listbox_x = entry_frame.winfo_x()
        listbox_y = entry_frame.winfo_y() + entry_frame.winfo_height()
        listbox_width = entry_frame.winfo_width()
        listbox_height = 70
        listbox.place(x=listbox_x, y=listbox_y, width=listbox_width, height=listbox_height)


def update_entry():
    entry.delete(0, tk.END)
    entry.insert(0, selected_option.get())


def append_to_chat_history(user_text, ai_text):
    chat_history.config(state=tk.NORMAL)
    chat_history.insert(tk.END, f"我: {user_text}\n")
    chat_history.insert(tk.END, f"您的机器人助手: {ai_text}\n")
    chat_history.config(state=tk.DISABLED)
    chat_history.see(tk.END)


def insert_newline(event, text_widget):
    text_widget.insert(tk.INSERT, "\n")
    return "break"


# 定义一个函数来处理从Text控件提交的输入
def process_input_from_text(event=None, text_widget=None):
    user_input = text_widget.get("1.0", tk.END).strip()
    if not user_input:
        text_widget.delete("1.0", tk.END)
        messagebox.showwarning("输入不合法", "请在提问前输入内容！")
        return
    selected_model = entry.get()
    loader = SparkLoader.SparkLoader(selected_model)
    answer = loader.Question(user_input)
    append_to_chat_history(user_input, answer)
    text_widget.delete("1.0", tk.END)


def on_return_key(event, text_widget):
    process_input_from_text(event=event, text_widget=text_widget)
    return "break"

if __name__ == '__main__':
    bg_color = "#FDFCFB"
    font_tuple_1 = ('华文楷体', 16)
    font_tuple_2 = ('华文楷体', 14)
    font_tuple_3 = ('华文楷体', 12)
    options = ["Spark Pro", "Spark4.0 Ultra", "Spark max"]

    root = tk.Tk()
    root.title("高考志愿问答机器人")
    root.geometry("960x600+370+195")
    root.resizable(False, False)

    bg_image = Image.open("background.png")
    bg_image = bg_image.resize((960, 600), Image.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg_image)
    canvas = tk.Canvas(root, width=960, height=600, highlightthickness=0)
    canvas.pack(fill="both", expand=True)
    canvas.create_image(0, 0, image=bg_photo, anchor='nw')

    selected_option = tk.StringVar()
    selected_option.set(options[0])
    label = tk.Label(root, text="当前选择模型：", bg=bg_color, fg="black", font=font_tuple_1)
    label.place(x=30, y=70)
    entry_frame = tk.Frame(root, bg=bg_color)
    entry_frame.place(x=30, y=100)
    entry = tk.Entry(entry_frame, textvariable=selected_option, state="readonly", bg=bg_color, fg="black",
                     font=font_tuple_2)
    entry.pack(side="left", fill="both", expand=True, padx=1)
    button_image = Image.open("double-down.png")
    button_image = button_image.resize((25, 25), Image.LANCZOS)
    button_photo = ImageTk.PhotoImage(button_image)
    button = tk.Button(entry_frame, image=button_photo, command=show_listbox, bg=bg_color, fg="black")
    button.pack(side="right", fill="both", expand=False)
    listbox = tk.Listbox(root, selectmode=tk.SINGLE, bg=bg_color, fg="black", font=font_tuple_2)
    for option in options:
        listbox.insert(tk.END, option)
    listbox.bind("<<ListboxSelect>>", on_select)
    listbox.place_forget()

    right_frame = tk.Frame(root, bg=bg_color)
    right_frame.place(x=280, y=50, width=570, height=480)

    # 创建用于显示聊天记录的Text控件和Scrollbar的框架
    chat_history_frame = tk.Frame(right_frame)
    chat_history_frame.grid(row=0, column=0, sticky="nsew", pady=8)
    chat_history = tk.Text(chat_history_frame, bg=bg_color, fg="black", font=font_tuple_3, wrap='word',
                           state=tk.DISABLED)
    chat_history.grid(row=0, column=0, sticky="nsew")
    scrollbar = tk.Scrollbar(chat_history_frame, orient=tk.VERTICAL, command=chat_history.yview)
    scrollbar.grid(row=0, column=1, sticky="ns")
    chat_history['yscrollcommand'] = scrollbar.set
    chat_history_frame.grid_columnconfigure(0, weight=1)
    chat_history_frame.grid_rowconfigure(0, weight=1)

    # 创建用于输入文本的Text控件和按钮的框架
    right_entry_frame = tk.Frame(right_frame, bg=bg_color)
    right_entry_frame.grid(row=1, column=0, sticky="nsew")
    right_entry = tk.Text(right_entry_frame, bg=bg_color, fg="black", font=font_tuple_3, height=2)
    right_entry.grid(row=0, column=0, sticky="nsew")

    # 绑定事件到Text控件
    right_entry.bind("<Alt-Return>", lambda event: insert_newline(event, right_entry))
    right_entry.bind("<Return>", lambda event: on_return_key(event, right_entry))

    sub_button_image = Image.open("send.png")
    sub_button_image = sub_button_image.resize((54, 25), Image.LANCZOS)
    sub_button_photo = ImageTk.PhotoImage(sub_button_image)
    submit_button = tk.Button(right_entry_frame, image=sub_button_photo, width=54,
                              command=lambda: process_input_from_text(None, right_entry),
                              bg=bg_color)
    submit_button.grid(row=0, column=1, sticky="ns")

    right_entry_frame.grid_columnconfigure(0, weight=1)
    right_entry_frame.grid_columnconfigure(1, weight=0)
    right_entry_frame.grid_rowconfigure(0, weight=1)

    right_frame.grid_rowconfigure(0, weight=7)
    right_frame.grid_rowconfigure(1, weight=1)
    right_frame.grid_columnconfigure(0, weight=1)

    root.mainloop()
