import sys
from PyQt5.QtWidgets import QApplication
from loading import LoadingScreen

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = LoadingScreen()
    window.show()
    sys.exit(app.exec_())
