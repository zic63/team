import sys
from PyQt5.QtWidgets import QApplication
from gui.main_window import MainWindow

def main():
    app = QApplication(sys.argv)  # Создание экземпляра приложения PyQt
    mainWin = MainWindow()        # Создание экземпляра главного окна
    mainWin.show()                # Отображение главного окна
    sys.exit(app.exec_())         # Запуск основного цикла событий приложения

if __name__ == '__main__':
    main()
