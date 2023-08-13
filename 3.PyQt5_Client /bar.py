import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QHBoxLayout

class CustomPlot(QWidget):
    def __init__(self, parent=None):
        super(CustomPlot, self).__init__(parent)

        self.layout = QVBoxLayout(self)
        self.figure, self.ax = plt.subplots(figsize=(7, 6))
        # self.figure.patch.set_facecolor("darkgreen")
        self.figure.patch.set_facecolor("#ABCDEF")
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setFixedSize(336, 448)
        self.layout.addWidget(self.canvas)

        colors = [
            (255, 255, 255), (0, 0, 0), (0, 0, 255), (255, 0, 255),
            (255, 255, 0), (0, 255, 255), (255, 0, 0), (127, 127, 127), (0, 255, 0)
        ]
        labels = [
            "нет данных", "дорога", "неясная площадь", "поляна/луг", "молодой лес",
            "жердняк\n(жердняковый лес)", "среднезрелый лес", "созревающий лес", "зрелый лес"
        ]

        bar_width = 1

        hbox = QHBoxLayout()

        for i in range(len(colors)):
            self.ax.barh(i, 5, color=np.array(colors[i]) / 255., height=bar_width)
            self.my_label = f'{i} {labels[i]}'
            self.ax.text(1., i, self.my_label, va='center', fontsize=14, color='darkgreen')

            #label = QLabel(labels[i])
            #label.setStyleSheet("font-size: 14px; color: darkblue;")
            #hbox.addWidget(label)

        self.layout.addLayout(hbox)

        self.ax.set_yticks(range(len(colors)))
        self.ax.set_yticklabels([""] * len(colors))
        self.ax.xaxis.set_visible(False)
        plt.tight_layout()


def main():
    app = QApplication(sys.argv)

    plot_widget = CustomPlot()
    plot_widget.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
