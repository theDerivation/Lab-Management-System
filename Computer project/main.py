import tkinter as tk
from tkinter import ttk
import sqlite3
from tkinter import messagebox

class AdminLoginPage:
    def __init__(self, root):
        self.root = root
        self.root.title("Admin Login")
        
        # admin pg size
        self.root.geometry("500x600")
        
        # canvas for admin background
        self.canvas = tk.Canvas(self.root, width=500, height=600)
        self.canvas.grid(row=0, column=0, rowspan=4, columnspan=2) #canvas in grid
        
        self.gradient_background()
        
        # password
        self.label_password = tk.Label(self.root, text="Admin Password:")
        self.entry_password = tk.Entry(self.root, show="*")
        
        # login
        self.login_button = tk.Button(self.root, text="Login", command=self.login)
        
        # admin pg grid
        self.label_password.grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.entry_password.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
        self.login_button.grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky="ew")  # Use sticky to make button expand
        
        self.center_window()
    
    def center_window(self):
        # screen dimensions
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # center
        x = (screen_width - 500) // 2
        y = (screen_height - 600) // 2
        
        self.root.geometry("500x600+{}+{}".format(x, y))
    
    def gradient_background(self):
        #top to bottom gradient
        for i in range(600):
            r = 255
            g = max(255 - i // 2, 0)  
            b = max(255 - i // 2, 0)  

            color = "#{:02x}{:02x}{:02x}".format(r, g, b)

            self.canvas.create_line(0, i, 500, i, fill=color)
    
    def login(self):
        password = self.entry_password.get()
        if password == "vanderwaal":
            self.root.destroy()  #close admin pg
            lab_root = tk.Tk()
            lab_app = LabManagementSystem(lab_root)
            lab_root.mainloop()
        else:
            self.display_message("Incorrect Admin Password")
    
    def display_message(self, message):
        pass

class LabManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Lab Management System")
        
        # Window size
        self.root.geometry("800x600")
        
        # db
        self.conn = sqlite3.connect("lab_equipment.db")
        self.cursor = self.conn.cursor()
        self.create_equipment_table()
        
        # Inputs, drop downs
        self.label_name = tk.Label(root, text="Equipment Name:")
        self.label_equipment_broken = tk.Label(root, text="Equipment Broken:")  
        self.label_quantity_broken = tk.Label(root, text="Quantity Broken:")
        self.label_quantity = tk.Label(root, text="Quantity:")
        
        self.equipment_names = ["Item 1", "Item 2", "Item 3", "Item 4"]  #test names
        self.equipment_name_var = tk.StringVar(root)
        self.equipment_name_var.set(self.equipment_names[0])
        self.equipment_name_dropdown = ttk.Combobox(root, textvariable=self.equipment_name_var, values=self.equipment_names, state='readonly')
        
        self.equipment_broken_var = tk.StringVar(root)
        self.equipment_broken_var.set("No")  #default value
        self.equipment_broken_dropdown = ttk.Combobox(root, textvariable=self.equipment_broken_var, values=["Yes", "No"], state='readonly')
        
        self.entry_quantity_broken = tk.Entry(root)
        self.entry_quantity = tk.Entry(root)
        
        # Create buttons
        self.add_button = tk.Button(root, text="Add Equipment", command=self.add_equipment, bg="green", fg="white")
        self.remove_button = tk.Button(root, text="Remove Equipment", command=self.remove_equipment, bg="red", fg="white")
        
        # table display
        self.tree = ttk.Treeview(root, columns=("Name", "Equipment Broken", "Quantity Broken", "Quantity"), show="headings", height=15)
        self.tree.heading("Name", text="Equipment Name")
        self.tree.heading("Equipment Broken", text="Equipment Broken")  # Added column for Equipment Broken
        self.tree.heading("Quantity Broken", text="Quantity Broken")
        self.tree.heading("Quantity", text="Quantity")
        self.tree.column("Name", width=200)
        self.tree.column("Equipment Broken", width=150)  # Added width for Equipment Broken
        self.tree.column("Quantity Broken", width=150)
        self.tree.column("Quantity", width=100)
        
        # Scrollbar 
        self.scrollbar = ttk.Scrollbar(root, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrollbar.set)
        
        # Grid layout for other widgets
        self.label_name.grid(row=0, column=2, padx=10, pady=5, sticky="w")
        self.equipment_name_dropdown.grid(row=0, column=3, padx=10, pady=5, sticky="ew")
        self.label_equipment_broken.grid(row=0, column=4, padx=10, pady=5, sticky="w")
        self.equipment_broken_dropdown.grid(row=0, column=5, padx=10, pady=5, sticky="ew")
        self.label_quantity.grid(row=2, column=2, padx=10, pady=5, sticky="w")
        self.label_quantity_broken.grid(row=2, column=4, padx=10, pady=5, sticky="w")
        self.entry_quantity.grid(row=2, column=3, padx=10, pady=5, sticky="ew")
        self.entry_quantity_broken.grid(row=2, column=5, padx=10, pady=5, sticky="ew")
        self.add_button.grid(row=3, column=2, padx=10, pady=5)
        self.remove_button.grid(row=3, column=4, padx=10, pady=5)
        self.tree.grid(row=4, column=2, columnspan=4, padx=10, pady=5, sticky="nsew")
        self.scrollbar.grid(row=4, column=6, sticky="ns")
        
        # widgets resize w/ resize in window
        root.grid_rowconfigure(4, weight=1)
        root.grid_columnconfigure(2, weight=1)
    
    def create_equipment_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS lab_equipment (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            equipment_broken TEXT NOT NULL,
            quantity_broken INTEGER NOT NULL,
            quantity INTEGER NOT NULL
        )''')
        self.conn.commit()
    
    def add_equipment(self):
        name = self.equipment_name_var.get()
        equipment_broken = self.equipment_broken_var.get()
        quantity = self.entry_quantity.get()
        quantity_broken = self.entry_quantity_broken.get()
        
        if quantity and quantity_broken:
            equipment_info = (name, equipment_broken, quantity_broken, quantity)
            if equipment_broken == "No":
                self.cursor.execute("INSERT INTO lab_equipment (name, equipment_broken, quantity_broken, quantity) VALUES (?, ?, ?, ?)", equipment_info)
            elif equipment_broken == "Yes":
                self.cursor.execute("INSERT INTO lab_equipment (name, equipment_broken, quantity_broken, quantity) VALUES (?, ?, ?, ?)", equipment_info)
            self.conn.commit()
            self.equipment_name_var.set(self.equipment_names[0])
            self.equipment_broken_var.set("No")
            self.entry_quantity.delete(0, tk.END)
            self.entry_quantity_broken.delete(0, tk.END)
            self.display_message(f"Added equipment: {equipment_info[0]}, Equipment Broken: {equipment_info[1]}, Quantity Broken: {equipment_info[2]}, Quantity: {equipment_info[3]}")
            self.update_equipment_table()
        else:
            self.display_message("Please enter all equipment details.")
    
    def update_equipment_table(self):
        self.clear_treeview()
        self.cursor.execute("SELECT name, equipment_broken, quantity_broken, quantity FROM lab_equipment")
        equipment_data = self.cursor.fetchall()
        for row in equipment_data:
            self.tree.insert("", "end", values=row)
    
    def display_message(self, message):
        pass
    
    def clear_treeview(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
    
    def remove_equipment(self):
        selected_item = self.tree.selection()
        if not selected_item:
            self.display_message("Please select an equipment to remove.")
            return

        confirmation = messagebox.askyesno("Confirmation", "Are you sure you want to remove the selected equipment?")
        if confirmation:
            for item in selected_item:
                equipment_name = self.tree.item(item, "values")[0]
                self.cursor.execute("DELETE FROM lab_equipment WHERE name=?", (equipment_name,))
                self.conn.commit()
                self.tree.delete(item)
                self.display_message(f"Removed equipment: {equipment_name}")

if __name__ == "__main__":
    root = tk.Tk()
    app = AdminLoginPage(root)
    root.mainloop()
