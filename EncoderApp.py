import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QLabel, QDial
from PySide6.QtCore import Qt, QSettings

class EncoderApp(QWidget):
    def __init__(self):
        super().__init__()
        self.settings = QSettings("MyCompany", "EncoderApp")
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Encoder")
        self.setFixedSize(400, 300)

        self.layout = QVBoxLayout()
        self.layout.setSpacing(10)

        self.dial_label = QLabel("Dial Value:")
        self.layout.addWidget(self.dial_label, alignment=Qt.AlignmentFlag.AlignTop)

        self.dial = QDial(self)
        self.dial.setRange(0, 255)
        self.dial.setValue(self.settings.value("current_value", 0, type=int))
        self.dial.valueChanged.connect(self.update_textboxes)
        self.layout.addWidget(self.dial, alignment=Qt.AlignmentFlag.AlignCenter)

        self.value_textbox = QLineEdit(self)
        self.value_textbox.setPlaceholderText("Current Value")
        self.layout.addWidget(self.value_textbox)

        self.change_textbox = QLineEdit(self)
        self.change_textbox.setPlaceholderText("Increasing/Decreasing Value")
        self.layout.addWidget(self.change_textbox)

        self.value = self.settings.value("ackumlated_value", 0, type=int)
        self.previous_value = self.dial.value() - 1
        self.value_textbox.setText("Prev" + str(self.previous_value) + " val" + str(self.dial.value()))
        if self.settings.value("is_increased", False, type=bool):
            self.change_textbox.setText(f"Increased by {self.value}")
        else:
            self.change_textbox.setText(f"Decreased by {self.value}")

        self.setLayout(self.layout)

    def update_textboxes(self, value):
        self.value_textbox.setText("Prev" + str(self.previous_value) + " val" + str(value))
        # Not wrapped around
        if abs(value - self.previous_value) < 127:
            if (value - self.previous_value > 0):
                self.value += (value - self.previous_value)
                self.change_textbox.setText(f"Increased by {self.value}")
                self.settings.setValue("is_increased", True)
            elif (value - self.previous_value < 0):
                self.value -= (self.previous_value - value)
                self.change_textbox.setText(f"Decreased by {self.value}")
                self.settings.setValue("is_increased", False)
        # Wrapped around
        else:
            if value < self.previous_value:
                self.value += (value + (256 - self.previous_value))
                self.change_textbox.setText(f"Increased by {self.value}")
                self.settings.setValue("is_increased", True)
            else:
                self.value -= ((256 - value) + self.previous_value)
                self.change_textbox.setText(f"Decreased by {self.value}")
                self.settings.setValue("is_increased", False)
        self.settings.setValue("current_value", value)
        self.settings.setValue("ackumlated_value", self.value)
        self.previous_value = value

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = EncoderApp()
    ex.show()
    sys.exit(app.exec())
