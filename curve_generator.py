import os
import math
import json
import tkinter as tk
from tkinter import messagebox
import urllib.request
import webbrowser
import customtkinter as ctk

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

CURRENT_VERSION = "v2.1.0"
GITHUB_REPO = "ROYALKINGSJ/Affinity_Math_Curves" 

class CustomFunctionDialog(ctk.CTkToplevel):
    # ... [Keep your existing CustomFunctionDialog code exactly as it was] ...
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Custom Math Function")
        self.geometry("400x300")
        self.resizable(False, False)
        self.result = None
        
        self.transient(parent)
        self.grab_set()

        ctk.CTkLabel(self, text="Enter a mathematical equation using 'x'", font=ctk.CTkFont(weight="bold", size=14)).pack(pady=(20, 5))
        
        examples = "Examples:\n- sin(x) + cos(2*x)\n- x**2 * 0.1\n- tan(x) * sin(x)"
        ctk.CTkLabel(self, text=examples, justify="left").pack(pady=5)

        link_label = ctk.CTkLabel(self, text="Test your function on Mathway first \u2197", text_color="#1f6aa5", cursor="hand2")
        link_label.pack(pady=5)
        link_label.bind("<Button-1>", lambda e: webbrowser.open("https://www.mathway.com/Graph"))

        self.entry = ctk.CTkEntry(self, width=250, placeholder_text="e.g., sin(x) * 2")
        self.entry.pack(pady=15)
        self.entry.focus_set()
        self.entry.bind("<Return>", lambda e: self.submit())

        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(pady=10)
        ctk.CTkButton(btn_frame, text="OK", width=100, command=self.submit).pack(side="left", padx=10)
        ctk.CTkButton(btn_frame, text="Cancel", width=100, fg_color="gray", hover_color="#555555", command=self.destroy).pack(side="left", padx=10)

        self.wait_window(self)

    def submit(self):
        self.result = self.entry.get()
        self.destroy()

class CurveGeneratorApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title(f"Live Math Curve Generator ({CURRENT_VERSION})")
        self.geometry("600x850") 
        
        # --- NATIVE MENU BAR SETUP ---
        self.menubar = tk.Menu(self)
        
        # Create a "Help" menu dropdown
        self.help_menu = tk.Menu(self.menubar, tearoff=0)
        self.help_menu.add_command(label="Check for Updates", command=lambda: self.check_github_updates(manual_check=True))
        self.help_menu.add_separator()
        self.help_menu.add_command(label="About", command=lambda: messagebox.showinfo("About", "Affinity Math Curve Generator\nCreated by ROYALKINGSJ"))
        
        # Add the dropdown to the main menu bar
        self.menubar.add_cascade(label="Help", menu=self.help_menu)
        
        # Apply the menu to the window
        self.config(menu=self.menubar)
        # -----------------------------

        # Run a silent update check on startup
        self.check_github_updates(manual_check=False)

        # --- UI Layout ---
        title_label = ctk.CTkLabel(self, text="Live Math Curve Generator", font=ctk.CTkFont(size=20, weight="bold"))
        title_label.pack(pady=(20, 15))

        # 1. Function Selection
        func_frame = ctk.CTkFrame(self, fg_color="transparent")
        func_frame.pack(pady=5)
        
        self.func_list = ["Sine (sin)", "Cosine (cos)", "Tangent (tan)", "Cosecant (cosec)", "Secant (sec)", "Cotangent (cot)"]
        self.func_var = ctk.StringVar(value=self.func_list[0])
        
        self.func_menu = ctk.CTkOptionMenu(func_frame, variable=self.func_var, values=self.func_list, command=self.redraw_preview, width=200)
        self.func_menu.pack(side="left", padx=10)

        self.add_btn = ctk.CTkButton(func_frame, text="Add Custom", width=100, command=self.add_custom_function)
        self.add_btn.pack(side="left")

        # 2. Controls Frame
        controls_frame = ctk.CTkFrame(self)
        controls_frame.pack(pady=15, padx=30, fill="x")

        # Step Size
        step_frame = ctk.CTkFrame(controls_frame, fg_color="transparent")
        step_frame.pack(pady=(10, 5), fill="x", padx=15)
        ctk.CTkLabel(step_frame, text="Slider Step Size:").pack(side="left")
        self.step_var = ctk.StringVar(value="0.1")
        self.step_entry = ctk.CTkEntry(step_frame, textvariable=self.step_var, width=60)
        self.step_entry.pack(side="right")
        self.step_entry.bind("<KeyRelease>", self.update_steps)

        # Amplitude
        amp_frame = ctk.CTkFrame(controls_frame, fg_color="transparent")
        amp_frame.pack(pady=5, fill="x", padx=15)
        ctk.CTkLabel(amp_frame, text="Amplitude:").pack(side="left", padx=(0, 10))
        self.amp_var = ctk.DoubleVar(value=50.0)
        self.amp_slider = ctk.CTkSlider(amp_frame, from_=-100, to=100, variable=self.amp_var, command=self.redraw_preview)
        self.amp_slider.pack(side="left", fill="x", expand=True, padx=10)
        self.amp_entry = ctk.CTkEntry(amp_frame, textvariable=self.amp_var, width=60)
        self.amp_entry.pack(side="right")
        self.amp_entry.bind("<Return>", lambda e: self.redraw_preview())

        # Frequency
        freq_frame = ctk.CTkFrame(controls_frame, fg_color="transparent")
        freq_frame.pack(pady=(5, 15), fill="x", padx=15)
        ctk.CTkLabel(freq_frame, text="Frequency:").pack(side="left", padx=(0, 10))
        self.freq_var = ctk.DoubleVar(value=2.0)
        self.freq_slider = ctk.CTkSlider(freq_frame, from_=-100, to=100, variable=self.freq_var, command=self.redraw_preview)
        self.freq_slider.pack(side="left", fill="x", expand=True, padx=10)
        self.freq_entry = ctk.CTkEntry(freq_frame, textvariable=self.freq_var, width=60)
        self.freq_entry.pack(side="right")
        self.freq_entry.bind("<Return>", lambda e: self.redraw_preview())

        # 3. Canvas Toggles (Axes & Grid)
        toggle_frame = ctk.CTkFrame(self, fg_color="transparent")
        toggle_frame.pack(pady=5)
        self.show_grid_var = ctk.BooleanVar(value=True)
        self.show_axes_var = ctk.BooleanVar(value=True)
        
        ctk.CTkCheckBox(toggle_frame, text="Show Grid", variable=self.show_grid_var, command=self.redraw_preview).pack(side="left", padx=15)
        ctk.CTkCheckBox(toggle_frame, text="Show Axes (X/Y)", variable=self.show_axes_var, command=self.redraw_preview).pack(side="left", padx=15)

        # 4. Canvas
        self.canvas_width = 500
        self.canvas_height = 250
        canvas_border = ctk.CTkFrame(self, border_width=2)
        canvas_border.pack(pady=10)
        self.canvas = tk.Canvas(canvas_border, width=self.canvas_width, height=self.canvas_height, bg="white", highlightthickness=0)
        self.canvas.pack(padx=2, pady=2)

        # 5. Export Section
        export_frame = ctk.CTkFrame(self, fg_color="transparent")
        export_frame.pack(pady=(15, 5))
        ctk.CTkLabel(export_frame, text="Output File Name:").pack(side="left", padx=10)
        self.file_entry = ctk.CTkEntry(export_frame, width=150)
        self.file_entry.insert(0, "math_curve.svg")
        self.file_entry.pack(side="left")

        self.generate_btn = ctk.CTkButton(self, text="Export Vector to SVG", height=40, font=ctk.CTkFont(weight="bold"), command=self.generate_svg)
        self.generate_btn.pack(pady=15)

        self.update_steps()
        self.redraw_preview()

    def check_github_updates(self, manual_check=False):
        url = f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=3) as response:
                data = json.loads(response.read().decode())
                latest_version = data.get("tag_name", CURRENT_VERSION)
                
                if latest_version != CURRENT_VERSION:
                    # Ask user if they want to download the update
                    answer = messagebox.askyesno(
                        "Update Available!", 
                        f"Version {latest_version} is available on GitHub!\nYou are running {CURRENT_VERSION}.\n\nWould you like to download the new version?"
                    )
                    if answer:
                        webbrowser.open(f"https://github.com/{GITHUB_REPO}/releases/latest")
                elif manual_check:
                    messagebox.showinfo("Up to Date", f"You are running the latest version ({CURRENT_VERSION}).")
        except Exception:
            if manual_check:
                messagebox.showerror("Network Error", "Could not connect to GitHub to check for updates.")

    def update_steps(self, event=None):
        try:
            step_val = float(self.step_var.get())
            if step_val > 0:
                self.amp_slider.configure(number_of_steps=int(200/step_val))
                self.freq_slider.configure(number_of_steps=int(200/step_val))
        except ValueError:
            pass

    def add_custom_function(self):
        dialog = CustomFunctionDialog(self)
        custom_eq = dialog.result
        if custom_eq:
            self.func_list.append(custom_eq)
            self.func_menu.configure(values=self.func_list)
            self.func_var.set(custom_eq)
            self.redraw_preview(None)

    def calculate_y(self, func_type, radians, amplitude):
        try:
            if func_type == "Sine (sin)": return math.sin(radians) * amplitude
            elif func_type == "Cosine (cos)": return math.cos(radians) * amplitude
            elif func_type == "Tangent (tan)": return math.tan(radians) * amplitude
            elif func_type == "Cosecant (cosec)": return (1 / math.sin(radians)) * amplitude
            elif func_type == "Secant (sec)": return (1 / math.cos(radians)) * amplitude
            elif func_type == "Cotangent (cot)": return (1 / math.tan(radians)) * amplitude
            else:
                safe_math = {k: v for k, v in math.__dict__.items() if not k.startswith("__")}
                safe_math["x"] = radians
                return eval(func_type, {"__builtins__": None}, safe_math) * amplitude
        except Exception:
            return None

    def draw_axes_and_grid(self, mid_x, mid_y):
        grid_spacing = 50
        if self.show_grid_var.get():
            for i in range(0, self.canvas_width, grid_spacing):
                self.canvas.create_line(i, 0, i, self.canvas_height, fill="#e5e5e5", dash=(2, 2))
            for i in range(0, self.canvas_height, grid_spacing):
                self.canvas.create_line(0, i, self.canvas_width, i, fill="#e5e5e5", dash=(2, 2))
        if self.show_axes_var.get():
            self.canvas.create_line(0, mid_y, self.canvas_width, mid_y, fill="black", width=1.5)
            self.canvas.create_line(mid_x, 0, mid_x, self.canvas_height, fill="black", width=1.5)
            for i in range(0, self.canvas_width, grid_spacing):
                if i != mid_x:
                    self.canvas.create_line(i, mid_y - 4, i, mid_y + 4, fill="black")
                    val = (i - mid_x) / grid_spacing
                    self.canvas.create_text(i, mid_y + 12, text=str(int(val)), fill="#555555", font=("Arial", 8))
            for i in range(0, self.canvas_height, grid_spacing):
                if i != mid_y:
                    self.canvas.create_line(mid_x - 4, i, mid_x + 4, i, fill="black")
                    val = -(i - mid_y) / grid_spacing
                    self.canvas.create_text(mid_x - 12, i, text=str(int(val)), fill="#555555", font=("Arial", 8))

    def redraw_preview(self, event=None):
        self.canvas.delete("all")
        mid_x = self.canvas_width / 2
        mid_y = self.canvas_height / 2
        self.draw_axes_and_grid(mid_x, mid_y)
        
        func = self.func_var.get()
        try:
            amp = round(float(self.amp_var.get()), 3)
            freq = round(float(self.freq_var.get()), 3)
        except ValueError:
            return

        points = []
        for x in range(self.canvas_width):
            real_x = x - mid_x
            radians = (real_x / self.canvas_width) * 2 * math.pi * freq
            y_offset = self.calculate_y(func, radians, amp)
            
            if y_offset is None or abs(y_offset) > self.canvas_height * 2:
                if len(points) > 1:
                    self.canvas.create_line(points, fill="#0052cc", width=2, smooth=True)
                points = [] 
                continue
                
            actual_y = mid_y - y_offset
            points.append((x, actual_y))
            
        if len(points) > 1:
            self.canvas.create_line(points, fill="#0052cc", width=2, smooth=True)

    def generate_svg(self):
        func = self.func_var.get()
        try:
            amp = round(float(self.amp_var.get()), 3)
            freq = round(float(self.freq_var.get()), 3)
        except ValueError:
            messagebox.showerror("Input Error", "Check your amplitude and frequency values.")
            return
            
        filename = self.file_entry.get()
        mid_x = self.canvas_width / 2
        mid_y = self.canvas_height / 2
        svg_header = f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.canvas_width}" height="{self.canvas_height}">\n'
        svg_footer = '</svg>'
        
        path_data = ""
        started = False

        for x in range(self.canvas_width):
            real_x = x - mid_x
            radians = (real_x / self.canvas_width) * 2 * math.pi * freq
            y_offset = self.calculate_y(func, radians, amp)

            if y_offset is None or abs(y_offset) > self.canvas_height * 2:
                started = False
                continue

            actual_y = mid_y - y_offset

            if not started:
                path_data += f"M {x} {actual_y} "
                started = True
            else:
                path_data += f"L {x} {actual_y} "

        path_element = f'<path d="{path_data}" fill="none" stroke="black" stroke-width="2"/>\n'

        try:
            with open(filename, 'w') as f:
                f.write(svg_header + path_element + svg_footer)
            messagebox.showinfo("Success", f"Saved successfully as '{filename}'!")
        except Exception as e:
            messagebox.showerror("File Error", f"Could not save file: {e}")

if __name__ == "__main__":
    app = CurveGeneratorApp()
    app.mainloop()