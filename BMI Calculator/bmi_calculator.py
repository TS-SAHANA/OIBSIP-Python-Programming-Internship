import tkinter as tk
from tkinter import messagebox, PhotoImage
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageTk
from tkinter import font
import matplotlib.pyplot as plt

class BMI_Calculator:
    def __init__(self, master):
        self.master = master
        self.master.title("BMI Calculator")

        # File Initialization
        self.file_path = "bmi_data.txt"
        
        # Center the window and set the size
        window_width = 626
        window_height = 626
        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        master.geometry(f"{window_width}x{window_height}+{x}+{y}")
        master.resizable(False, False)

        # Load background image
        try:
            self.background_image = PhotoImage(file="background.png")
        except tk.TclError as e:
            messagebox.showerror("Error", f"Couldn't recognize data in image file: {e}")

        # Set up a label to display the background image
        background_label = tk.Label(master, image=self.background_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Define a custom font
        custom_font = font.Font(family="Helvetica", size=12, weight="bold")

        # GUI Components
        self.weight_label = tk.Label(master, text="Enter Weight (kg):", bg='lightblue1', font=custom_font)
        self.weight_label.place(relx=0.5, rely=0.1, anchor="center")

        self.weight_entry = tk.Entry(master, font=custom_font)
        self.weight_entry.place(relx=0.5, rely=0.15, anchor="center")

        self.height_label = tk.Label(master, text="Enter Height (cm):", bg='lightblue1', font=custom_font)
        self.height_label.place(relx=0.5, rely=0.2, anchor="center")

        self.height_entry = tk.Entry(master, font=custom_font)
        self.height_entry.place(relx=0.5, rely=0.25, anchor="center")

        result_font = font.Font(family="Helvetica", size=14, weight="bold", slant="italic")
        self.result_label = tk.Label(master, text="", bg="lightblue1", font=result_font)
        self.result_label.place(relx=0.5, rely=0.32, anchor="center")

        # Calculate BMI Button
        button_font = font.Font(family="Helvetica", size=12, weight="bold")
        self.calculate_button = tk.Button(master, text="Calculate BMI", command=self.calculate_bmi, bg="steelblue3", font=button_font)
        self.calculate_button.place(relx=0.5, rely=0.4, anchor="center")

        # Data Visualization Button
        self.view_data_button = tk.Button(master, text="View Historical Data", command=self.view_historical_data, bg="steelblue3", font=button_font)
        self.view_data_button.place(relx=0.5, rely=0.48, anchor="center")

         #Load background image
        try:
            original_image = Image.open("bmi_image.png")
            resized_image = original_image.resize((200, 200), Image.ANTIALIAS)
            self.new_image = ImageTk.PhotoImage(resized_image)
        except (FileNotFoundError, OSError) as e:
            messagebox.showerror("Error", f"Couldn't recognize data in image file: {e}")

        # Set up a label to display the background image
        new_label = tk.Label(master, image=self.new_image)
        new_label.place(x=3, y=3,rely=0.7, relx=0.5, anchor='center')
        
    def categorize_bmi(self, bmi):
        if bmi < 18.5:
            return "Underweight"
        elif 18.5 <= bmi < 24.9:
            return "Normal Weight"
        elif 25 <= bmi < 29.9:
            return "Overweight"
        else:
            return "Obese"


    def calculate_bmi(self):
        try:
            weight = float(self.weight_entry.get())
            height = float(self.height_entry.get()) / 100.0  # convert to meters
            bmi = weight / (height ** 2)

            # Categorize BMI
            category = self.categorize_bmi(bmi)

            result_text = f"Your BMI: {bmi:.2f}\nCategory: {category}"
            self.result_label.config(text=result_text)

            # Save data to the file
            self.save_to_file(weight, height, bmi)

        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter valid numbers.")

    def save_to_file(self, weight, height, bmi):
        with open(self.file_path, "a") as file:
            file.write(f"{weight},{height},{bmi}\n")

    def view_historical_data(self):
        try:
            # Read historical data from the file
            with open(self.file_path, "r") as file:
                data = [line.strip().split(",") for line in file]

            if not data:
                messagebox.showinfo("No Data", "No historical BMI data available.")
                return

            # Create a new window for historical data visualization
            data_window = tk.Toplevel(self.master)
            data_window.title("Historical Data")
            data_window.geometry("800x600")  # Set a default size

            # Plot the data using Matplotlib in the new window
            weights = [float(row[0]) for row in data]
            heights = [float(row[1]) for row in data]
            bmis = [float(row[2]) for row in data]

            fig, axs = plt.subplots(3, 1, figsize=(8, 8))
            fig.suptitle("Historical BMI Data")

            axs[0].plot(weights, marker='o', linestyle='-')
            axs[0].set_ylabel('Weight (kg)')

            axs[1].plot(heights, marker='o', linestyle='-', color='r')
            axs[1].set_ylabel('Height (cm)')

            axs[2].plot(bmis, marker='o', linestyle='-', color='g')
            axs[2].set_ylabel('BMI')

            plt.tight_layout()
            canvas = FigureCanvasTkAgg(fig, master=data_window)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        except FileNotFoundError:
            messagebox.showinfo("No Data", "No historical BMI data available.")

def main():
    root = tk.Tk()
    bmi_calculator = BMI_Calculator(root)
    root.mainloop()

if __name__ == "__main__":
    main()