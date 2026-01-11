from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QTextEdit, QPushButton, QComboBox, QMessageBox
)
from PyQt6.QtGui import QIcon
import sys
import os

APP_VERSION = "4.1.0"


def resource_path(relative):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative)
    return os.path.join(os.path.dirname(__file__), relative)


def safe_split_strip(s):
    return [part.strip() for part in s.split() if part.strip()]


class DefusalLogic:
    @staticmethod
    def wires(s: str) -> str:
        parts = safe_split_strip(s)
        if len(parts) == 0:
            parts = list(s.strip())
        wires = [p[0].lower() for p in parts]
        n = len(wires)

        if n == 3:
            if 'r' not in wires:
                return 'Cut the first wire.'
            if 'w' in wires:
                return 'Cut the second wire.'
            if 'b' in wires:
                return 'Cut the last wire.'
            return 'No rule matched for 3 wires.'

        elif n == 4:
            if 'g' not in wires:
                return 'Cut the first wire.'
            if 'b' not in wires:
                return 'Cut the second wire.'
            if 'w' not in wires:
                return 'Cut the third wire.'
            return 'Cut the last wire.'

        elif n == 5:
            if '|' in s:
                light = s.split('|', 1)[1].strip().lower()
                lc = light[0] if light else ''
            else:
                return 'For 5 wires, provide the light color after a `|`.'

            if lc == 'r':
                return 'Cut the first wire.'
            if lc == 'g':
                return 'Cut the second wire.'
            if lc == 'b':
                return 'Cut the third wire.'
            if lc == 'y':
                return 'Cut the fourth wire.'
            return 'Cut the last wire.'

        return 'Wires module expects 3, 4, or 5 wires.'

    @staticmethod
    def button(s: str) -> str:
        parts = safe_split_strip(s.lower())
        if not parts:
            return 'Provide input like "blue detonate" or "red abort".'

        color = parts[0]
        text = ' '.join(parts[1:])

        if color == 'blue' and 'detonate' in text:
            return 'Press once and hold (follow release rules).'
        if color == 'red' and 'abort' in text:
            return 'Press and hold (follow indicator rules).'
        if color == 'red':
            return 'Press twice and then follow release rules.'
        if 'abort' in text:
            return 'Press 3 times and then follow release rules.'
        if color in ('grey', 'gray', 'white'):
            return 'Press 4 times and then follow release rules.'

        return 'No matching rule for the given button.'

    @staticmethod
    def hexadecimal(s: str) -> str:
        parts = safe_split_strip(s)
        if not parts:
            return 'Provide hex bytes like "41 42 43".'
        try:
            return 'Answer: ' + ''.join(chr(int(p, 16)) for p in parts)
        except Exception as e:
            return f'Error parsing hex: {e}'

    @staticmethod
    def tiles(s: str) -> str:
        parts = safe_split_strip(s)
        if not parts:
            parts = list(s.strip())
        if len(parts) < 2:
            return 'Provide two tile colors.'

        mapping = {'r': 1, 'g': 9, 'b': 7, 'y': 2, 'p': 6, 'w': 5}
        try:
            return f'Answer is {mapping[parts[0][0].lower()] + mapping[parts[1][0].lower()]}'
        except Exception:
            return 'Unknown tile color.'

    @staticmethod
    def keypads(s: str) -> str:
        parts = safe_split_strip(s)
        if len(parts) != 4:
            return 'Provide 4 numbers.'

        try:
            labels = [int(p) for p in parts]
        except ValueError:
            return 'All labels must be integers.'

        positions = ['top left', 'top right', 'bottom left', 'bottom right']
        order = [p for _, p in sorted(zip(labels, positions))]
        return 'Press in order: ' + ', '.join(order)

    @staticmethod
    def binary(s: str) -> str:
        bits = safe_split_strip(s)
        if len(bits) == 1:
            bits = list(bits[0])

        try:
            bits = [int(b) for b in bits]
        except Exception:
            return 'Binary must be 0s and 1s.'

        if len(bits) < 7:
            return 'Binary input must be at least 7 bits.'

        ones = bits.count(1)
        zeros = bits.count(0)

        if ones == 0:
            return 'Click red once.'
        if bits[1] == 1 and bits[6] == 0:
            return 'Click red twice.'
        if bits[0] == 1 and bits[1] == 1 and ones < 3:
            return 'Click red three times.'
        if zeros > 3:
            return 'Click red seven times.'
        if ones > 5:
            return 'Click red eight times.'
        if ones == 7:
            return 'Click red nine times.'

        return 'Click red ten times.'

    @staticmethod
    def mathematics(s: str) -> str:
        mapping = {'a': '1', 'b': '3', 'c': '7', 'd': '2', 'e': '4',
                   'f': '5', 'g': '6', 'h': '0', 'i': '8', 'j': '9'}

        s = s.strip().lower()
        if len(s) != 4:
            return 'Provide exactly 4 letters (a–j).'

        try:
            digits = ''.join(mapping[c] for c in s)
            return str(int(digits[:2]) * int(digits[2:]))
        except KeyError:
            return 'Letters must be a–j.'

    @staticmethod
    def color_code(s: str) -> str:
        if '|' not in s:
            return 'Provide "lights | display".'

        lights, display = map(str.strip, s.split('|', 1))
        md = {'r': 1, 'g': 3, 'b': 2, 'y': 3, 'w': 4}
        ml = {'r': 0, 'g': 0, 'b': 1, 'y': 2, 'w': 3}

        diff = sum(md.get(c, 0) for c in display.lower()) - \
               sum(ml.get(c, 0) for c in lights.lower())

        return 'Submit without pressing the red button.' if diff <= 0 else f'Press the button {diff} times.'

    @staticmethod
    def multi_buttons(s: str) -> str:
        parts = safe_split_strip(s)
        if len(parts) != 6:
            return 'Provide 6 numbers.'

        try:
            nums = [int(p) for p in parts]
        except ValueError:
            return 'All inputs must be integers.'

        base = ['red', 'orange', 'yellow', 'green', 'blue', 'purple']
        alt = ['orange', 'red', 'green', 'yellow', 'purple', 'blue']

        colors = [base[i] if n < 6 else alt[i] for i, n in enumerate(nums)]
        order = list(dict.fromkeys(colors))
        return 'Press in the following order: ' + ', '.join(order)

    @staticmethod
    def timing(s: str) -> str:
        parts = safe_split_strip(s)
        if len(parts) < 2:
            return 'Provide "12 ab".'

        try:
            x = int(parts[0][0]) + int(parts[0][1])
        except Exception:
            return 'Invalid digits.'

        mapping = {'a': 4, 'b': 3, 'c': 7, 'd': 9}
        y = sum(mapping.get(c, 0) for c in parts[1][:2])
        z = x * y

        thresholds = [(60, 'white'), (100, 'red'), (200, 'yellow'),
                      (300, 'green'), (400, 'blue'), (500, 'yellow'),
                      (600, 'red')]

        for limit, color in thresholds:
            if z < limit:
                return f'Press on {color}.'

        return 'Press on white.'

    @staticmethod
    def divisibility(s: str) -> str:
        parts = safe_split_strip(s)
        out = []

        for p in parts[:3]:
            try:
                n = int(p)
            except ValueError:
                out.append(f'{p}: invalid')
                continue

            flags = [n % d == 0 for d in (2, 3, 5, 7)]
            if not any(flags):
                out.append(f'{n}: F')
            else:
                out.append(f'{n}: {"ABCDEF"[sum(flags)-1]}')

        return '\n'.join(out)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle(f'defuser v{APP_VERSION}')
        self.setWindowIcon(QIcon(resource_path("defusal.ico")))
        self.resize(700, 450)

        central = QWidget(self)
        self.setCentralWidget(central)

        layout = QVBoxLayout(central)

        top = QHBoxLayout()
        layout.addLayout(top)

        self.module_combo = QComboBox()
        self.module_combo.addItems([
            'wires', 'button', 'hexadecimal', 'tiles', 'keypads',
            'binary', 'mathematics', 'color code',
            'multi buttons', 'timing', 'divisibility'
        ])
        self.module_combo.currentTextChanged.connect(self.update_prompt)

        top.addWidget(QLabel('Module:'))
        top.addWidget(self.module_combo)

        self.prompt_label = QLabel()
        layout.addWidget(self.prompt_label)

        self.input_edit = QLineEdit()
        layout.addWidget(self.input_edit)

        run_btn = QPushButton('Run')
        run_btn.clicked.connect(self.run_module)
        layout.addWidget(run_btn)

        layout.addWidget(QLabel('Result:'))
        self.result_area = QTextEdit(readOnly=True)
        layout.addWidget(self.result_area)

        self.update_prompt(self.module_combo.currentText())

    def update_prompt(self, module):
        self.prompt_label.setText(f'Input for {module}:')

    def run_module(self):
        try:
            func = getattr(DefusalLogic, self.module_combo.currentText().replace(' ', '_'))
            self.result_area.setPlainText(func(self.input_edit.text()))
        except Exception as e:
            QMessageBox.warning(self, 'Error', str(e))


def main():
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(resource_path("defusal.ico")))

    win = MainWindow()
    win.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
