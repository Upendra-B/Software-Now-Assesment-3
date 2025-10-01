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

    # ---------------------- Menu ----------------------
    def create_menu(self):
        menubar = tk.Menu(self)
        self.config(menu=menubar)

        # File
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Exit", command=self.quit)

        # Models
        models_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Models", menu=models_menu)
        models_menu.add_command(label="Reload Models", command=self.reload_models)

        # Help
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=lambda: messagebox.showinfo("About", "AI Image Generator GUI"))

    # ---------------------- Top Section ----------------------
    def create_model_selection_and_output_section(self):
        top_frame = ttk.Frame(self.main_frame, relief="ridge", borderwidth=2, padding="10")
        top_frame.grid(row=0, column=0, columnspan=2, sticky="nsew", pady=(0, 10))
        top_frame.columnconfigure(1, weight=1)

        ttk.Label(top_frame, text="Model Selection:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.model_combo = ttk.Combobox(top_frame, values=["Text-to-Image", "Image-to-Image"])
        self.model_combo.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.model_combo.set("Text-to-Image")

        load_model_button = ttk.Button(top_frame, text="Load Model", command=self.load_model)
        load_model_button.grid(row=0, column=2, padx=5, pady=5, sticky="e")

    
    # ---------------------- Middle Section ----------------------
    def create_input_and_output_section(self):
        # Input frame
        input_frame = ttk.Frame(self.main_frame, relief="ridge", borderwidth=2, padding="10")
        input_frame.grid(row=1, column=0, sticky="nsew", padx=(0, 5))
        input_frame.columnconfigure(0, weight=1)
        input_frame.rowconfigure(2, weight=1)

        ttk.Label(input_frame, text="User Input Section", font=('Helvetica', 12, 'bold')).grid(
            row=0, column=0, columnspan=3, sticky="w", pady=(0, 5)
        )

        # Input type radio
        self.input_var = tk.StringVar(value="Text")
        ttk.Radiobutton(input_frame, text="Text", variable=self.input_var, value="Text").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        ttk.Radiobutton(input_frame, text="Image", variable=self.input_var, value="Image").grid(row=1, column=1, padx=5, pady=5, sticky="w")

        browse_button = ttk.Button(input_frame, text="Browse", command=self.browse_file)
        browse_button.grid(row=1, column=2, padx=5, pady=5, sticky="e")

        # Input area
        self.input_text = scrolledtext.ScrolledText(input_frame, wrap=tk.WORD, width=40, height=10)
        self.input_text.grid(row=2, column=0, columnspan=3, padx=5, pady=5, sticky="nsew")

        # Buttons
        ttk.Button(input_frame, text="Generate", command=self.generate_image).grid(row=3, column=0, padx=5, pady=5, sticky="w")
        ttk.Button(input_frame, text="Clear", command=self.clear_fields).grid(row=3, column=2, padx=5, pady=5, sticky="e")

        # Output frame
        output_frame = ttk.Frame(self.main_frame, relief="ridge", borderwidth=2, padding="10")
        output_frame.grid(row=1, column=1, sticky="nsew", padx=(5, 0))
        output_frame.columnconfigure(0, weight=1)
        output_frame.rowconfigure(1, weight=1)

        ttk.Label(output_frame, text="Model Output Section", font=('Helvetica', 12, 'bold')).grid(
            row=0, column=0, sticky="w", pady=(0, 5)
        )

        # Read-only output
        self.output_display = scrolledtext.ScrolledText(output_frame, wrap=tk.WORD, width=40, height=10)
        self.output_display.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        self.output_display.config(state="disabled")  # make read-only

        # Image preview
        self.img_label = ttk.Label(output_frame)
        self.img_label.grid(row=2, column=0, pady=10)

    # ---------------------- Bottom Section ----------------------
    def create_info_and_notes_section(self):
        bottom_frame = ttk.Frame(self.main_frame, relief="ridge", borderwidth=2, padding="10")
        bottom_frame.grid(row=2, column=0, columnspan=2, sticky="nsew", pady=(10, 0))
        bottom_frame.columnconfigure(0, weight=1)
        bottom_frame.columnconfigure(1, weight=1)

        # Model Info
        ttk.Label(bottom_frame, text="Model Information", font=('Helvetica', 10, 'bold')).grid(row=0, column=0, sticky="w")
        self.model_info = scrolledtext.ScrolledText(bottom_frame, wrap=tk.WORD, height=8)
        self.model_info.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        self.model_info.config(state="disabled")

        # OOP Info
        ttk.Label(bottom_frame, text="OOP Explanation", font=('Helvetica', 10, 'bold')).grid(row=0, column=1, sticky="w")
        self.oop_info = scrolledtext.ScrolledText(bottom_frame, wrap=tk.WORD, height=8)
        self.oop_info.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)

        # Fill OOP info text (read-only)
        oop_text = (
            "OOP Concepts Explanation:\n"
            "- Multiple Inheritance (Logger + BaseHandler)\n"
            "- Encapsulation (_model is private)\n"
            "- Method Overriding (custom log)\n"
            "- Decorators (@log_time applied)\n"
        )
        self.oop_info.insert(tk.END, oop_text)
        self.oop_info.config(state="disabled")
