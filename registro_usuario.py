import conexion
import login
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *
class registro_usuario(QMainWindow):
    def reg_usu(self):

        uic.loadUi("ventana_registro_usuario.ui", self)
        self.setWindowTitle("REGISTRO DE USUARIO")



if __name__ == '__main__':
    app = QApplication(sys.argv)
    GUI = login()
    GUI.show()
    sys.exit(app.exec())
