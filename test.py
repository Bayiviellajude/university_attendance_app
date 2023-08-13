import tkinter as tk
from tkinter import messagebox
from datetime import datetime

class TodoList:
    def __init__(self, master):
        self.master = master
        self.master.title("My Todo")
        self.master.geometry("400x400")
        
        # Create a listbox to display the to-do items
        self.listbox = tk.Listbox(self.master, height=15, width=50)
        self.listbox.pack(pady=10)
        
        # Add scrollbar to the listbox
        scrollbar = tk.Scrollbar(self.master)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.listbox.yview)
        
        # Create an entry field for adding new items
        self.entry = tk.Entry(self.master, width=50)
        self.entry.pack(pady=10)
        
        # Add buttons for adding and deleting items
        add_button = tk.Button(self.master, text="Add Item", command=self.add_item)
        add_button.pack(side=tk.LEFT, padx=10)
        delete_button = tk.Button(self.master, text="Delete Item", command=self.delete_item)
        delete_button.pack(side=tk.LEFT, padx=10)
        
        # Add a button for clearing all items
        clear_button = tk.Button(self.master, text="Clear All", command=self.clear_all)
        clear_button.pack(side=tk.LEFT, padx=10)
        
        # Load existing items from a file
        self.load_items()
    
    def load_items(self):
        try:
            with open("items.txt", "r") as f:
                items = f.readlines()
                for item in items:
                    self.listbox.insert(tk.END, item.strip())
        except FileNotFoundError:
            pass
    
    def add_item(self):
        item = self.entry.get()
        if item:
            now = datetime.now()
            date_time = now.strftime("%m/%d/%Y %H:%M:%S")
            item = f"{date_time} - {item}"
            self.listbox.insert(tk.END, item)
            self.entry.delete(0, tk.END)
            self.save_items()
        else:
            messagebox.showerror("Error", "Please enter an item!")
    
    def delete_item(self):
        selection = self.listbox.curselection()
        if selection:
            self.listbox.delete(selection[0])
            self.save_items()
        else:
            messagebox.showerror("Error", "Please select an item to delete!")
    
    def clear_all(self):
        self.listbox.delete(0, tk.END)
        self.save_items()
    
    def save_items(self):
        items = self.listbox.get(0, tk.END)
        with open("items.txt", "w") as f:
            for item in items:
                f.write(item + "\n")

root = tk.Tk()
app = TodoList(root)
root.mainloop()
