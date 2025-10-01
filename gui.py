import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext, messagebox
from PIL import Image, ImageTk
from models import ModelHandler

class AIGUI(tk.Tk):
    """
    AI GUI with modular Tkinter design + integrated ModelHandler.
    """
    def _init_(self):
        super()._init_()
        self.title("AI Image Generator")
        self.geometry("900x700")

        # Model handler
        self.model_handler = ModelHandler()

        # Store input/output
        self.input_image_path = None
        self.input_image_for_model = None
        self.output_image = None

        # Keep reference to PhotoImage
        self.displayed_image = None

        # Create UI
        self.create_widgets()

    def create_widgets(self):
        self.create_menu()

        self.main_frame = ttk.Frame(self, padding="10")
        self.main_frame.pack(fill="both", expand=True)
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=1)

        self.create_model_selection_and_output_section()
        self.create_input_and_output_section()
        self.create_info_and_notes_section()
