
from app import *
from db import *





#Spring 2025 OBHR 33000-008 LEC
def main(): 
    
    app = QApplication()
# Create a Qt widget, which will be our window.
    window = MainWindow()
    window.show()  # IMPORTANT!!!!! Windows are hidden by default.
    
    # Start the event loop.
    app.exec()
    
    # document.save(name + ".docx")




if __name__ == "__main__":
    main()