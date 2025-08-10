import tkinter as tk
from tkinter import filedialog, messagebox, ttk, scrolledtext
from PIL import Image, ImageDraw, ImageFont
import pandas as pd
import os
from fpdf import FPDF
import re
import webbrowser

class CertificateGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Certificate Generator")
        self.root.geometry("600x400")

        # Add icon (must be .ico format on Windows)
        try:
            # Windows .ico
            self.root.iconbitmap('appicon.ico')
            # Cross-platform fallback
            # img = tk.PhotoImage(file='appicon.png')
            # self.root.tk.call('wm', 'iconphoto', self.root._w, img)
        except Exception as e:
            print(f"Icon not loaded: {e}")
        
        # Font options
        self.font_options = [
            "Ephesis-Regular.ttf",
            "BonheurRoyale-Regular.ttf",
            "Schoolbell-Regular.ttf",
            "Birthstone-Regular.ttf",
            "Hurricane-Regular.ttf"
        ]
        
        # Variables
        self.csv_path = tk.StringVar()
        self.template_path_3k = tk.StringVar(value="3km.jpg")
        self.template_path_5k = tk.StringVar(value="5km.jpg")
        self.output_dir = tk.StringVar(value="output_certificates")
        self.font_path = tk.StringVar(value=self.font_options[0])  # Default to first font
        self.font_size = tk.IntVar(value=128)
        self.font_color = (0, 0, 0)  # Black
        self.y_position = tk.IntVar(value=580)
        
        # Create UI
        self.create_widgets()

        # Show README
        self.show_readme()
    
    def show_readme(self):
        readme_path = os.path.join(os.path.dirname(__file__), "README.html")
        webbrowser.open(f"file://{readme_path}")

    def create_widgets(self):
        # File Selection Frame
        file_frame = ttk.LabelFrame(self.root, text="File Selection", padding=10)
        file_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(file_frame, text="Select CSV File", command=self.select_csv).grid(row=0, column=0, sticky=tk.W, pady=5)
        ttk.Label(file_frame, textvariable=self.csv_path).grid(row=0, column=1, sticky=tk.W)
        
        ttk.Button(file_frame, text="Select 3KM Template", command=lambda: self.select_template("3k")).grid(row=1, column=0, sticky=tk.W, pady=5)
        ttk.Label(file_frame, textvariable=self.template_path_3k).grid(row=1, column=1, sticky=tk.W)
        
        ttk.Button(file_frame, text="Select 5KM Template", command=lambda: self.select_template("5k")).grid(row=2, column=0, sticky=tk.W, pady=5)
        ttk.Label(file_frame, textvariable=self.template_path_5k).grid(row=2, column=1, sticky=tk.W)
        
        # Settings Frame
        settings_frame = ttk.LabelFrame(self.root, text="Certificate Settings", padding=10)
        settings_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(settings_frame, text="Font:").grid(row=0, column=0, sticky=tk.W)
        # Replace Entry with Combobox for font selection
        font_dropdown = ttk.Combobox(settings_frame, textvariable=self.font_path, 
                                    values=self.font_options, state="readonly")
        font_dropdown.grid(row=0, column=1, pady=3, sticky=tk.EW)
        
        ttk.Label(settings_frame, text="Font Size:").grid(row=1, column=0, sticky=tk.W)
        ttk.Entry(settings_frame, textvariable=self.font_size).grid(row=1, column=1, pady=3)
        
        ttk.Label(settings_frame, text="Y Position:").grid(row=2, column=0, sticky=tk.W)
        ttk.Entry(settings_frame, textvariable=self.y_position).grid(row=2, column=1, pady=3)
        
        # Generate Button
        ttk.Button(self.root, text="Generate Certificates", command=self.generate).pack(pady=15)
        
        # Progress/Status
        self.status = ttk.Label(self.root, text="Ready to generate certificates")
        self.status.pack()
    
    # [Rest of the methods remain exactly the same...]
    def select_csv(self):
        path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if path:
            self.csv_path.set(path)
            self.status.config(text=f"Loaded: {os.path.basename(path)}")
    
    def select_template(self, distance):
        path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.png")])
        if path:
            if distance == "3k":
                self.template_path_3k.set(path)
            else:
                self.template_path_5k.set(path)
            self.status.config(text=f"Set {distance.upper()} template")
    
    def generate(self):
        if not self.csv_path.get():
            messagebox.showerror("Error", "Please select a CSV file first!")
            return
        
        try:
            self.status.config(text="Generating certificates...")
            self.root.update()  # Force UI update
            
            # Process certificates
            self.process_certificates()
            
            messagebox.showinfo("Success", "Certificates generated successfully!")
            self.status.config(text="Ready to generate more certificates")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred:\n{str(e)}")
            self.status.config(text="Error - check inputs and try again")
    
    def process_certificates(self):
        # Load and filter data
        df = pd.read_csv(self.csv_path.get())
        df_3km = df[df['Registration Type'].str.contains('3KM')]
        df_5km = df[df['Registration Type'].str.contains('5KM')]
        
        # Generate certificates for each group
        self.generate_group(df_3km, "3KM", self.template_path_3k.get())
        self.generate_group(df_5km, "5KM", self.template_path_5k.get())
    
    def generate_group(self, participants_df, distance, template_path):
        # output_img_dir = f'{self.output_dir.get()}_{distance.lower()}/'
        # output_pdf_path = f'{distance.lower()}_certs.pdf'
        
        # os.makedirs(output_img_dir, exist_ok=True)

        output_folder = "output"
        os.makedirs(output_folder, exist_ok=True)
        output_img_dir = os.path.join(output_folder, f'{self.output_dir.get()}_{distance.lower()}/')
        output_pdf_path = os.path.join(output_folder, f'{distance.lower()}_certs.pdf')
        
        os.makedirs(output_img_dir, exist_ok=True)
        
        # Generate individual certificates
        for index, row in participants_df.iterrows():
            nameDefault = row['Full Name'].strip()
            name = self.format_name(nameDefault)
            
            try:
                img = Image.open(template_path)
                draw = ImageDraw.Draw(img)
                
                try:
                    font = ImageFont.truetype(self.font_path.get(), self.font_size.get(), encoding="unic")
                except:
                    # font = ImageFont.load_default()
                    ImageFont.truetype(self.font_path.get(), self.font_size.get())
                    
                    # Synthetic bold effect
                    draw.text((x_position-1, y_position-1), name, font=font, fill=self.font_color)
                    draw.text((x_position+1, y_position+1), name, font=font, fill=self.font_color)
                
                # Calculate centered position
                text_width = draw.textlength(name, font=font)
                img_width = img.size[0]
                x_position = (img_width - text_width) / 2
                
                draw.text((x_position, self.y_position.get()), name, font=font, fill=self.font_color)
                img.save(f'{output_img_dir}certificate_{name}.jpg')
            except Exception as e:
                print(f"Error generating certificate for {name}: {str(e)}")
                continue
        
        # Create PDF
        pdf = FPDF(orientation='L')
        pdf.set_auto_page_break(False)
        
        for index, row in participants_df.iterrows():
            name = row['Full Name'].strip()
            img_path = f'{output_img_dir}certificate_{name}.jpg'
            
            if os.path.exists(img_path):
                with Image.open(img_path) as img:
                    width, height = img.size
                
                pdf.add_page(orientation='P' if height > width else 'L')
                pdf.image(img_path, x=0, y=0, w=pdf.w, h=pdf.h)
        
        pdf.output(output_pdf_path)

    def format_name(self, name):
        """Convert names to proper title case (First Last)"""
        # Handle empty/whitespace names
        if not name.strip():
            return ""
        
        # Convert to title case and handle special cases
        formatted = []
        for part in name.strip().split():
            # Handle hyphenated names (e.g., Mary-Ann)
            if '-' in part:
                part = '-'.join([p.capitalize() for p in part.split('-')])
            # Handle apostrophes (e.g., O'Connor)
            elif "'" in part:
                part = "'".join([p.capitalize() for p in part.split("'")])
            else:
                part = part.capitalize()
            formatted.append(part)
        
        return ' '.join(formatted)
    
if __name__ == "__main__":
    root = tk.Tk()
    app = CertificateGeneratorApp(root)
    root.mainloop()