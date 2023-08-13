import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QGraphicsView, QGraphicsScene
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QByteArray, QBuffer, QIODevice
import requests
from io import BytesIO

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'Image Processing App'
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)

        layout = QVBoxLayout()

        self.input_image_label = QLabel("Input image")
        self.output_image_label = QLabel("Output image")

        self.input_graphics_view = QGraphicsView()
        self.output_graphics_view = QGraphicsView()

        self.input_scene = QGraphicsScene()
        self.output_scene = QGraphicsScene()

        self.input_graphics_view.setScene(self.input_scene)
        self.output_graphics_view.setScene(self.output_scene)

        load_button = QPushButton('Load Image', self)
        load_button.clicked.connect(self.load_image)

        process_button = QPushButton('Process Image', self)
        process_button.clicked.connect(self.process_image)

        clear_button = QPushButton('Clear Images', self)
        clear_button.clicked.connect(self.clear_images)

        layout.addWidget(self.input_image_label)
        layout.addWidget(self.input_graphics_view)
        layout.addWidget(self.output_image_label)
        layout.addWidget(self.output_graphics_view)
        layout.addWidget(load_button)
        layout.addWidget(process_button)
        layout.addWidget(clear_button)

        self.setLayout(layout)

    def load_image(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_name, _ = QFileDialog.getOpenFileName(self, "Load Image", "", "Images (*.png *.xpm *.jpg *.bmp);;All Files (*)", options=options)
        if file_name:
            pixmap = QPixmap(file_name)
            self.input_scene.clear()
            self.input_scene.addPixmap(pixmap)
            self.input_graphics_view.setScene(self.input_scene)

    def process_image(self):
        if not self.input_scene.items():
            return

        url = "http://apiserv.ru:8001/process_image"  # адрес сервера FastAPI
        input_image = self.input_scene.items()[0].pixmap().toImage()
        byte_array = QByteArray()
        buffer = QBuffer(byte_array)
        buffer.open(QIODevice.WriteOnly)
        input_image.save(buffer, "PNG")
        image_data = bytes(byte_array)

        response = requests.post(url, files={"image": ("input_image.png", image_data, "image/png")})

        if response.status_code == 200:
            output_image_data = BytesIO(response.content)
            pixmap = QPixmap()
            pixmap.loadFromData(output_image_data.getvalue())
            self.output_scene.clear()
            self.output_scene.addPixmap(pixmap)
            self.output_graphics_view.setScene(self.output_scene)

    def clear_images(self):
        self.input_scene.clear()
        self.output_scene.clear()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())
