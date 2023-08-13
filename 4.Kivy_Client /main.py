from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.lang import Builder
import os
import requests


Builder.load_string('''
<CustomFileChooser>:
    orientation: 'vertical'
    FileChooserListView:
        id: filechooser
        filters: ['*.png', '*.jpg', '*.jpeg', '*.bmp']
        show_hidden: False
    Button:
        text: "Select"
        on_release:
            root.select_image(filechooser.selection)
            root.owner.dismiss_popup()
''')


class CustomFileChooser(BoxLayout):
    def __init__(self, owner, **kwargs):
        super().__init__(**kwargs)
        self.owner = owner

    def select_image(self, selection):
        if selection:
            self.owner.input_image.source = selection[0]

class ImageProcessingApp(App):
    def build(self):
        self.input_image = Image(source='placeholder.png', allow_stretch=True, keep_ratio=True)
        self.output_image = Image(source='placeholder.png', allow_stretch=True, keep_ratio=True)

        layout = BoxLayout(orientation='vertical')

        input_image_container = BoxLayout(orientation='vertical', size_hint_y=0.45)
        input_image_container.add_widget(Label(text='Input Image', size_hint_y=None, height=30))
        input_image_container.add_widget(self.input_image)
        layout.add_widget(input_image_container)

        output_image_container = BoxLayout(orientation='vertical', size_hint_y=0.45)
        output_image_container.add_widget(Label(text='Output Image', size_hint_y=None, height=30))
        output_image_container.add_widget(self.output_image)
        layout.add_widget(output_image_container)

        layout.add_widget(Button(text='Load Image', on_release=self.load_image, size_hint_y=None, height=40))
        layout.add_widget(Button(text='Process Image', on_release=self.process_image, size_hint_y=None, height=40))
        layout.add_widget(Button(text='Clear Widgets', on_release=self.clear_images, size_hint_y=None, height=40))

        return layout


    def load_image(self, _):
        content = CustomFileChooser(owner=self)
        self.popup = Popup(title='Select an image', content=content, size_hint=(0.9, 0.9))
        self.popup.open()

    def dismiss_popup(self):
        self.popup.dismiss()

    def process_image(self, _):
        if not self.input_image.source or self.input_image.source == 'placeholder.png':
            return

        url = "http://api-serv.ru:8001/process_image"  # адрес сервера FastAPI
        with open(self.input_image.source, 'rb') as f:
            image_data = f.read()

        response = requests.post(url, files={"image": ("input_image.png", image_data, "image/png")})

        if response.status_code == 200:
            with open('output_image.png', 'wb') as f:
                f.write(response.content)
            self.output_image.source = 'output_image.png'
            self.output_image.reload()

    def clear_images(self, _):
        self.input_image.source = 'placeholder.png'
        self.output_image.source = 'placeholder.png'


if __name__ == '__main__':
    ImageProcessingApp().run()
