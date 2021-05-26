#!/usr/bin/env python3
import sys
from package.src.form import Form
from PyQt5.QtWidgets import QApplication

app = QApplication(sys.argv)
ex = Form()
sys.exit(app.exec_())
