import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import tkinter.font as tkFont

# Initialize data structures for apparatus, chemicals, and experiments
with open("db.txt") as f:
    lines = f.readlines()   
    apparatus = eval(lines[0])
    chemicals = eval(lines[1])
    experiments = eval(lines[2])
    print(apparatus)
    print(chemicals)
    print(experiments)


admin_username = "admin"
admin_password = "ok"

DEFAULT_FONT = ("SF Pro Display", 13)

class LabManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Lab Inventory Management")
        self.root["bg"] = "skyblue"

        global DEFAULT_FONT_OBJECT
        DEFAULT_FONT_OBJECT = tkFont.Font(family='SF Pro Display', size=13)

        def get_width(e=None):
            print(self.root.winfo_width())
            print(self.root.winfo_height())
    
        self.root.bind("<Escape>", get_width)

        # Create the Notebook (Tabbed Interface)
        self.notebook = ttk.Notebook(root)
        self.notebook.bind("<<NotebookTabChanged>>", self.center_window)
        self.notebook.pack(fill='both', expand=True)

        self.inventory_tab = ttk.Frame(self.notebook, width=834)
        self.experiments_tab = ttk.Frame(self.notebook, width=1090)

        self.notebook.add(self.inventory_tab, text='Inventory')
        self.notebook.add(self.experiments_tab, text='Experiments')
        
        self.center_window()

    def center_window(self, e=None):
        if self.notebook.index(self.notebook.select()) == 0:
            self.root.geometry("838x389")
        else:
            self.root.geometry("1008x500")


#=========================================INVENTORY===================================#

        self.a = tk.Label(self.inventory_tab, text="Apparatus", font=DEFAULT_FONT)

        self.apparatus_chosen = tk.StringVar()
        self.apparatus_chosen.set("Choose an Apparatus")

        global apparatuses
        apparatuses = [
            "Titration flask",
            "Flat bottomed flask",
            "Test tube",
            "Burette",
        ]
        self.apparatus_entry = tk.OptionMenu(self.inventory_tab, self.apparatus_chosen,  *apparatuses)

        menu = self.inventory_tab.nametowidget(self.apparatus_entry.menuname)
        menu.config(font=DEFAULT_FONT_OBJECT)
        self.apparatus_entry.config(font=DEFAULT_FONT)

        self.q = tk.Label(self.inventory_tab, text="Quantity", font=DEFAULT_FONT)
        self.apparatus_quantity_entry = tk.Entry(self.inventory_tab, font=DEFAULT_FONT)

        self.add_apparatus_button = tk.Button(self.inventory_tab, text="Add Apparatus", command=self.add_apparatus, font=DEFAULT_FONT, background="skyblue")

        self.c = tk.Label(self.inventory_tab, text="Chemicals", font=DEFAULT_FONT)
        global chemicals_
        chemicals_ = [
            "dil HCl",
            "dil NaOH",
            "lead acetate"
        ]
        self.chemical_chosen = tk.StringVar()
        self.chemical_chosen.set("Choose chemical")
        self.chemical_entry = tk.OptionMenu(self.inventory_tab, self.chemical_chosen, *chemicals_)
        menu = self.inventory_tab.nametowidget(self.chemical_entry.menuname)
        menu.config(font=DEFAULT_FONT_OBJECT)
        self.chemical_entry.config(font = DEFAULT_FONT)

        self.q1 = tk.Label(self.inventory_tab, text="Quantity", font=DEFAULT_FONT)
        self.chemical_quantity_entry = tk.Entry(self.inventory_tab, font=DEFAULT_FONT)

        self.add_chemical_button = tk.Button(self.inventory_tab, text="Add Chemical", command=self.add_chemical, font=DEFAULT_FONT, background="skyblue")

        self.apparatus_tree = ttk.Treeview(self.inventory_tab, columns=("Item", "Quantity"), show=["headings"])
        self.apparatus_tree.heading("#1", text="Apparatus") 
        self.apparatus_tree.heading("#2", text="Quantity")

        self.chemical_tree = ttk.Treeview(self.inventory_tab, columns=("Item", "Quantity"), show=["headings"])
        self.chemical_tree.heading("#1", text="Chemical")
        self.chemical_tree.heading("#2", text="Quantity")
        
        self.a.grid(row=0, column=0)
        self.c.grid(row=0, column=2)
        self.q.grid(row=1, column=0)
        self.q1.grid(row=1, column=2)

        self.apparatus_tree.grid(row=3, column=0, columnspan=2, ipadx=3, ipady=3, pady=5, padx=5)
        self.chemical_tree.grid(row=3, column=2, columnspan=2, ipadx=3, ipady=3, pady=5, padx=5)

        self.add_apparatus_button.grid(row=2, column=0, columnspan=2, pady=10, ipady=5, ipadx=3)
        self.add_chemical_button.grid(row=2, column=2, columnspan=2, pady=10, ipady=5, ipadx=3)  #apparatus and chemical side by side

        self.chemical_quantity_entry.grid(row=1, column=3) #quantity of each one below the other
        self.apparatus_quantity_entry.grid(row=1, column=1)

        self.chemical_entry.grid(row=0, column=3)
        self.apparatus_entry.grid(row=0, column=1)

        
#==================================EXPERIMENTS=====================================================#

        self.exp_name = tk.Label(self.experiments_tab, text="Experiment Name", font=DEFAULT_FONT)
        self.experiment_name_entry = tk.Entry(self.experiments_tab, font=DEFAULT_FONT)
        self.apparatus_needed = tk.Label(self.experiments_tab, text="Apparatus Needed", font=DEFAULT_FONT)
        self.apparatus_chosen_exp = tk.StringVar()
        self.apparatus_chosen_exp.set("Choose an apparatus")
        ap = apparatuses
        self.apparatus_combobox = tk.OptionMenu(self.experiments_tab, self.apparatus_chosen_exp, *ap)
        menu = self.inventory_tab.nametowidget(self.apparatus_combobox.menuname)
        menu.config(font=DEFAULT_FONT_OBJECT)
        self.apparatus_entry.config(font=DEFAULT_FONT)
        self.apparatus_combobox.config(font=DEFAULT_FONT)
        self.apparatus_quantity = tk.Label(self.experiments_tab, text="Apparatus Quantity", font=DEFAULT_FONT)
        self.experiment_apparatus_quantity_entry = tk.Entry(self.experiments_tab, font=DEFAULT_FONT)

        self.chems_needed = tk.Label(self.experiments_tab, text="Chemicals Needed", font=DEFAULT_FONT)
        self.chemical_needed_exp = tk.StringVar()
        self.chemical_needed_exp.set("Choose a chemical")
        ch = chemicals_
        self.experiment_chemicals_entry = tk.OptionMenu(self.experiments_tab, self.chemical_needed_exp, *ch)
        menu = self.inventory_tab.nametowidget(self.experiment_chemicals_entry.menuname)
        menu.config(font=DEFAULT_FONT_OBJECT)
        self.experiment_chemicals_entry.config(font=DEFAULT_FONT)
        self.chem_quantity = tk.Label(self.experiments_tab, text="Chemicals Quantity", font=DEFAULT_FONT)
        self.experiment_chemicals_quantity_entry = tk.Entry(self.experiments_tab, font=DEFAULT_FONT)

        self.add_apparatus_to_experiment_button = tk.Button(self.experiments_tab, text="Add Apparatus to Experiment", command=self.add_apparatus_to_experiment, font=DEFAULT_FONT, background="skyblue")

        self.add_chemical_to_experiment_button = tk.Button(self.experiments_tab, text="Add Chemical to Experiment", command=self.add_chemical_to_experiment, font=DEFAULT_FONT, background="skyblue")

        self.create_experiment_button = tk.Button(self.experiments_tab, text="Create Experiment", command=self.create_experiment, font=DEFAULT_FONT, pady=20, background="navyblue", foreground="white")


        self.style = ttk.Style()
        self.style.configure("Treeview.Heading", font=DEFAULT_FONT)
        self.experiments_tree = ttk.Treeview(self.experiments_tab, columns=("Experiment Name", "Apparatus Needed", "Apparatus Quantity", "Chemicals Needed", "Chemicals Quantity"), show=["headings"])
        self.experiments_tree.heading("#1", text="Experiment Name")
        self.experiments_tree.heading("#2", text="Apparatus Needed")
        self.experiments_tree.heading("#3", text="Apparatus Quantity")
        self.experiments_tree.heading("#4", text="Chemicals Needed")
        self.experiments_tree.heading("#5", text="Chemicals Quantity")

        self.exp_name.grid(row=0, column=1)
        self.experiment_name_entry.grid(row=0, column=2, pady=30)

        self.apparatus_needed.grid(row=2, column=0)
        self.apparatus_combobox.grid(row=2, column=1)
        self.chems_needed.grid(row=2, column=2, padx=50)

        self.apparatus_quantity.grid(row=3, column=0)
        self.experiment_apparatus_quantity_entry.grid(row=3, column=1)
        self.experiment_chemicals_entry.grid(row=2, column=3)
        self.chem_quantity.grid(row=3, column=2)
        self.experiment_chemicals_quantity_entry.grid(row=3, column=3)

        self.add_apparatus_to_experiment_button.grid(row=4, column=0, columnspan=2)
        self.add_chemical_to_experiment_button.grid(row=4, column=2, columnspan=2)

        self.create_experiment_button.grid(row=5, column=0, columnspan=5, sticky="ew", pady=15)
        self.experiments_tree.grid(row=6, column=0, columnspan=5)
        self.update_inventory_display()
        self.update_experiments_display()

    def add_apparatus(self):
        self.update_globals()
        print(self.inventory_tab.winfo_width())
        apparatus_name = self.apparatus_chosen.get()
        quantity = self.apparatus_quantity_entry.get()
        if apparatus_name and quantity:
            if apparatus_name in apparatus:
                apparatus[apparatus_name] += int(quantity)
                with open("db.txt", "w") as f:
                    f.write(str(apparatus) + "\n")
                    f.write(str(chemicals) + "\n")
                    f.write(str(experiments) + "\n")
            else:
                apparatus[apparatus_name] = int(quantity)
                with open("db.txt", "w") as f:
                    f.write(str(apparatus) + "\n")
                    f.write(str(chemicals) + "\n")
                    f.write(str(experiments) + "\n")
            self.update_globals()
            self.apparatus_chosen.set("Choose an apparatus")
            self.apparatus_quantity_entry.delete(0, tk.END)
            self.update_inventory_display()

    def add_chemical(self):
        self.update_globals()
        chemical_name = self.chemical_chosen.get()
        quantity = self.chemical_quantity_entry.get()
        if chemical_name and quantity:
            if chemical_name in chemicals:
                chemicals[chemical_name] += int(quantity)
                with open("db.txt", "w") as f:
                    f.write(str(apparatus) + "\n")
                    f.write(str(chemicals) + "\n")
                    f.write(str(experiments) + "\n")
            else:
                chemicals[chemical_name] = int(quantity)
                with open("db.txt", "w") as f:
                    f.write(str(apparatus) + "\n")
                    f.write(str(chemicals) + "\n")
                    f.write(str(experiments) + "\n")
            self.chemical_chosen.set("Choose a chemical")
            self.chemical_quantity_entry.delete(0, tk.END)
            self.update_inventory_display()
            

    def add_apparatus_to_experiment(self):
        self.update_globals()
        apparatus_name = self.apparatus_chosen_exp.get()
        self.apparatus_chosen.set("Choose an Apparatus")
        quantity = self.experiment_apparatus_quantity_entry.get()
        experiment_name = self.experiment_name_entry.get()
        if experiment_name and apparatus_name and quantity:
            if experiment_name in experiments:
                if 'Apparatus Needed' not in experiments[experiment_name]:
                    experiments[experiment_name]['Apparatus Needed'] = {}
                    with open("db.txt", "w") as f:
                        f.write(str(apparatus) + "\n")
                        f.write(str(chemicals) + "\n")
                        f.write(str(experiments) + "\n")
                experiments[experiment_name]['Apparatus Needed'][apparatus_name] = int(quantity)
                with open("db.txt", "w") as f:
                    f.write(str(apparatus) + "\n")
                    f.write(str(chemicals) + "\n")
                    f.write(str(experiments) + "\n")
                self.experiment_apparatus_quantity_entry.delete(0, tk.END)
                self.update_experiments_display()

    def add_chemical_to_experiment(self):
        chemical_name = self.experiment_chemicals_entry.get()
        quantity = self.experiment_chemicals_quantity_entry.get()
        experiment_name = self.experiment_name_entry.get()
        if experiment_name and chemical_name and quantity:
            if experiment_name in experiments:
                if 'Chemicals Needed' not in experiments[experiment_name]:
                    experiments[experiment_name]['Chemicals Needed'] = {}
                    with open("db.txt", "w") as f:
                        f.write(str(apparatus) + "\n")
                        f.write(str(chemicals) + "\n")
                        f.write(str(experiments) + "\n")
                experiments[experiment_name]['Chemicals Needed'][chemical_name] = int(quantity)
                with open("db.txt", "w") as f:
                    f.write(str(apparatus) + "\n")
                    f.write(str(chemicals) + "\n")
                    f.write(str(experiments) + "\n")
                self.experiment_chemicals_entry.delete(0, tk.END)
                self.experiment_chemicals_quantity_entry.delete(0, tk.END)
                self.update_experiments_display()

    def create_experiment(self):
        self.update_globals()
        experiment_name = self.experiment_name_entry.get()
        if experiment_name:
            if experiment_name not in experiments:
                experiments[experiment_name] = {
                    'Apparatus Needed': {},
                    'Chemicals Needed': {},
                }
                with open("db.txt", "w") as f:
                    f.write(str(apparatus) + "\n")
                    f.write(str(chemicals) + "\n")
                    f.write(str(experiments) + "\n")

            apparatus_needed = self.apparatus_chosen_exp.get()
            chemicals_needed = self.chemical_needed_exp.get()
            apparatus_quantity = self.experiment_apparatus_quantity_entry.get()
            chemicals_quantity = self.experiment_chemicals_quantity_entry.get()

            if apparatus_needed and apparatus_quantity:
                experiments[experiment_name]['Apparatus Needed'][apparatus_needed] = int(apparatus_quantity)
                with open("db.txt", "w") as f:
                    f.write(str(apparatus) + "\n")
                    f.write(str(chemicals) + "\n")
                    f.write(str(experiments) + "\n")

            if chemicals_needed and chemicals_quantity:
                experiments[experiment_name]['Chemicals Needed'][chemicals_needed] = int(chemicals_quantity)
                with open("db.txt", "w") as f:
                    f.write(str(apparatus) + "\n")
                    f.write(str(chemicals) + "\n")
                    f.write(str(experiments) + "\n")

            self.experiment_name_entry.delete(0, tk.END)
            self.experiment_apparatus_quantity_entry.delete(0, tk.END)
            self.experiment_chemicals_entry.delete(0, tk.END)
            self.experiment_chemicals_quantity_entry.delete(0, tk.END)

            self.update_experiments_display()
        print(apparatus)
        print(chemicals)
        print(experiments)

    def update_inventory_display(self):
        self.update_globals()

        # self.apparatus_combobox = list(apparatus.keys())

        self.apparatus_tree.delete(*self.apparatus_tree.get_children())
        self.chemical_tree.delete(*self.chemical_tree.get_children())

        for item, quantity in apparatus.items():
            self.apparatus_tree.insert("", tk.END, values=(item, quantity)) # changed from "end" to tk.END
        for item, quantity in chemicals.items():
            self.chemical_tree.insert("", tk.END, values=(item, quantity))

    def update_experiments_display(self):
        self.experiments_tree.delete(*self.experiments_tree.get_children())
        self.update_globals()
        for experiment_name, experiment_info in experiments.items():
            apparatus_needed_items = experiment_info.get('Apparatus Needed', {}).items()
            chemicals_needed_items = experiment_info.get('Chemicals Needed', {}).items()

            apparatus_needed = ', '.join([f'{k}' for k, v in apparatus_needed_items])
            apparatus_quantity = ', '.join([str(v) for k, v in apparatus_needed_items])
            chemicals_needed = ', '.join([f'{k}' for k, v in chemicals_needed_items])
            chemicals_quantity = ', '.join([str(v) for k, v in chemicals_needed_items])

            self.experiments_tree.insert("", "end", values=(experiment_name, apparatus_needed, apparatus_quantity, chemicals_needed, chemicals_quantity))
    
    def update_globals(self):
        with open("db.txt") as f:
            L = f.readlines()
            global apparatus
            apparatus = eval(L[0])
            global chemicals
            chemicals = eval(L[1])
            global experiments
            experiments = eval(L[2])

#===========================================================================#

class AdminLoginPage:
    def __init__(self, root):
        self.root = root
        self.root.title("Admin Login")
        self.root.bind("<Return>", self.login)
        root.resizable(False, False)
        
        # admin pg size
        self.root.geometry("500x600")
        
        # canvas for admin background
        self.canvas = tk.Canvas(self.root, width=500, height=600)
        self.canvas.grid(row=0, column=0, rowspan=4, columnspan=2) #canvas in grid
        
        self.color()
        
        # password
        self.f = tk.Frame(background="skyblue")
        self.label_password = tk.Label(self.f, text="Admin Password:", background= "skyblue", font=("SF Pro Display", 15)) 
        self.entry_password = tk.Entry(self.f, show="*", background= "white", font=("SF Pro Display", 15))
        self.entry_password.grid(row=0, column=1, sticky="w")
        
        # login
        self.info = tk.Label(self.root, text="", background="skyblue", font=DEFAULT_FONT, foreground="red")
        self.login_button = tk.Button(self.root, text="Login", command=self.login, font=("SF Pro Display", 15), background="navyblue", foreground="white")
        
        # admin pg grid 
        self.f.grid(row=1, column=1, sticky = "ew")
        self.label_password.grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.entry_password.grid(row=1, column=1, padx=10, pady=5, ipadx=5, sticky="ew")
        self.login_button.grid(row=2, column=0, columnspan=2, padx=10, ipady=7, sticky="ew")
        self.info.place(x=133, y=300)

        self.root.geometry()
        
    #     self.center_window()
    # def center_window(self):
    #     # screen dimensions
    #     screen_width = self.root.winfo_screenwidth()
    #     screen_height = self.root.winfo_screenheight()
        
    #     # center
    #     x = (screen_width - 500) // 2
    #     y = (screen_height - 600) // 2
        
    #     self.root.geometry("500x600+{}+{}".format(x, y))
    
    def color(self):
        self.canvas.configure(bg = "skyblue")
    
    def login(self, e=None):
        password = self.entry_password.get()
        if password == admin_password:
            self.root.destroy()  #close admin pg
            lab_root = tk.Tk()
            lab_app = LabManagementSystem(lab_root)
            lab_root.mainloop()
        else:
            self.display_message("Incorrect Admin Password")
    
    def display_message(self, message):
        self.info["text"] = message
        print(self.info.winfo_width())

if __name__ == "__main__":
    root = tk.Tk()
    app = AdminLoginPage(root)
    root.mainloop()