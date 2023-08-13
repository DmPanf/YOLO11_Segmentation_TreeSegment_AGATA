#from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog, QFrame
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QFileDialog, QFrame
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QDesktopWidget, QListWidget, QListWidgetItem, QMessageBox
from PyQt5.QtWidgets import QDialog, QLineEdit, QVBoxLayout, QFormLayout, QRadioButton, QDialogButtonBox
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QByteArray, QBuffer, QIODevice
from datetime import datetime
from io import BytesIO
import requests
import json
import sys
import os
from bar import CustomPlot

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        #self.settings.clicked.connect(self.show_settings_dialog)

        # Инициализируем UI
        self.initUI()


    def initUI(self):
        self.title = 'Tree Segmentation Application ->'
        #self.setWindowTitle(self.title)
        self.setWindowTitle(self.title + f' [{self.get_current_server_url()}]')

        # Создаем виджеты для отображения изображений, Задаем форму и тень рамки
        # Установим ширину и цвет рамки (например, 2 пикселя и черный цвет)
        border_width = 8
        border_color = "#ABCDEF" # "black"
        self.image_label1 = QLabel(self)
        self.image_label1.setFixedSize(448, 448)
        self.image_label1.setFrameShape(QFrame.Box)
        self.image_label1.setFrameShadow(QFrame.Plain)
        self.image_label1.setLineWidth(border_width)
        self.image_label1.setStyleSheet(f"border: {border_width}px solid {border_color};")

        self.image_label2 = QLabel(self)
        self.image_label2.setFixedSize(448, 448)
        self.image_label2.setFrameShape(QFrame.Box)
        self.image_label2.setFrameShadow(QFrame.Plain)
        self.image_label2.setLineWidth(border_width)
        self.image_label2.setStyleSheet(f"border: {border_width}px solid {border_color};")

        # Добавим определения input_scene и output_scene
        self.input_graphics_view = QGraphicsView(self)
        self.input_scene = QGraphicsScene(self)
        self.input_graphics_view.setScene(self.input_scene)

        self.output_graphics_view = QGraphicsView(self)
        self.output_scene = QGraphicsScene(self)
        self.output_graphics_view.setScene(self.output_scene)

        # Создаем кнопки
        self.settings = QPushButton("💻 FastAPI")
        self.load_button = QPushButton("📥 Load Image")
        self.process_button = QPushButton("⚙️ AI MODEL")
        self.save_button = QPushButton("🖼 Save Result")
        self.clear_button = QPushButton("♻️  Clear Form")

        # Изменяем размеры и шрифт кнопок
        # self.save_button.setFixedSize(200, 50)
        button_font = QFont()
        button_font.setPointSize(15)
        for button in [self.settings, self.load_button, self.process_button, self.save_button, self.clear_button]:
            button.setFixedSize(button.sizeHint().width()+90, button.sizeHint().height()+20)
            button.setFont(button_font)


        # Создаем виджет CustomPlot и добавляем его в макет
        self.custom_plot = CustomPlot(self)

        # Создаем макеты для размещения виджетов
        image_layout = QHBoxLayout() # горизонтальное размещение (1 уровень)
        image_layout.addWidget(self.image_label1)
        image_layout.addWidget(self.image_label2)
        image_layout.addWidget(self.custom_plot)

        button_layout = QHBoxLayout() # горизонтальное размещение (2 уровень)
        button_layout.addWidget(self.settings)
        button_layout.addWidget(self.load_button)
        button_layout.addWidget(self.process_button)
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.clear_button)

        main_layout = QVBoxLayout() # вертикальное размещение ( 1 + 2 уровни)
        main_layout.addLayout(image_layout)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)
        self.center_on_screen()

        # Подключаем слоты (обработчики при нажатии кнопок)
        self.settings.clicked.connect(self.settings_func)
        self.load_button.clicked.connect(self.load_image)
        self.process_button.clicked.connect(self.process_image)
        self.save_button.clicked.connect(self.save_output_image)
        self.clear_button.clicked.connect(self.clear_images)

    def show_settings_dialog(self):
        self.dialog = SettingsDialog(self)
        self.dialog.show()

    def update_title(self):
        self.setWindowTitle(self.title + f' [{self.get_current_server_url()}]')


    def get_current_server_url(self):
        current_server_url = "http://api-serv.ru:8001"
        # Путь к файлу с данными сервера
        servers_file_path = 'servers.json'
        
        if os.path.exists(servers_file_path):
            # Если файл существует, загружаем данные из него
            with open(servers_file_path, 'r') as f:
                servers = json.load(f)
            
            # Находим сервер с True в поле 'active' и возвращаем его URL.
            # Если такого сервера нет, возвращаем значение по умолчанию.
            for server in servers:
                if server.get('active'):
                    current_server_url = f"http://{server.get('server')}:{server.get('port')}"
                    return current_server_url
        
        # Если файл не существует или активный сервер не найден, возвращаем значение по умолчанию     
        return current_server_url

    # Здесь вызываем функцию, которая обновляет график в CustomPlot
    def update_plot(self):
        self.custom_plot.plot()  # Вызываем функцию plot из CustomPlot

    def settings_func(self):
        self.settings_dialog = SettingsDialog(self)
        self.settings_dialog.exec_()

    def load_image(self):
        # Загрузка изображения
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_name, _ = QFileDialog.getOpenFileName(self, "Выберите изображение", "", "Images (*.png *.xpm *.jpg *.bmp);;All Files (*)", options=options)
        if file_name:
            pixmap = QPixmap(file_name)
            self.image_label1.setPixmap(pixmap.scaled(self.image_label1.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
            self.input_scene.clear()
            pixmap_item = self.input_scene.addPixmap(self.image_label1.pixmap())


    def process_image(self):
        if not self.input_scene.items():
            return

        try:
            with open("servers.json", "r") as f:
                servers = json.load(f)
        except FileNotFoundError:
            print("servers.json not found!")
            return

        active_server = next((server for server in servers if server["active"]), None)
        if active_server is None:
            print("No active server found!")
            return

        url = f"http://{active_server['server']}:{active_server['port']}/process_image"

        item = self.input_scene.items()[0]
        input_image = item.pixmap().toImage()

        byte_array = QByteArray()
        buffer = QBuffer(byte_array)
        buffer.open(QIODevice.WriteOnly)
        input_image.save(buffer, "PNG")
        image_data = bytes(byte_array)

        try:
            response = requests.post(url, files={"image": ("input_image.png", image_data, "image/png")})
            response.raise_for_status()  # This will raise an exception if the status code is not 200
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")

            error_message = QMessageBox(self)
            error_message.setWindowTitle("Error")
            error_message.setIcon(QMessageBox.Critical)
            error_message.setText(f"Не удалось выполнить запрос:\n{url}\n\nОшибка: {e}")
            error_message.exec_()

            return

        output_image_data = BytesIO(response.content)
        pixmap = QPixmap()
        pixmap.loadFromData(output_image_data.getvalue())
        self.image_label2.setPixmap(pixmap.scaled(self.image_label2.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.output_scene.clear()
        pixmap_item = self.output_scene.addPixmap(self.image_label2.pixmap())
        # pixmap_item = self.output_scene.addPixmap(pixmap.scaled(self.output_graphics_view.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
        #self.image_label2.setPixmap(pixmap.scaled(self.image_label2.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))


    def save_output_image(self):
        if not self.output_scene.items():
            return

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        default_filename = f"tree_segmentation_{timestamp}.png"
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Сохраняем обработанное изображение",
            default_filename,
            "Images (*.png *.jpg *.bmp);;All Files (*)",
            options=options,
        )

        if filename:
            output_image = self.output_scene.items()[0].pixmap().toImage()
            output_image.save(filename)


    def clear_images(self):
        # Очистка виджетов с изображениями
        self.image_label1.clear()
        self.image_label2.clear()


    def center_on_screen(self):
        # Получаем геометрию экрана
        screen_geometry = QApplication.desktop().availableGeometry()
        # Получаем геометрию окна
        window_geometry = self.frameGeometry()
        # Устанавливаем центр окна в центр экрана
        window_geometry.moveCenter(screen_geometry.center())
        # Добавляем смещение: отодвигаем окно вверх на 50 пикселей
        window_geometry.moveTop(window_geometry.top() - 50)
        # Перемещаем главное окно по этим координатам
        self.move(window_geometry.topLeft())


class ServerForm(QFormLayout):
    def __init__(self, server=None):
        super().__init__()
        self.server_edit = QLineEdit()
        self.port_edit = QLineEdit()
        self.active_button = QRadioButton()

        self.addRow("Server:", self.server_edit)
        self.addRow("Port:", self.port_edit)
        self.addRow("Active:", self.active_button)

        if server:
            self.server_edit.setText(server["server"])
            self.port_edit.setText(str(server["port"]))
            self.active_button.setChecked(server["active"])

    def get_server(self):
        return {
            "server": self.server_edit.text(),
            "port": self.port_edit.text(),
            "active": self.active_button.isChecked()
        }


class SettingsDialog(QDialog):
    def __init__(self, main_window, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Server FastAPI")
        self.main_window = main_window

        self.layout = QVBoxLayout(self)
        self.forms = []

        self.load_servers()

        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok, self)
        self.layout.addWidget(self.button_box)
        self.setLayout(self.layout)

        self.button_box.accepted.connect(self.accept)

    def load_servers(self):
        try:
            with open("servers.json", "r") as f:
                servers = json.load(f)
                for server in servers:
                    form = ServerForm(server)
                    self.forms.append(form)
                    self.layout.insertLayout(self.layout.count() - 1, form)
        except FileNotFoundError:
            form = ServerForm({"server": "api-serv.ru", "port": "8001", "active": False})
            self.forms.append(form)
            self.layout.insertLayout(self.layout.count() - 1, form)

    def accept(self):
        servers = [form.get_server() for form in self.forms]
        with open("servers.json", "w") as f:
            json.dump(servers, f)
        super().accept()
        # Обновляем заголовок главного окна
        self.main_window.update_title()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
