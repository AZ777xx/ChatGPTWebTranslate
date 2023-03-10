import tkinter as tk
from tkinter import *
import queue
import threading
class ChatWindow:


    def __init__(self, master, ChatGPTclass,DeepLclass):
        self.ChatGPT = ChatGPTclass
        self.DeepL = DeepLclass
        self.InputQue = queue.Queue()
        self.query_lock = threading.Lock()
        self.processing_flag = False

        self.master = master
        self.master.title("Chat Window")
        self.master.geometry("500x600")

        settingsframe = tk.Frame(master)
        settingsframe.pack()
        settingsframe.columnconfigure(0, minsize=200)
        self.ChatGPT_label = tk.Label(settingsframe, text="ChatGPT:\n Some Text")
        self.ChatGPT_label.grid(row=0, column=0, sticky="W")

        self.cookie_button = Button(settingsframe, text="Reset cookies", command = self.reset_cookies)
        self.cookie_button.grid(row=0, column=1, padx=10)

        self.reload_ChatGPT_button = Button(settingsframe, text="Reload ChatGPT", command = self.reload_ChatGPT)
        self.reload_ChatGPT_button.grid(row=0, column=2, padx=10)


        self.DeepL_label = tk.Label(settingsframe, text="DeepL:\n Some Text")
        self.DeepL_label.grid(row=1, column=0, sticky="W")

        self.language_dropdown_options = ["Option 1", "Option 2", "Option 3"]
        self.language_dropdown_selected = tk.StringVar()
        self.language_dropdown_selected.set(self.language_dropdown_options[0])
        self.language_dropdown = tk.OptionMenu(settingsframe,self.language_dropdown_selected, *self.language_dropdown_options)
        self.language_dropdown.grid(row=1, column=1, padx=5)

        self.reload_DeepL_button = Button(settingsframe, text="Reload DeepL", command=self.reload_DeepL)
        self.reload_DeepL_button.grid(row=1, column=2, padx=10)



        chatframe= tk.Frame(master)
        chatframe.pack(side=tk.BOTTOM)

        self.scrollbar = Scrollbar(chatframe)
        self.scrollbar.pack(side=RIGHT, fill=Y)

        self.text_area = Text(chatframe, height=20, width=55, yscrollcommand=self.scrollbar.set)
        self.text_area.pack(expand=True, fill=BOTH)
        self.text_area.config(state=DISABLED)

        self.scrollbar.config(command=self.text_area.yview)

        self.entry = Entry(chatframe, width=45)
        self.entry.pack(pady=10)
        self.entry.bind("<Return>", self.user_message)

        self.send_button = Button(chatframe, text="Send", command=self.user_message)
        self.send_button.pack()

        self.master.after(100, self.update_GUI_loop)

    def user_message(self,event=None):
        message = self.entry.get()
        self.InputQue.put(message)
        self.text_area.config(state=NORMAL)
        self.text_area.insert(END, "You: " + message + "\n")
        self.text_area.config(state=DISABLED)
        self.entry.delete(0, END)
        self.text_area.see(END)
    def process_user_messages_thread(self,message):
        answer = self.ChatGPT.Query(message)
        self.text_area.config(state=NORMAL)
        self.text_area.insert(END, "ChatGPT: " + answer + "\n")
        self.text_area.config(state=DISABLED)
        self.query_lock.release()
        self.processing_flag = False
        self.text_area.see(END)

    def process_user_messages(self,event=None):
        #print("quesize",self.InputQue.qsize())
        if self.InputQue.qsize() > 0 and self.query_lock.acquire(blocking=False) and not self.processing_flag:
            self.processing_flag = True
            input = self.InputQue.get()
            print("Removed from que: ", input)
            ProcessMessagesThread = threading.Thread(target=self.process_user_messages_thread,args=(input,))
            ProcessMessagesThread.start()


    def update_GUI_loop(self,event=None):
        self.process_user_messages()
        self.ChatGPT_label.config(text="ChatGPT:\n"+ self.ChatGPT.state)
        self.DeepL_label.config(text="DeepL:\n" + self.DeepL.state)
        self.master.after(100, self.update_GUI_loop)

    def reset_cookies(self, event=None):
        self.ChatGPT.clear_cookies()

    def reload_ChatGPT(self,event=None):
        self.ChatGPT.reload()
    def reload_DeepL(self,event=None):
        pass
