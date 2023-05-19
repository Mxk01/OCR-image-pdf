import cv2
import pytesseract
import tkinter as tk
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
from PIL import ImageTk, Image
from fpdf import FPDF

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

class ImagePreviewDialog(tk.Toplevel):
    def __init__(self, image_path):
        super().__init__()
        self.image_path = image_path
        self.title("Image Preview")

        self.image = Image.open(self.image_path)
        self.image.thumbnail((400, 400))  # Resize the image to fit within the dialog

        self.photo = ImageTk.PhotoImage(self.image)  # Convert the PIL Image to PhotoImage

        self.image_label = tk.Label(self, image=self.photo)
        self.image_label.pack(padx=10, pady=10)

def create_pdf(text, input):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, text.encode('latin-1', 'replace').decode('latin-1'))  # Handle encoding issues
    pdf.output(f"pdfs/${input}.pdf")

def convert_to_text():
    image_path = askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.bmp")])
    image_preview_dialog = ImagePreviewDialog(image_path)
    image_preview_dialog.transient(app)  # Set the main window as the parent of the dialog
    app.wait_window(image_preview_dialog)  # Wait until the dialog is closed

    image = cv2.imread(image_path)
    ConvertImage = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    text_result = pytesseract.image_to_string(ConvertImage)
    return text_result

def show_text():
    text = convert_to_text()
    input_text = input_field.get()  # Get the user's input from the entry field
    print("Text result:")
    print(text)

    if text.strip() == "":
        # Show the messagebox
        messagebox.showinfo("Alert", "Aceasta imagine nu poate fi convertita intr-un PDF deoarece nu are text!")
    else:
        print("User's input:")
        print(input_text)
        create_pdf(text, input_text)

# Create the main application window
app = tk.Tk()
app.geometry("500x300")
app.title("Image to PDF Converter")

# Configure grid layout
app.grid_columnconfigure(0, weight=1)
app.grid_rowconfigure(1, weight=1)

# Create a frame for the content
content_frame = tk.Frame(app)
content_frame.grid(row=1, column=0, padx=20, pady=20)

# Create an entry field for user input
input_field = tk.Entry(content_frame, width=40)
input_field.grid(row=0, column=0, columnspan=2, padx=5, pady=10)

# Create a label for the entry field
label = tk.Label(content_frame, text="Enter File Name:")
label.grid(row=1, column=0, sticky="W", padx=5)

# Create a button to search for the file
button = tk.Button(content_frame, text="Search File", command=show_text, fg="white", bg="#6c5ce7")
button.grid(row=1, column=1, padx=5)

# Run the main application loop
app.mainloop()
