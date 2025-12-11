import tkinter as tk
from tkinter import messagebox, ttk
import json
import os
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

class BMICalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced BMI Calculator")
        self.data_file = "bmi_history.json"
        self.users_data = self.load_data()
        
        self.setup_ui()
    
    def load_data(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as f:
                return json.load(f)
        return {}
    
    def save_data(self):
        with open(self.data_file, 'w') as f:
            json.dump(self.users_data, f, indent=4)
    
    def setup_ui(self):
        # Input frame
        input_frame = ttk.Frame(self.root, padding="10")
        input_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        ttk.Label(input_frame, text="Weight (kg):").grid(row=0, column=0)
        self.weight_entry = ttk.Entry(input_frame)
        self.weight_entry.grid(row=0, column=1)
        
        ttk.Label(input_frame, text="Height (m):").grid(row=1, column=0)
        self.height_entry = ttk.Entry(input_frame)
        self.height_entry.grid(row=1, column=1)
        
        ttk.Button(input_frame, text="Calculate BMI", 
                  command=self.calculate).grid(row=2, column=0, columnspan=2, pady=10)
        
        # Results frame
        self.result_frame = ttk.Frame(self.root, padding="10")
        self.result_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.result_label = ttk.Label(self.result_frame, text="", font=("Arial", 12, "bold"))
        self.result_label.grid(row=0, column=0)
        
        self.category_label = ttk.Label(self.result_frame, text="")
        self.category_label.grid(row=1, column=0)
        
        # History frame
        ttk.Button(self.root, text="View History", 
                  command=self.show_history).grid(row=2, column=0, pady=10)
    
    def calculate(self):
        try:
            weight = float(self.weight_entry.get())
            height = float(self.height_entry.get())
            
            if weight <= 0 or height <= 0:
                raise ValueError("Values must be positive")
            
            bmi = weight / (height ** 2)
            category = self.get_category(bmi)
            
            self.result_label.config(text=f"BMI: {bmi:.2f}")
            self.category_label.config(text=f"Category: {category}")
            
            # Save to history
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
            user_id = f"user_{len(self.users_data) + 1}"
            if user_id not in self.users_data:
                self.users_data[user_id] = []
            self.users_data[user_id].append({"date": timestamp, "bmi": bmi})
            self.save_data()
            
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))
    
    def get_category(self, bmi):
        if bmi < 18.5: return "Underweight"
        elif bmi < 25: return "Normal"
        elif bmi < 30: return "Overweight"
        else: return "Obese"
    
    def show_history(self):
        history_window = tk.Toplevel(self.root)
        history_window.title("BMI History")
        
        tree = ttk.Treeview(history_window, columns=("User", "Date", "BMI"), show="headings")
        tree.heading("User", text="User")
        tree.heading("Date", text="Date")
        tree.heading("BMI", text="BMI")
        
        for user_id, records in self.users_data.items():
            for record in records:
                tree.insert("", "end", values=(user_id, record["date"], f"{record['bmi']:.2f}"))
        
        tree.pack(pady=10)
        
        ttk.Button(history_window, text="Show Trend Chart", 
                  command=lambda: self.show_trend_chart()).pack()

    def show_trend_chart(self):
        fig, ax = plt.subplots()
        for user_id, records in self.users_data.items():
            dates = [r["date"] for r in records]
            bmis = [r["bmi"] for r in records]
            ax.plot(dates, bmis, marker='o', label=user_id)
        
        ax.set_xlabel("Date")
        ax.set_ylabel("BMI")
        ax.legend()
        ax.grid(True)
        
        chart_window = tk.Toplevel(self.root)
        canvas = FigureCanvasTkAgg(fig, chart_window)
        canvas.draw()
        canvas.get_tk_widget().pack()

if __name__ == "__main__":
    root = tk.Tk()
    app = BMICalculator(root)
    root.mainloop()
