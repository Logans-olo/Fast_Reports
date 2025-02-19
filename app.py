import sys
from PySide6.QtCore import QUrl
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtPdf import QPdfDocument, QPdfPageRenderer
from db import *
students = []
tables =[]
csvs=[]
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        width = 400
        height = 500
        self.setWindowTitle("My App")
        self.window1 = AnotherWindow(" ")
        self.label = QLabel("Select The student from the Database")
        self.stInput = QComboBox()
        self.stInput.addItems(students)
        self.tbInput = QComboBox()
        self.numColumn = QSpinBox()
        self.label2 = QLabel("Select the table you would like to query from/ Number of columns")
        toolbar = QToolBar("Main toolbar")
        # self.addToolBar(toolbar)
        tool_action = QAction("Add student", self)
        tool_action.triggered.connect(self.toggle_window1)
        tool_action.setToolTip("This button does stuff")
        
        
        add_action = QAction("Add table", self)
        add_action.triggered.connect(self.toggle_window2)
        add_action.setToolTip("This button also does stuff")
        
        export_action = QAction("Export tables", self)
        import_action = QAction("Import tables", self)
        
        self.button = QPushButton("Generate New Window!")
        self.button.clicked.connect(lambda: self.toggle_result())
        
        #Start of the menu layout, which will be where all of the additional functionality will
        #come from, such as adding students via a new window
        #Or adding a new CSV to the database 
        self.setStatusBar(QStatusBar(self))
        menu = self.menuBar()
        registry_menu = menu.addMenu("students")
        database_menu = menu.addMenu("Databases")
        file_menu = menu.addMenu("File")
        database_menu.addAction(add_action)
        registry_menu.addAction(tool_action)
        file_menu.addAction(export_action)
        file_menu.addAction(import_action)
        
        
        
        layout = QVBoxLayout()
        layout2 = QHBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.stInput)
        layout.addWidget(self.label2)
        layout2.addWidget(self.tbInput)
        layout2.addWidget(self.numColumn)
        layout.addLayout(layout2)
        layout.addWidget(self.button)

        container = QWidget()
        container.setLayout(layout)
        self.setMinimumSize(width, height)
        self.setCentralWidget(container)

    def contextMenuEvent(self, e):
        context = QMenu(self)
        close_action = QAction("Exit", self)
        close_action.triggered.connect(self.close)
        context.addAction(close_action)
        context.addAction(QAction("test 2", self))
        context.addAction(QAction("test 3", self))
        context.exec(e.globalPos())
        
    def onMyToolBarButtonClick(self, s): 
        print(s)
        dlg = QDialog(self)
        dlg.setMinimumSize(250,250)
        dlg.setWindowTitle("Add Table")
        dlg.exec()
    def toggle_window1(self):
        # if self.window1.isVisible():
        #     self.window1.hide()
        # else:
        #     self.window1.show()
        dlg = AnotherWindow("")
        dlg.setMinimumSize(250, 250)
        dlg.setWindowTitle("Add student to database")
        dlg.exec()
        self.stInput.addItem(students[len(students) -1 ])
    def toggle_window2(self):
        
        dlg = tableAdd()
        dlg.setMinimumSize(250, 250)
        dlg.setWindowTitle("Add student to database")
        dlg.exec()
        self.tbInput.addItem(tables[len(tables) -1 ])
    def toggle_result(self): 
        self.w = QueryResult(self.tbInput.currentText())
        if self.w.isVisible():
            self.w.hide()
        else: 
            self.w.show()

class AnotherWindow(QDialog):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """

    def __init__(self, text):
        super().__init__()

        # Set up layout and label
        layout1 = QVBoxLayout()
        layout2 = QHBoxLayout()
        self.label = QLabel("Another Window")
        self.combobox = QComboBox()
        self.input = QLineEdit()
        self.combobox.addItems(students)
        self.button = QPushButton("Add student to registry")
        self.button.clicked.connect(lambda: self.add_item_from_text(self.input.text()))
        self.combobox.currentTextChanged.connect(self.text_changed)
        layout1.addWidget(self.label)
        layout1.addWidget(self.input)
        layout2.addWidget(self.combobox)
        layout2.addWidget(self.button)
        layout1.addLayout(layout2)

        # self.graphics_view = QGraphicsView()
        # self.graphics_scene = QGraphicsScene(self)
        # self.graphics_view.setScene(self.graphics_scene)
        # layout.addWidget(self.graphics_view)

        self.setLayout(layout1)

        # Update label text with the passed value from MainWindow
        # self.label.setText(text)

        # Load and render the PDF
        #self.load_pdf('Logan.pdf')  # Replace with the correct PDF path
    def text_changed(self,text): 
        print(text)
        
    def add_item_from_text(self, text):
        self.combobox.addItem(text)
        students.append(text)
    def load_pdf(self, pdf_path):
        # Load the PDF document
        self.pdf_document = QPdfDocument()
        self.pdf_document.load(pdf_path)

        # Render the first page of the PDF
        self.render_page(0)

    def render_page(self, page_number):
        # Create a renderer for the page
        pdf_renderer = QPdfPageRenderer(self.pdf_document)

        # Create a pixmap to render the page to
        page_pixmap = pdf_renderer.render(page_number)

        # Display the rendered page in the graphics scene
        pixmap_item = QGraphicsPixmapItem(page_pixmap)
        self.graphics_scene.addItem(pixmap_item)
        self.graphics_view.setRenderHint(QGraphicsView.Antialiasing)

        # Optionally, adjust the view to fit the content
        self.graphics_view.setSceneRect(pixmap_item.boundingRect())
        self.graphics_view.fitInView(pixmap_item, 1)
class QueryResult(QMainWindow): 
    """
    This "window" is a QDialog. It must be removed before the program is allowed to continue
    """
    
    def __init__(self, table_name):
        constraint = QWidget()
        super().__init__()
        self.setMinimumSize(400,400)
        # Set up layout and label
        layout1 = QVBoxLayout()
        headers = []
        layout2 = QHBoxLayout()
        self.label = QLabel()
        self.combo = QComboBox()
        self.label.setText(table_name)
        layout1.addWidget(self.label)
        
        data = db_column(table_name)
        for row in data:
            headers.append(row[1])
        self.combo.addItems(headers)
        layout1.addWidget(self.combo)
        self.setLayout(layout1)
        constraint.setLayout(layout1)
        self.setCentralWidget(constraint)
class tableAdd(QDialog): 
    def __init__(self):
        
        super().__init__()
        layout1 = QVBoxLayout()
        layout2 = QHBoxLayout()
        self.label = QLabel("What is the name of the CSV to read from")
        self.input = QLineEdit()
        self.label2 = QLabel("What would you like to name this table")
        self.input2 = QLineEdit()
        self.button = QPushButton("Add to Database")
        self.button.clicked.connect(lambda: self.add_item_from_text(self.input2.text(), self.input.text()))
        self.combobox = QComboBox()
        self.combobox.addItems(tables)
        layout1.addWidget(self.label)
        layout1.addWidget(self.input)
        layout1.addWidget(self.label2)
        layout1.addWidget(self.input2)
        layout2.addWidget(self.combobox)
        layout2.addWidget(self.button)
        
        layout1.addLayout(layout2)
        self.setLayout(layout1)
        
    def add_item_from_text(self, table_name, pathname):
        self.combobox.addItem(table_name)
        tables.append(table_name)
        csvs.append(pathname)
        db_init(table_name, pathname)
        