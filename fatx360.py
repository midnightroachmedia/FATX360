import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import shutil
import threading
import re

def is_fatx_compatible(name):
    return len(name) <= 42 and all(char.isalnum() or char in "()." for char in name)

def make_fatx_compatible(name):
    filename, extension = os.path.splitext(name)
    filename = re.sub(r'[^\w\s()]', '', filename)
    words = filename.split()
    if words:
        camel_case_name = words[0].lower()
        for word in words[1:]:
            camel_case_name += word.capitalize()
    else:
        camel_case_name = ""
    max_filename_length = 42 - len(extension)
    if len(camel_case_name) > max_filename_length:
        camel_case_name = camel_case_name[:max_filename_length]
    return camel_case_name + extension

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("FATX360 v1.3")
        self.master.geometry("500x550")
        self.pack(fill=tk.BOTH, expand=True)
        self.all_selected = False
        self.total_items = 0
        self.processed_items = 0
        self.cancel_flag = False
        self.max_depth = 10  # Maximum depth for the slider
        self.create_widgets()

    def create_widgets(self):
        self.create_menu()
        
        dir_frame = ttk.Frame(self)
        dir_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.dir_entry = ttk.Entry(dir_frame)
        self.dir_entry.pack(side=tk.LEFT, expand=True, fill=tk.X)
        
        self.select_dir_button = ttk.Button(dir_frame, text="Select Directory", command=self.select_directory)
        self.select_dir_button.pack(side=tk.RIGHT)

        list_frame = ttk.Frame(self)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.select_all_button = ttk.Button(list_frame, text="Select All", command=self.toggle_select_all)
        self.select_all_button.pack(side=tk.TOP, anchor=tk.W)

        self.listbox = tk.Listbox(list_frame, selectmode=tk.MULTIPLE)
        self.listbox.pack(fill=tk.BOTH, expand=True)

        options_frame = ttk.Frame(self)
        options_frame.pack(fill=tk.X, padx=10, pady=5)

        self.top_level_var = tk.BooleanVar()
        self.top_level_check = ttk.Checkbutton(options_frame, text="Rename top-level folders", 
                                               variable=self.top_level_var)
        self.top_level_check.pack(side=tk.TOP, anchor=tk.W)

        self.subfolders_var = tk.BooleanVar()
        self.subfolders_check = ttk.Checkbutton(options_frame, text="Rename subfolders", 
                                                variable=self.subfolders_var, 
                                                command=self.toggle_depth_slider)
        self.subfolders_check.pack(side=tk.TOP, anchor=tk.W)

        # Depth slider
        self.depth_frame = ttk.Frame(options_frame)
        self.depth_frame.pack(side=tk.TOP, fill=tk.X, padx=20, pady=5)
        self.depth_label = ttk.Label(self.depth_frame, text="Subfolder depth:")
        self.depth_label.pack(side=tk.LEFT)
        self.depth_var = tk.IntVar(value=self.max_depth)
        self.depth_slider = ttk.Scale(self.depth_frame, from_=1, to=self.max_depth, 
                                      orient=tk.HORIZONTAL, variable=self.depth_var, 
                                      length=200, command=self.update_depth_label)
        self.depth_slider.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.depth_value_label = ttk.Label(self.depth_frame, text=str(self.max_depth))
        self.depth_value_label.pack(side=tk.LEFT)
        self.depth_frame.pack_forget()  # Initially hidden

        self.files_var = tk.BooleanVar()
        self.files_check = ttk.Checkbutton(options_frame, text="Rename files", 
                                           variable=self.files_var)
        self.files_check.pack(side=tk.TOP, anchor=tk.W)

        self.rename_button = ttk.Button(options_frame, text="Rename Selected", 
                                        command=self.rename_selected)
        self.rename_button.pack(side=tk.TOP, pady=5)

        progress_frame = ttk.Frame(self)
        progress_frame.pack(fill=tk.X, padx=10, pady=5)

        self.progress = ttk.Progressbar(progress_frame, orient=tk.HORIZONTAL, length=100, mode='determinate')
        self.progress.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.progress_label = ttk.Label(progress_frame, text="0 / 0")
        self.progress_label.pack(side=tk.RIGHT)

        self.cancel_button = ttk.Button(self, text="Cancel", command=self.cancel_operation, state=tk.DISABLED)
        self.cancel_button.pack(pady=5)

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

    def toggle_depth_slider(self):
        if self.subfolders_var.get():
            self.depth_frame.pack(side=tk.TOP, fill=tk.X, padx=20, pady=5)
        else:
            self.depth_frame.pack_forget()

    def update_depth_label(self, *args):
        self.depth_value_label.config(text=str(self.depth_var.get()))

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
        self.cancel_button['state'] = 'normal'
        self.cancel_flag = False

        self.total_items = self.count_total_items(selected_items)
        self.processed_items = 0
        self.update_progress_label()

        thread = threading.Thread(target=self.rename_items_thread, args=(selected_items, dest_dir))
        thread.start()

    def count_total_items(self, items):
        total = 0
        for item in items:
            full_path = os.path.join(self.directory, item)
            if os.path.isdir(full_path):
                for root, dirs, files in os.walk(full_path):
                    total += len(files)
            else:
                total += 1
        return total

    def rename_items_thread(self, items, dest_dir):
        renamed_dir = os.path.join(dest_dir, "RENAMED")
        try:
            os.makedirs(renamed_dir, exist_ok=True)
        except PermissionError:
            self.show_error("Permission Error", "Cannot create the RENAMED directory.")
            self.finish_operation()
            return

        for item in items:
            if self.cancel_flag:
                return  # Exit the loop if cancelled
            try:
                full_path = os.path.join(self.directory, item)
                if os.path.isdir(full_path):
                    self.process_directory(full_path, renamed_dir, self.top_level_var.get(), self.subfolders_var.get(), self.files_var.get())
                else:
                    self.process_file(full_path, renamed_dir, self.files_var.get())
            except PermissionError:
                self.show_error("Permission Error", f"Cannot access {item}.")
            except shutil.Error as e:
                self.show_error("Copy Error", f"Error copying {item}: {str(e)}")
            except OSError as e:
                self.show_error("OS Error", f"Error processing {item}: {str(e)}")

        if not self.cancel_flag:
            self.show_success("Rename Complete", "Selected items have been renamed and copied to the RENAMED folder.")
        self.finish_operation()

    def process_directory(self, src_dir, dest_parent_dir, rename_top_level, rename_subfolders, rename_files, current_depth=0):
        new_dir_name = make_fatx_compatible(os.path.basename(src_dir)) if rename_top_level or (rename_subfolders and current_depth < self.depth_var.get()) else os.path.basename(src_dir)
        new_dir_path = os.path.join(dest_parent_dir, new_dir_name)
        os.makedirs(new_dir_path, exist_ok=True)

        for root, dirs, files in os.walk(src_dir):
            if self.cancel_flag:
                return
            rel_path = os.path.relpath(root, src_dir)
            new_root = os.path.join(new_dir_path, rel_path)

            # Rename subfolders if option is selected and within depth
            if rename_subfolders and current_depth < self.depth_var.get() and root != src_dir:
                new_root = os.path.join(os.path.dirname(new_root), make_fatx_compatible(os.path.basename(root)))

            os.makedirs(new_root, exist_ok=True)

            for file in files:
                if self.cancel_flag:
                    return
                src_file = os.path.join(root, file)
                self.process_file(src_file, new_root, rename_files)

            # Process subdirectories
            for dir_name in dirs:
                full_dir_path = os.path.join(root, dir_name)
                self.process_directory(full_dir_path, new_root, False, rename_subfolders, rename_files, current_depth + 1)

            # We only want to process the top-level of this directory, so break the loop
            break

    def process_file(self, src_file, dest_dir, rename_file):
        new_name = make_fatx_compatible(os.path.basename(src_file)) if rename_file else os.path.basename(src_file)
        new_path = os.path.join(dest_dir, new_name)
        shutil.copy2(src_file, new_path)
        self.processed_items += 1
        self.update_progress()

    def update_progress(self):
        progress_value = (self.processed_items / self.total_items) * 100
        self.progress['value'] = progress_value
        self.update_progress_label()

    def update_progress_label(self):
        self.progress_label.config(text=f"{self.processed_items} / {self.total_items}")

    def cancel_operation(self):
        self.cancel_flag = True
        self.cancel_button['state'] = 'disabled'
        self.show_info("Operation Cancelled", "The renaming operation was cancelled.")
        self.reset_interface()

    def finish_operation(self):
        self.rename_button['state'] = 'normal'
        self.cancel_button['state'] = 'disabled'
        self.cancel_flag = False
        self.reset_interface()

    def reset_interface(self):
        # Reset progress bar
        self.progress['value'] = 0
        self.progress_label.config(text="0 / 0")
        
        # Reset selection
        self.listbox.selection_clear(0, tk.END)
        self.all_selected = False
        self.select_all_button.config(text="Select All")
        
        # Reset checkboxes
        self.top_level_var.set(False)
        self.subfolders_var.set(False)
        self.files_var.set(False)
        
        # Hide depth slider
        self.depth_frame.pack_forget()
        
        # Reset depth slider value
        self.depth_var.set(self.max_depth)
        self.update_depth_label()
        
        # Reset counters
        self.total_items = 0
        self.processed_items = 0

    def show_error(self, title, message):
        self.master.after(0, lambda: messagebox.showerror(title, message))

    def show_success(self, title, message):
        self.master.after(0, lambda: messagebox.showinfo(title, message))

    def show_info(self, title, message):
        self.master.after(0, lambda: messagebox.showinfo(title, message))

root = tk.Tk()
app = Application(master=root)
app.mainloop()
