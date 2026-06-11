# Affinity Math Curve Generator

## About the Project
This is a standalone Python application designed to generate mathematically perfect curves (like Sine, Cosine, Parabolas, etc.) for vector design workflows. 

Because Affinity Designer currently lacks built-in tools for generating specific mathematical curves and does not support interactive UI plugins (as of mid-2026), this tool serves as a lightweight, native bridge. You can visually tweak parameters, plot custom equations, and instantly export the results as infinitely scalable vectors or high-res images to drag and drop directly into your Affinity canvas.

## Features
* **Live Visual Preview:** See your math rendered in real-time before you export, complete with togglable axes and grid lines.
* **Standard & Custom Functions:** Comes with built-in trigonometric functions (sin, cos, tan, etc.), plus a custom equation parser to type your own math (e.g., `sin(x) + cos(2*x)`).
* **Multiple Export Formats:** * `SVG` & `EPS` (Perfect for importing into Affinity Designer/Illustrator)
  * `PNG` & `JPEG` (Standard image formats)
  * `CSV` (Raw X/Y coordinate data points)
* **Modern UI:** Built with CustomTkinter to match your system's native Dark or Light mode.
* **Auto-Updates:** Native menu-bar checker alerts you when new versions are published to GitHub.

---

## Installation

There are two ways to get the app running on your machine:

### Option 1: Download the Pre-built App (Recommended)
The easiest way to use the generator is to download the ready-to-use application.
1. Go to the [Releases](../../releases) page on this GitHub repository.
2. Download the `.zip` file for your operating system (e.g., Mac Apple Silicon, Mac Intel, or Windows).
3. Extract the file and double-click the application icon to run it. No terminal required!

### Option 2: Build from Source
If you want to modify the code, add your own features, or compile the app yourself, you can build it directly using Python (v3.13+ recommended).

**1. Clone the repository and navigate to the folder:**
bash
git clone https://github.com/ROYALKINGSJ/Affinity_Math_Curves.git
cd Affinity_Math_Curves


**2. Install the required dependencies:**
bash
pip install customtkinter Pillow pyinstaller


**3. Compile the standalone application:**
Run PyInstaller to package the script into a native OS application. Make sure to replace `"PATH"` with the actual absolute path to your script:
bash
pyinstaller --noconfirm --onedir --windowed --noconsole "PATH/curve_generator.py"

*(Example for Mac):*
bash
pyinstaller --noconfirm --onedir --windowed --noconsole /Users/macbook/Desktop/Affinity_Math_Curves/curve_generator.py


Once finished, your runnable application will be located inside the newly generated `dist` folder.

---

## Usage
1. Select a built-in mathematical curve from the dropdown, or click **Add Custom** to write your own equation using `x`.
2. Use the sliders or text boxes to adjust the **Amplitude** (height) and **Frequency** (density) of the wave.
3. Type your desired output file name.
4. Click **Export Curve Data** and choose your preferred format (SVG, EPS, PNG, JPEG, or CSV).
5. Drag and drop the exported file straight into your design software!