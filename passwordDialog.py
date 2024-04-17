

import tkinter as tk

class PasswordDialog:
    def __init__(self, master):
        self.master = master
        self.master.title("Password Required")
        
        # Calculate the position for the dialog box to be centered
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        dialog_size = 15
        dialog_width = dialog_height = dialog_size * 20 # Assuming 20 pixels per unit (adjust as needed)
        x_pos = (screen_width - dialog_width) // 2
        y_pos = (screen_height - dialog_height) // 2
        self.master.geometry(f"{dialog_width}x{dialog_height}+{x_pos}+{y_pos}")

        self.label = tk.Label(master, text="Enter password:")
        self.label.pack()

        self.entry = tk.Entry(master, show="*")
        self.entry.pack()

        self.button = tk.Button(master, text="Submit", command=self.submit_password)
        self.button.pack()

    def submit_password(self):
        password = self.entry.get()
        if password == "derishisha":  # Change "your_password" to your actual password
            self.master.destroy()
        else:
            print("Invalid password. Try again.")
