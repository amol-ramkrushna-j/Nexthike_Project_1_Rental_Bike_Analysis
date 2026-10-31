import sys
import subprocess

# Automatically check and install PyQt6 if missing
try:
    import PyQt6
except ImportError:
    print("PyQt6 is not installed. Installing it now...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "PyQt6"])
        import PyQt6
        print("PyQt6 installed successfully!")
    except Exception as e:
        print(f"Failed to auto-install PyQt6: {e}")
        print("Please manually run: pip install PyQt6 in your terminal.")
        sys.exit(1)

import math
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, 
    QGridLayout, QLineEdit, QPushButton, QMessageBox, QSizePolicy
)

class AdvancedCalculator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Professional Calculator (PyQt6)")
        self.setFixedSize(360, 580)
        
        self.expression = ""
        self.memory = 0.0  # Memory storage for CA/finance operations
        
        # Main Widget and Layout with clean margins
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setContentsMargins(12, 12, 12, 12)
        self.layout.setSpacing(10)
        
        # Display Screen
        self.display = QLineEdit()
        self.display.setReadOnly(True)
        self.display.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.display.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.display.setFixedHeight(70)
        self.display.setStyleSheet(
            "font-size: 32px; background-color: #2b2b2b; color: white; border-radius: 6px; padding: 5px 12px; border: 1px solid #444;"
        )
        self.layout.addWidget(self.display)
        
        # Buttons Grid Layout with balanced spacing
        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(8)
        self.layout.addLayout(self.grid_layout)
        
        self.create_buttons()
        self.apply_styles()

    def create_buttons(self):
        buttons = [
            ('MC', 0, 0, '#6c757d'), ('MR', 0, 1, '#6c757d'), ('M+', 0, 2, '#6c757d'), ('M-', 0, 3, '#6c757d'),
            ('C', 1, 0, '#d9534f'), ('(', 1, 1, '#444444'), (')', 1, 2, '#444444'), ('/', 1, 3, '#f0ad4e'),
            ('sin', 2, 0, '#555555'), ('cos', 2, 1, '#555555'), ('tan', 2, 2, '#555555'), ('*', 2, 3, '#f0ad4e'),
            ('7', 3, 0, '#333333'), ('8', 3, 1, '#333333'), ('9', 3, 2, '#333333'), ('-', 3, 3, '#f0ad4e'),
            ('4', 4, 0, '#333333'), ('5', 4, 1, '#333333'), ('6', 4, 2, '#333333'), ('+', 4, 3, '#f0ad4e'),
            ('1', 5, 0, '#333333'), ('2', 5, 1, '#333333'), ('3', 5, 2, '#333333'), ('=', 5, 3, '#5cb85c'),
            ('0', 6, 0, '#333333'), ('.', 6, 1, '#333333'), ('sqrt', 6, 2, '#555555'), ('^', 6, 3, '#f0ad4e'),
        ]

        for text, row, col, color in buttons:
            btn = QPushButton(text)
            btn.setFixedHeight(55)  # Uniform height for perfect vertical alignment
            btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {color};
                    color: white;
                    font-size: 16px;
                    font-weight: bold;
                    border-radius: 6px;
                    border: none;
                }}
                QPushButton:pressed {{
                    background-color: #555555;
                }}
            """)
            btn.clicked.connect(lambda checked, t=text: self.on_button_click(t))
            self.grid_layout.addWidget(btn, row, col)

    def apply_styles(self):
        self.setStyleSheet("background-color: #1e1e1e;")

    def on_button_click(self, char):
        if char == 'C':
            self.clear_all()
        elif char == '=':
            self.calculate()
        elif char == 'MC':
            self.memory = 0.0
        elif char == 'MR':
            self.expression += str(self.memory)
            self.display.setText(self.expression)
        elif char == 'M+':
            try:
                result = eval(self.expression, {"__builtins__": None}, {"math": math})
                self.memory += float(result)
            except Exception:
                pass
        elif char == 'M-':
            try:
                result = eval(self.expression, {"__builtins__": None}, {"math": math})
                self.memory -= float(result)
            except Exception:
                pass
        elif char == 'sqrt':
            self.expression += "math.sqrt("
            self.display.setText(self.expression)
        elif char == '^':
            self.expression += "**"
            self.display.setText(self.expression)
        elif char in ['sin', 'cos', 'tan']:
            self.expression += f"math.{char}(math.radians("
            self.display.setText(self.expression)
        else:
            self.expression += char
            self.display.setText(self.expression)

    def clear_all(self):
        self.expression = ""
        self.display.setText("")

    def calculate(self):
        try:
            result = str(eval(self.expression, {"__builtins__": None}, {"math": math}))
            self.expression = result
            self.display.setText(result)
        except Exception:
            QMessageBox.critical(self, "Error", "Invalid Expression")
            self.clear_all()

    def keyPressEvent(self, event):
        key = event.key()
        
        if key in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            self.calculate()
        elif key == Qt.Key.Key_Backspace:
            self.expression = self.expression[:-1]
            self.display.setText(self.expression)
        elif key == Qt.Key.Key_Escape:
            self.clear_all()
        else:
            text = event.text()
            if text in "0123456789+-*/().":
                self.expression += text
                self.display.setText(self.expression)
            elif text == "^":
                self.expression += "**"
                self.display.setText(self.expression)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    calc = AdvancedCalculator()
    calc.show()
    sys.exit(app.exec())