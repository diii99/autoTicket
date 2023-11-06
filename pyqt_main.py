import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QComboBox, QPushButton, QLabel, QMessageBox
from PyQt5.QtCore import QThread, pyqtSignal
import select_info_demo

# Global variable to hold all information
ALL_INFO = None


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.all_info = None
        # Set the window title
        self.setWindowTitle('Title')
        # Set the initial size of the window
        self.resize(400, 130)
        # Initialize the flag
        self.tag = 0
        # Create layout
        layout = QVBoxLayout()

        # First row: Type selection
        first_row_layout = QHBoxLayout()
        type_label = QLabel('Select Type')
        self.type_combobox = QComboBox(self)
        first_row_layout.addWidget(type_label)
        first_row_layout.addWidget(self.type_combobox)

        # Second row: Date selection
        second_row_layout = QHBoxLayout()
        date_label = QLabel('Select Date')
        self.date_combobox = QComboBox(self)
        second_row_layout.addWidget(date_label)
        second_row_layout.addWidget(self.date_combobox)

        # Third row: Time selection
        third_row_layout = QHBoxLayout()
        time_label = QLabel('Select Time')
        self.time_combobox = QComboBox(self)
        third_row_layout.addWidget(time_label)
        third_row_layout.addWidget(self.time_combobox)

        # Fourth row: Information and buttons
        fourth_row_layout = QHBoxLayout()
        self.info_label = QLabel('Information Message')
        self.initialize_button = QPushButton('Initialize')
        self.initialize_button.clicked.connect(self.initialize)
        self.book_button = QPushButton('Book')
        self.book_button.clicked.connect(self.book)
        self.book_button.setEnabled(False)
        fourth_row_layout.addWidget(self.initialize_button)
        fourth_row_layout.addWidget(self.book_button)
        fourth_row_layout.addStretch(1)
        fourth_row_layout.addWidget(self.info_label)

        # Add rows to main layout
        layout.addLayout(first_row_layout)
        layout.addLayout(second_row_layout)
        layout.addLayout(third_row_layout)
        layout.addLayout(fourth_row_layout)
        layout.addStretch(1)

        # Set layout for the window
        self.setLayout(layout)

        # Connect signals and slots
        self.type_combobox.highlighted[int].connect(self.populate_dates)
        self.date_combobox.highlighted[str].connect(self.populate_times)

    def populate_dates(self, index):
        date_list = []
        if self.all_info is not None:
            self.info_by_type = select_info_demo.get_info_by_type(self.all_info, index)
            for info in self.info_by_type:
                date = f'{info["time"][0]},{info["time"][1]} {info["time"][2]} {info["time"][3]}'
                if date not in date_list:
                    date_list.append(date)
            self.date_combobox.clear()
            self.date_combobox.addItems(date_list)

    def populate_times(self, date_string):
        time_list = []
        type_selected = self.type_combobox.currentText()
        for info in self.all_info:
            date = f'{info["time"][0]},{info["time"][1]} {info["time"][2]} {info["time"][3]}'
            if date == date_string and type_selected in info['title']:
                time_str = f'{info["time"][4]}-{info["time"][5]}'
                if time_str not in time_list:
                    time_list.append(time_str)
        self.time_combobox.clear()
        self.time_combobox.addItems(time_list)

    def initialize(self):
        self.info_label.setText('Initializing...')
        self.initialize_button.setText('Initializing...')
        self.initialize_button.setEnabled(False)
        self.initialize_thread = InitializationThread()
        self.initialize_thread.finished_signal.connect(self.finish_initialization)
        self.initialize_thread.start()

    def book(self):
        type_selected = self.type_combobox.currentText()
        date_selected = self.date_combobox.currentText()
        time_selected = self.time_combobox.currentText()
        for info in self.all_info:
            date_str = f'{info["time"][0]},{info["time"][1]} {info["time"][2]} {info["time"][3]}'
            time_str = f'{info["time"][4]}-{info["time"][5]}'
            if date_selected == date_str and type_selected in info['title'] and time_selected == time_str:
                self.info_label.setText('Automating...')
                self.book_button.setText('Booking...')
                self.book_button.setEnabled(False)
                self.booking_thread = BookingThread(info['id'])
                self.booking_thread.finished_signal.connect(self.finish_booking)
                self.booking_thread.start()

    def finish_booking(self, result):
        self.book_button.setText('Book')
        self.info_label.setText('Booking Complete')
        QMessageBox.information(self, "Notification", "Booking Complete!", QMessageBox.Ok)
        self.book_button.setEnabled(True)

    def finish_initialization(self, result):
        self.all_info = result
        self.initialize_button.setText('Initialization Complete')
        self.info_label.setText('Initialization Complete')
        QMessageBox.information(self, "Notification", "Initialization Complete!", QMessageBox.Ok)
        self.type_combobox.addItems(['Easton', 'Local'])
        self.book_button.setEnabled(True)


class BookingThread(QThread):
    finished_signal = pyqtSignal(int)

    def __init__(self, id):
        super().__init__()
        self.id = id

    def run(self):
        import selenium_mode
        result = selenium_mode.start(self.id)
        self.finished_signal.emit(result)


class InitializationThread(QThread):
    finished_signal = pyqtSignal(list)

    def run(self):
        result = select_info_demo.info_init()
        self.finished_signal.emit(result)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
