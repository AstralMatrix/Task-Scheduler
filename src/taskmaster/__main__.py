#!/usr/bin/env python3
import sys
from PyQt5.QtWidgets import QApplication
from form import Form

app = QApplication(sys.argv)
ex = Form()
sys.exit(app.exec_())
