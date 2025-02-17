import sys
from PySide6.QtCore import QUrl
from PySide6.QtGui import QPixmap, QAction
from PySide6.QtWidgets import *
from PySide6.QtPdf import QPdfDocument, QPdfPageRenderer


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        width = 200
        height = 200
        self.setWindowTitle("My App")
        self.window1 = AnotherWindow(" ")
        self.label = QLabel()

        self.input = QLineEdit()
        
        self.button = QPushButton("Generate New Window!")
        self.button.clicked.connect(lambda: self.label.setText(self.input.text()))
        self.button.clicked.connect(lambda: self.toggle_window1())
        
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
        layout = QVBoxLayout()
        self.label = QLabel("Another Window")
        combobox = QComboBox()
        combobox.addItems(["one", "two", "three"])
        combobox.currentTextChanged.connect(self.text_changed)
        layout.addWidget(self.label)
        layout.addWidget(combobox)

        # self.graphics_view = QGraphicsView()
        # self.graphics_scene = QGraphicsScene(self)
        # self.graphics_view.setScene(self.graphics_scene)
        # layout.addWidget(self.graphics_view)

        self.setLayout(layout)

        # Update label text with the passed value from MainWindow
        self.label.setText(text)

        # Load and render the PDF
        #self.load_pdf('Logan.pdf')  # Replace with the correct PDF path
    def text_changed(self,text): 
        print(text)
        
        
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