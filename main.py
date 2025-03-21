
from app import *
from db import *
import pandas as pd




#Spring 2025 OBHR 33000-008 LEC
def main(): 
    mode = 0
    if(mode):
        try:
            app = QApplication()
        # Create a Qt widget, which will be our window.
            window = MainWindow()
            window.show()  # IMPORTANT!!!!! Windows are hidden by default.
            
            # Start the event loop.
            app.exec()
        except Exception as e:
            QMessageBox.critical(app, "General Error with Window", str(e))
    # document.save(name + ".docx")
    else: 
        df = pd.DataFrame(pd.read_excel(input("Please enter the name of the excel file")))
        for i in range(0,4): 
            print(df.loc[i])




if __name__ == "__main__":
    main()