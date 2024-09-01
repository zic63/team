import sys
from PyQt5.QtWidgets import QApplication
from gui.main_window import MainWindow

def main():
    app = QApplication(sys.argv)  # Создаём экземпляр приложения PyQt
    mainWin = MainWindow()        # Создаём экземпляр главного окна
    mainWin.show()                # Отображаем главное окно
    sys.exit(app.exec_())         # Запускаем основной цикл событий приложения

if __name__ == '__main__':
    main()