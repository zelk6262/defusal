from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QTextEdit, QPushButton, QComboBox, QMessageBox
)
from PyQt6.QtGui import QIcon
import sys
import math
import os


def resource_path(relative):
    if hasattr(sys, '_MEIPASS'):
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
                return 'For 5 wires, provide the light color after a `|` (e.g. "r w b y p | green").'
            if lc == 'r':
                return 'Cut the first wire.'
            if lc == 'g':
                return 'Cut the second wire.'
            if lc == 'b':
                return 'Cut the third wire.'
            if lc == 'y':
                return 'Cut the fourth wire.'
            return 'Cut the last wire.'
        else:
            return 'Wires module expects 3, 4, or 5 wires.'

    @staticmethod
    def button(s: str) -> str:
        parts = safe_split_strip(s.lower())
        if not parts:
            return 'Provide two words like "blue detonate" or "red".'
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
            return 'Provide space-separated two-digit hex bytes, e.g. "41 42 43".'
        try:
            chars = ''.join(chr(int(p, 16)) for p in parts)
            return f'Answer: {chars}'
        except Exception as e:
            return f'Error parsing hex: {e}'

    @staticmethod
    def tiles(s: str) -> str:
        parts = safe_split_strip(s)
        if len(parts) == 0:
            parts = list(s.strip())
        if len(parts) < 2:
            return 'Provide two tile colors (e.g. "r g" or "red green").'
        mapping = {'r': 1, 'g': 9, 'b': 7, 'y': 2, 'p': 6, 'w': 5}
        try:
            vals = [mapping[p[0].lower()] for p in parts[:2]]
            return f'Answer is {vals[0] + vals[1]}'
        except Exception:
            return 'Unknown tile color. Use r,g,b,y,p,w.'

    @staticmethod
    def keypads(s: str) -> str:
        parts = safe_split_strip(s)
        if len(parts) != 4:
            return 'Provide 4 numbers separated by spaces.'
        try:
            labels = [int(p) for p in parts]
        except ValueError:
            return 'All labels must be integers.'
        positions = ['top left', 'top right', 'bottom left', 'bottom right']
        paired = list(zip(labels, positions))
        paired.sort(key=lambda x: x[0])
        order = [pos for _, pos in paired]
        return 'Press in order: ' + ', '.join(order)

    @staticmethod
    def binary(s: str) -> str:
        bits = safe_split_strip(s)
        if len(bits) == 1 and set(bits[0]) <= {'0', '1'}:
            bits = list(bits[0])
        try:
            bits = [int(b) for b in bits]
        except Exception:
            return 'Binary must be a sequence of 0s and 1s.'
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
        mapping = {'a':'1','b':'3','c':'7','d':'2','e':'4','f':'5','g':'6','h':'0','i':'8','j':'9'}
        s = s.strip().lower()
        if len(s) != 4 or not all(ch.isalpha() for ch in s):
            return 'Provide exactly 4 letters (a-j).'
        try:
            digits = ''.join(mapping[ch] for ch in s)
            n1 = int(digits[:2])
            n2 = int(digits[2:])
            return str(n1 * n2)
        except KeyError:
            return 'Letters must be in range a-j.'

    @staticmethod
    def color_code(s: str) -> str:
        if '|' not in s:
            return 'Provide "lights | display".'
        lights, display = [part.strip() for part in s.split('|',1)]
        x = 0
        mapping_display = {'r':1,'g':3,'b':2,'y':3,'w':4}
        mapping_lights = {'r':0,'g':0,'b':1,'y':2,'w':3}
        for ch in display:
            x += mapping_display.get(ch.lower(), 0)
        y = 0
        for ch in lights:
            y += mapping_lights.get(ch.lower(), 0)
        diff = x - y
        if diff <= 0:
            return 'Submit without pressing the red button.'
        return f'Press the button {diff} times.'

    @staticmethod
    def multi_buttons(s: str) -> str:
        parts = safe_split_strip(s)
        if len(parts) != 6:
            return 'Provide 6 numbers.'
        try:
            nums = [int(p) for p in parts]
        except ValueError:
            return 'All inputs must be integers.'
        colors = []
        for i, n in enumerate(nums):
            if n < 6:
                colors.append(['red','orange','yellow','green','blue','purple'][i%6])
            else:
                colors.append(['orange','red','green','yellow','purple','blue'][i%6])
        seen = []
        order = []
        for c in colors:
            if c not in seen:
                seen.append(c)
                order.append(c)
        return 'Press in the following order: ' + ', '.join(order)

    @staticmethod
    def timing(s: str) -> str:
        parts = safe_split_strip(s)
        if len(parts) < 2:
            return 'Provide a two-digit number pair and two letters ("12 ab").'
        numbers = parts[0]
        letters = parts[1]
        if len(numbers) < 2:
            return 'Need two digits.'
        try:
            x = int(numbers[0]) + int(numbers[1])
        except Exception:
            return 'Digits only.'
        mapping = {'a':4,'b':3,'c':7,'d':9}
        vals = [mapping.get(ch,0) for ch in letters[:2]]
        y = sum(vals)
        z = x * y
        if z < 60:
            return 'Press on white.'
        if z < 100:
            return 'Press on red.'
        if z < 200:
            return 'Press on yellow.'
        if z < 300:
            return 'Press on green.'
        if z < 400:
            return 'Press on blue.'
        if z < 500:
            return 'Press on yellow.'
        if z < 600:
            return 'Press on red.'
        return 'Press on white.'

    @staticmethod
    def divisibility(s: str) -> str:
        parts = safe_split_strip(s)
        if len(parts) == 0:
            return 'Provide up to 3 numbers.'
        out = []
        for p in parts[:3]:
            try:
                number = int(p)
            except ValueError:
                out.append(f'{p}: invalid')
                continue
            two = number % 2 == 0
            three = number % 3 == 0
            five = number % 5 == 0
            seven = number % 7 == 0
            if not (two or three or five or seven):
                out.append(f'{number}: F')
            elif two and not (three or five or seven):
                out.append(f'{number}: A')
            elif three and not (two or five or seven):
                out.append(f'{number}: D')
            elif five and not (two or three or seven):
                out.append(f'{number}: F')
            elif seven and not (two or three or five):
                out.append(f'{number}: C')
            else:
                scond = sum([two, three, five, seven])
                letters = ['A','B','C','D','E','F']
                out.append(f'{number}: {letters[(scond-1) % len(letters)]}')
        return '\n'.join(out)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Correct icon path for PyInstaller
        ico_path = resource_path("defusal.ico")
        self.setWindowIcon(QIcon(ico_path))

        self.setWindowTitle('defuser v4')
        self.resize(700, 450)

        central = QWidget()
        self.setCentralWidget(central)

        layout = QVBoxLayout()
        central.setLayout(layout)

        top = QHBoxLayout()
        layout.addLayout(top)

        self.module_combo = QComboBox()
        modules = ['wires','button','hexadecimal','tiles','keypads','binary','mathematics','color code','multi buttons','timing','divisibility']
        self.module_combo.addItems(modules)
        self.module_combo.currentTextChanged.connect(self.update_prompt)
        top.addWidget(QLabel('Module:'))
        top.addWidget(self.module_combo)

        self.prompt_label = QLabel('Input:')
        layout.addWidget(self.prompt_label)

        self.input_edit = QLineEdit()
        layout.addWidget(self.input_edit)

        self.run_btn = QPushButton('Run')
        self.run_btn.clicked.connect(self.run_module)
        layout.addWidget(self.run_btn)

        layout.addWidget(QLabel('Result:'))
        self.result_area = QTextEdit()
        self.result_area.setReadOnly(True)
        layout.addWidget(self.result_area)

        self.update_prompt(self.module_combo.currentText())

    def update_prompt(self, module_name: str):
        notes = {
            'wires': 'Enter wires as colors or letters separated by space (3-5). For 5 wires add light color after "|", e.g. "r w b y p | green"',
            'button': 'Enter like: "blue detonate" or "red" or "white abort"',
            'hexadecimal': 'Enter space-separated two-digit hex bytes: e.g. "41 42 43"',
            'tiles': 'Enter two tile colors, e.g. "r g" or "red green"',
            'keypads': 'Enter 4 integer labels like "12 4 8 25"',
            'binary': 'Enter a 7-bit string like "0110010"',
            'mathematics': 'Enter 4 letters a-j, e.g. "abcd"',
            'color code': 'Enter "lights | display", e.g. "rgby | rgbw"',
            'multi buttons': 'Enter 6 integers',
            'timing': 'Enter number pair + 2 letters, e.g. "12 ab"',
            'divisibility': 'Enter up to 3 numbers'
        }
        self.prompt_label.setText('Input: ' + notes.get(module_name, ''))

    def run_module(self):
        module = self.module_combo.currentText()
        user_input = self.input_edit.text()
        try:
            func = getattr(DefusalLogic, module.replace(' ', '_'))
        except AttributeError:
            QMessageBox.warning(self, 'Error', f'Module logic not found for: {module}')
            return
        try:
            res = func(user_input)
        except Exception as e:
            res = f'Error while running module: {e}'
        self.result_area.setPlainText(res)


def main():
    app = QApplication(sys.argv)

    app.setWindowIcon(QIcon(resource_path("defusal.ico")))

    win = MainWindow()
    win.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
