import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import QtWidgets
from PyQt5.QtChart import QChartView, QBarSeries, QBarSet, QLineSeries
from PyQt5.QtGui import QPen, QColor
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve

from PyQt5.QtWidgets import QMessageBox
from PyQt5 import QtCore
from PyQt5.QtChart import QChart, QScatterSeries, QValueAxis
from PyQt5.QtGui import QPainter
from PyQt5.QtCore import Qt
import random


#Sıralama algoritmaları
def bubble_sort(arr):
    n = len(arr)
    comparisons = 0

    for i in range(n):
        for j in range(0, n - i - 1):
            comparisons += 1
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]

    return arr, comparisons


def insertion_sort(arr):
    comparisons = 0

    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and key < arr[j]:
            comparisons += 1
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key

    return arr, comparisons


def selection_sort(arr):
    n = len(arr)
    comparisons = 0

    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            comparisons += 1
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]

    return arr, comparisons


def merge_sort(arr):
    if len(arr) > 1:
        mid = len(arr) // 2
        L = arr[:mid]
        R = arr[mid:]

        L, left_comparisons = merge_sort(L)
        R, right_comparisons = merge_sort(R)

        i = j = k = 0
        comparisons = left_comparisons + right_comparisons

        while i < len(L) and j < len(R):
            comparisons += 1
            if L[i] < R[j]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1

        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1

        while j < len(R):
            arr[k] = R[j]
            j += 1
            k += 1

        return arr, comparisons

    return arr, 0


def quick_sort(arr, low, high):
    if low < high:
        pi = partition(arr, low, high)

        arr, left_comparisons = quick_sort(arr, low, pi - 1)
        arr, right_comparisons = quick_sort(arr, pi + 1, high)

        return arr, left_comparisons + right_comparisons

    return arr, 0



def partition(arr, low, high):
    i = (low - 1)
    pivot = arr[high]

    for j in range(low, high):
        if arr[j] <= pivot:
            i = i + 1
            arr[i], arr[j] = arr[j], arr[i]

    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return (i + 1)

#Animasyon methodları
def draw_scatter_chart(data, chart_view):
    chart = QChart()
    chart.setTitle("Dağılım Grafiği")
    chart.legend().hide()

    series = QScatterSeries()
    for i, val in enumerate(data):
        series.append(i, val)

    chart.addSeries(series)

    axis_x = QValueAxis()
    axis_x.setLabelFormat("%d")
    axis_x.setTitleText("Index")

    axis_y = QValueAxis()
    axis_y.setLabelFormat("%d")
    axis_y.setTitleText("Value")

    chart.addAxis(axis_x, Qt.AlignBottom)
    chart.addAxis(axis_y, Qt.AlignLeft)
    series.attachAxis(axis_x)
    series.attachAxis(axis_y)

    chart_view.setChart(chart)

    # Animasyon özellikleri
    animation = QPropertyAnimation(series, b"color")
    animation.setDuration(1000000000)
    animation.setStartValue(Qt.red)
    animation.setEndValue(Qt.green)
    animation.start()


def draw_bar_chart(data, chart_view):
    series = QBarSeries()
    set0 = QBarSet("Data")

    # Verileri çubuklar halinde ekleme
    for val in data:
        set0.append(val)
    series.append(set0)

    # Chart nesnesi oluşturma
    chart = QChart()
    chart.addSeries(series)
    chart.setTitle("Bar Chart")
    chart.setAnimationOptions(QChart.SeriesAnimations)

    # Çubuklar için renk animasyonunu oluşturma
    bar_animation = QPropertyAnimation()
    bar_animation.setTargetObject(set0)
    bar_animation.setPropertyName(b"color")
    bar_animation.setDuration(100000)  # Animasyon süresi (ms)
    bar_animation.setStartValue(QColor(Qt.red))
    bar_animation.setEndValue(QColor(Qt.green))
    bar_animation.setEasingCurve(QEasingCurve.Linear)

    # X ekseninde label ayarlama
    axis_x = chart.createDefaultAxes()
    if axis_x is None:
        axis_x = QValueAxis()
    axis_x.setTitleText("Index")
    chart.addAxis(axis_x, Qt.AlignBottom)

    # Y ekseninde label ayarlama
    axis_y = chart.createDefaultAxes()
    if axis_y is None:
        axis_y = QValueAxis()
    axis_y.setTitleText("Value")
    chart.addAxis(axis_y, Qt.AlignLeft)

    # Animasyonu başlatma
    bar_animation.start()

    chart_view.setChart(chart)
    chart_view.show()
def draw_stem_chart(data, chart_view):

    # Chart nesnesi oluşturma
    chart = QChart()
    chart.setTitle("Stem Chart")

    # Seri oluşturma
    series = QLineSeries()
    series.setPen(QPen(Qt.red))

    # Verileri ekleme
    for i in range(len(data)):
        series.append(i, data[i])

    chart.addSeries(series)

    # X ekseninde label ayarlama
    axis_x = QValueAxis()
    axis_x.setLabelFormat("%d")
    axis_x.setTitleText("Index")
    chart.addAxis(axis_x, Qt.AlignBottom)
    series.attachAxis(axis_x)

    # Y ekseninde label ayarlama
    axis_y = QValueAxis()
    axis_y.setLabelFormat("%d")
    axis_y.setTitleText("Value")
    chart.addAxis(axis_y, Qt.AlignLeft)
    series.attachAxis(axis_y)

    chart_view.setChart(chart)




class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.comparisons_label = QtWidgets.QLabel('Karşılaştırmalar: 0')
        self.comparisons_label.setAlignment(QtCore.Qt.AlignCenter)
        # Animasyon kontrol butonları
        self.pause_button = QtWidgets.QPushButton('Durdur')
        self.pause_button.clicked.connect(self.pause_animation)
        self.resume_button = QtWidgets.QPushButton('Devam Et')
        self.resume_button.clicked.connect(self.resume_animation)
        self.start_button = QtWidgets.QPushButton('Başlat')
        self.start_button.clicked.connect(self.start_animation)

        # Dizi girişi için QLineEdit oluşturma
        self.array_label = QtWidgets.QLabel('Dizi:')
        self.array_line_edit = QtWidgets.QLineEdit()

        # Boyut seçimi
        self.size_label = QtWidgets.QLabel('Boyut:')
        self.size_spinbox = QtWidgets.QSpinBox()
        self.size_spinbox.setRange(1, 10000)
        self.size_spinbox.setValue(1000)

        # Hız seçimi
        self.speed_label = QtWidgets.QLabel('Hız:')
        self.speed_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.speed_slider.setRange(1, 100)
        self.speed_slider.setValue(50)

        # Sıralama algoritması seçimi
        self.sort_label = QtWidgets.QLabel('Sıralama Algoritması:')
        self.sort_combo = QtWidgets.QComboBox()
        self.sort_combo.addItems(['Selection Sort', 'Insertion Sort', 'Bubble Sort', 'Merge Sort','Quick Sort'])

        # Sıralama algoritması seçimi
        self.graphic_label = QtWidgets.QLabel('Grafik Türü:')
        self.graphic_combo = QtWidgets.QComboBox()
        self.graphic_combo.addItems(['Dağılım(Scatter) Grafiği', 'Sütun (Bar) Grafiği', 'Kök (Sten) Grafiği'])

        # Uygula butonu
        self.apply_button = QtWidgets.QPushButton('Sort')
        self.apply_button.clicked.connect(self.apply)

        # Grafik görünümünü oluşturun
        self.chart_view = QChartView(self)
        self.chart_view.setRenderHint(QPainter.Antialiasing)
        self.chart_view.setMinimumSize(640, 480)

        # Pencere düzeni
        layout = QtWidgets.QGridLayout()
        layout.addWidget(self.size_label, 0, 0)
        layout.addWidget(self.size_spinbox, 0, 1)
        layout.addWidget(self.speed_label, 1, 0)
        layout.addWidget(self.speed_slider, 1, 1)
        layout.addWidget(self.sort_label, 2, 0)
        layout.addWidget(self.sort_combo, 2, 1)
        layout.addWidget(self.graphic_label, 3, 0)
        layout.addWidget(self.graphic_combo, 3, 1)
        layout.addWidget(self.array_label, 4, 0)
        layout.addWidget(self.array_line_edit, 4, 1)
        layout.addWidget(self.apply_button, 5, 1)
        layout.addWidget(self.chart_view, 0, 2, 6, 1)
        layout.addWidget(self.chart_view, 0, 2, 7, 1)
        layout.addWidget(self.pause_button, 7, 2)
        layout.addWidget(self.resume_button, 8, 2)
        layout.addWidget(self.start_button, 9, 2)
        layout.addWidget(self.comparisons_label, 10, 0, 1, 3)

        self.setLayout(layout)

        # Pencere boyutu
        self.resize(800, 500)



    def pause_animation(self):
        self.chart_view.chart().animation().pause()

    def resume_animation(self):
        self.chart_view.chart().animation().resume()

    def start_animation(self):
        self.chart_view.chart().animation().start()

    def apply(self):
        try:
            # Seçilen değerleri alma
            size = self.size_spinbox.value()
            speed = self.speed_slider.value()
            sort_algorithm = self.sort_combo.currentText()
            graph_type = self.graphic_combo.currentText()

            # Seçilen değerleri ekrana yazdırma
            print(f"Boyut: {size}")
            print(f"Hız: {speed}")


            print(f"Sıralama Algoritması: {sort_algorithm}")
            array_input = self.array_line_edit.text()
            if array_input:
                data = list(map(int, array_input.split()))
            else:
                size = self.size_spinbox.value()
                data = [random.randint(1, 100) for _ in range(size)]
            print(data)
            if (sort_algorithm == 'Bubble Sort'):
                sorted_data, comparisons = bubble_sort(data)
                print("Buble Sort : ")
            elif (sort_algorithm == 'Quick Sort'):
                sorted_data, comparisons = quick_sort(data, 0, len(data) - 1)
                print("Quick Sort : ")
            elif (sort_algorithm == 'Selection Sort'):
                sorted_data, comparisons = selection_sort(data)
                print("Selection Sort : ")
            elif (sort_algorithm == 'Insertion Sort'):
                sorted_data, comparisons = insertion_sort(data)
                print("İnsertion Sort : ")
            elif (sort_algorithm == 'Merge Sort'):
                sorted_data, comparisons = merge_sort(data)
                print("Merge Sort : ")

            print("Sorted Data:", sorted_data)
            self.comparisons_label.setText(f'Karşılaştırmalar: {comparisons}')

            # Grafiği oluşturun
            chart_data = QBarSeries()
            set0 = QBarSet("Data")
            set0.append(data)
            chart_data.append(set0)

            chart = QChart()
            chart.addSeries(chart_data)
            chart.setTitle("Sorted Data")
            chart.setAnimationOptions(QChart.SeriesAnimations)
            #draw_scatter_chart(data, self.chart_view)

            if (graph_type == 'Dağılım(Scatter) Grafiği'):
                draw_scatter_chart(data, self.chart_view)
                print("a")
            elif (graph_type == 'Sütun (Bar) Grafiği'):
                draw_bar_chart(data, self.chart_view)
                print("b")
            elif(graph_type=='Kök (Sten) Grafiği'):
                draw_stem_chart(data,self.chart_view)
                print('c')

        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Uygulamada bir hata oluştu: {str(e)}")
            print(e)


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()












