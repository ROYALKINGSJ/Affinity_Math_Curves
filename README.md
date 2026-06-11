# Affinity Math Curve Generator

> **⚠️ Important Note from the Developer:**
> **Building from source is highly recommended.** Due to cross-compilation hardware limitations, pre-built binary releases are primarily provided for Apple Silicon Macs. Windows and Linux versions are not included in the releases and must be compiled locally from source. Additionally, pre-built updates for Intel Macs will likely be deprecated in the future.

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

### Option 1: Download the Pre-built App (Mac Apple Silicon)
1. Go to the [Releases](../../releases) page on this GitHub repository.
2. Download the `.zip` file for your operating system (if available).
3. Extract the file and double-click the application icon to run it. No terminal required!

### Option 2: Build from Source (Highly Recommended)
If you want to run this on Windows, Linux, or Intel Macs, or if you want to modify the code yourself, you should build it directly using Python (v3.13+ recommended).

**1. Clone the repository and navigate to the folder:**
```bash
git clone [https://github.com/ROYALKINGSJ/Affinity_Math_Curves.git](https://github.com/ROYALKINGSJ/Affinity_Math_Curves.git)
cd Affinity_Math_Curves
```

**2. Install the required dependencies:**
```bash
pip install customtkinter Pillow pyinstaller
```
*(Note for Mac/Linux users: You may need to use `pip3` instead of `pip` depending on your environment).*

**3. Compile the standalone application:**
Run PyInstaller to package the script into a native OS application. Make sure to replace the path with the actual absolute path to your downloaded script.

* **For Mac:**
  ```bash
  pyinstaller --noconfirm --onedir --windowed --noconsole "/Users/your_username/Desktop/Affinity_Math_Curves/curve_generator.py"
  ```
* **For Windows:**
  ```cmd
  pyinstaller --noconfirm --onedir --windowed --noconsole "C:\Users\YourUsername\Desktop\Affinity_Math_Curves\curve_generator.py"
  ```
* **For Linux:**
  ```bash
  pyinstaller --noconfirm --onedir --windowed --noconsole "/home/your_username/Desktop/Affinity_Math_Curves/curve_generator.py"
  ```

Once the process finishes, your runnable application will be located inside the newly generated `dist` folder.

---

## Usage
1. Select a built-in mathematical curve from the dropdown, or click **Add Custom** to write your own equation using `x`.
2. Use the sliders or text boxes to adjust the **Amplitude** (height) and **Frequency** (density) of the wave.
3. Type your desired output file name.
4. Click **Export Curve Data** and choose your preferred format (SVG, EPS, PNG, JPEG, or CSV).
5. Drag and drop the exported file straight into your design software!

---

## Support the Project
If this tool helped speed up your design workflow, consider supporting its continued development!
☕ **[Support me on Patreon](https://patreon.com/TECHCOM?utm_medium=unknown&utm_source=join_link&utm_campaign=creatorshare_creator&utm_content=copyLink)**