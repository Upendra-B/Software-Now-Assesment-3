# Import the main GUI class from gui.py
from gui import AIGUI  

# Run this block only if this file is executed directly (not imported)
if __name__ == "__main__":
    # Create an instance of the AIGUI application
    app = AIGUI()
    
    # Start the Tkinter event loop to display the GUI window
    app.mainloop()
