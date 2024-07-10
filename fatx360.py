import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import shutil
import threading

def is_fatx_compatible(name):
    allowed_chars = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!#$%&'()-.@[]^_`{}~")
    return len(name) <= 42 and all(char in allowed_chars for char in name)

def make_fatx_compatible(name):
    allowed_chars = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!#$%&'()-.@[]^_`{}~")
    new_name = ''.join(char if char in allowed_chars else '_' for char in name)
    return new_name[:42]

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("FATX360")
        self.master.geometry("500x400")
        self.pack(fill=tk.BOTH, expand=True)
        self.create_widgets()
        self.all_selected = False

    def create_widgets(self):
        self.create_menu()
        
        # Frame for directory selection
        dir_frame = ttk.Frame(self)
        dir_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.dir_entry = ttk.Entry(dir_frame)
        self.dir_entry.pack(side=tk.LEFT, expand=True, fill=tk.X)
        
        self.select_dir_button = ttk.Button(dir_frame, text="Select Directory", command=self.select_directory)
        self.select_dir_button.pack(side=tk.RIGHT)

        # Frame for listbox and select all button
        list_frame = ttk.Frame(self)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Select All button
        self.select_all_button = ttk.Button(list_frame, text="Select All", command=self.toggle_select_all)
        self.select_all_button.pack(side=tk.TOP, anchor=tk.W)

        # Listbox for file/folder selection
        self.listbox = tk.Listbox(list_frame, selectmode=tk.MULTIPLE)
        self.listbox.pack(fill=tk.BOTH, expand=True)

        # Frame for options
        options_frame = ttk.Frame(self)
        options_frame.pack(fill=tk.X, padx=10, pady=5)

        self.folders_only_var = tk.BooleanVar()
        self.folders_only_check = ttk.Checkbutton(options_frame, text="Rename folders only", variable=self.folders_only_var)
        self.folders_only_check.pack(side=tk.LEFT)

        self.rename_button = ttk.Button(options_frame, text="Rename Selected", command=self.rename_selected)
        self.rename_button.pack(side=tk.RIGHT)

        # Progress bar
        self.progress = ttk.Progressbar(self, orient=tk.HORIZONTAL, length=100, mode='determinate')
        self.progress.pack(fill=tk.X, padx=10, pady=5)

    def create_menu(self):
        menubar = tk.Menu(self.master)
        self.master.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Select Directory", command=self.select_directory)
        file_menu.add_command(label="Exit", command=self.master.quit)
        menubar.add_cascade(label="File", menu=file_menu)

    def select_directory(self):
        self.directory = filedialog.askdirectory()
        self.dir_entry.delete(0, tk.END)
        self.dir_entry.insert(0, self.directory)
        self.update_listbox()

    def update_listbox(self):
        self.listbox.delete(0, tk.END)
        try:
            for item in os.listdir(self.directory):
                self.listbox.insert(tk.END, item)
            self.all_selected = False
            self.select_all_button.config(text="Select All")
        except PermissionError:
            messagebox.showerror("Permission Error", "Cannot access the selected directory.")
        except FileNotFoundError:
            messagebox.showerror("Directory Not Found", "The selected directory does not exist.")

    def toggle_select_all(self):
        if self.all_selected:
            self.listbox.selection_clear(0, tk.END)
            self.select_all_button.config(text="Select All")
        else:
            self.listbox.selection_set(0, tk.END)
            self.select_all_button.config(text="Deselect All")
        self.all_selected = not self.all_selected

    def rename_selected(self):
        selected_indices = self.listbox.curselection()
        selected_items = [self.listbox.get(i) for i in selected_indices]
        if not selected_items:
            messagebox.showwarning("No Selection", "Please select items to rename.")
            return

        dest_dir = filedialog.askdirectory(title="Select Destination Folder for Renamed Items")
        if not dest_dir:
            return

        self.progress['value'] = 0
        self.rename_button['state'] = 'disabled'

        thread = threading.Thread(target=self.rename_items_thread, args=(selected_items, dest_dir))
        thread.start()

    def rename_items_thread(self, items, dest_dir):
        renamed_dir = os.path.join(dest_dir, "RENAMED")
        try:
            os.makedirs(renamed_dir, exist_ok=True)
        except PermissionError:
            self.show_error("Permission Error", "Cannot create the RENAMED directory.")
            return

        total_items = len(items)
        for i, item in enumerate(items):
            try:
                full_path = os.path.join(self.directory, item)
                if os.path.isdir(full_path) or not self.folders_only_var.get():
                    new_name = make_fatx_compatible(item)
                    new_path = os.path.join(renamed_dir, new_name)
                    
                    if os.path.isdir(full_path):
                        shutil.copytree(full_path, new_path)
                        if not self.folders_only_var.get():
                            for root, dirs, files in os.walk(new_path):
                                for name in files:
                                    if not is_fatx_compatible(name):
                                        old_file = os.path.join(root, name)
                                        new_file = os.path.join(root, make_fatx_compatible(name))
                                        os.rename(old_file, new_file)
                    else:
                        shutil.copy2(full_path, new_path)
            except PermissionError:
                self.show_error("Permission Error", f"Cannot access {item}.")
            except shutil.Error as e:
                self.show_error("Copy Error", f"Error copying {item}: {str(e)}")
            except OSError as e:
                self.show_error("OS Error", f"Error processing {item}: {str(e)}")

            self.update_progress((i + 1) / total_items * 100)

        self.show_success("Rename Complete", "Selected items have been renamed and copied to the RENAMED folder.")

    def update_progress(self, value):
        self.progress['value'] = value
        if value >= 100:
            self.rename_button['state'] = 'normal'

    def show_error(self, title, message):
        self.master.after(0, lambda: messagebox.showerror(title, message))

    def show_success(self, title, message):
        self.master.after(0, lambda: messagebox.showinfo(title, message))

root = tk.Tk()
app = Application(master=root)
app.mainloop()
