import sys
from PySide6.QtCore import QUrl
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtPdf import QPdfDocument, QPdfPageRenderer
from db import *
students = ["Logan", "Jacob", "Nathan"]
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        width = 400
        height = 500
        self.setWindowTitle("My App")
        self.window1 = AnotherWindow(" ")
        self.label = QLabel()

        self.input = QLineEdit()
        toolbar = QToolBar("Main toolbar")
        self.addToolBar(toolbar)
        tool_action = QAction("Add student", self)
        tool_action.triggered.connect(self.onMyToolBarButtonClick)
        tool_action.setToolTip("This button does stuff")
        
        
        add_action = QAction("Add table", self)
        add_action.triggered.connect(lambda: db_init(""))
        add_action.setToolTip("This button also does stuff")
        
        self.button = QPushButton("Generate New Window!")
        self.button.clicked.connect(lambda: self.label.setText(self.input.text()))
        self.button.clicked.connect(lambda: self.toggle_window1())
        
        #Start of the menu layout, which will be where all of the additional functionality will
        #come from, such as adding students via a new window
        #Or adding a new CSV to the database 
        self.setStatusBar(QStatusBar(self))
        menu = self.menuBar()
        registry_menu = menu.addMenu("students")
        database_menu = menu.addMenu("Databases")
        database_menu.addAction(add_action)
        registry_menu.addAction(tool_action)
        
        
        
        layout = QVBoxLayout()
        layout.addWidget(self.input)
        layout.addWidget(self.label)
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
        dlg.setWindowTitle("Add student")
        dlg.exec()
    def toggle_window1(self):
        if self.window1.isVisible():
            self.window1.hide()
        else:
            self.window1.show()


class AnotherWindow(QWidget):
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
        self.label.setText(text)

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