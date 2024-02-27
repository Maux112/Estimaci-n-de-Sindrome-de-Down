from os import getcwd
import time
from PyQt5.QtCore import QRegExp, Qt
from PyQt5.QtGui import QRegExpValidator, QPixmap
import conexion
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import (QApplication, QMessageBox)
from datetime import datetime, date

from PyQt5.QtGui import QIcon, QFont, QTextDocument
from PyQt5.QtCore import Qt, QFileInfo, QTextCodec, QByteArray, QTranslator, QLocale, QLibraryInfo
from PyQt5.QtWidgets import (QApplication, QTreeWidget, QTreeWidgetItem, QDialog, QPushButton, QFileDialog,
                             QMessageBox, QToolBar)
from PyQt5.QtPrintSupport import QPrintDialog, QPrinter, QPrintPreviewDialog

TIME_LIMIT = 100


class login(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("ventana_login.ui", self)
        self.setWindowTitle("INICIO DE SESIÓN")
        self.btn_iniciar.clicked.connect(self.validarLogin)
        #self.btn_registrar.clicked.connect(self.ir_ventana_registrar)
        # self.btn_registrar.clicked.connect(self.irVentanaPrincipal)

        self.btn_registrar.clicked.connect(self.ir_ventana_registrar_Admin)


        self.setWindowTitle("Login")
        self.setWindowIcon(QIcon("C:/Users/HP/Desktop/TALLER/PresentacionFinal_DefensaPublica/Recursos/icon.jpg"))
        self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.MSWindowsFixedSizeDialogHint)
        # Para un tamnio en especifico de la ventana self.setFixedSize(400, 380)

    def validarLogin(self):
        print("estas en validarLogin")
        usuario = self.txt_usuario.text()
        clave = self.txt_clave.text()
        # print("Captura de datos exitoso: ", usuario, "and password:", clave)
        print("Captura de datos exitoso: ", usuario)
        contador = 0
        # aca realizo la consulta a la bd para validar el login
        conexion.cursor.execute(
            "SELECT * FROM login_usuario where usuario='{0}' and clave='{1}' and estado_login_usuario= 0  ".format(
                usuario, clave))
        '''verificacion de existencia de registro'''
        for row in conexion.cursor:
            contador = contador + 1

            global idLogin
            idLogin = row[0]
            # print(row)
            global codLogExam
            codLogExam = row[3]
            print(contador)

        if contador == 1:
            # poner esto en una funcion
            self.irMenuPrincipal()
        else:
            if self.txt_clave.text() == "" or self.txt_usuario.text() == "":

                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setText("Usuario y/o contraseña vacios")
                msg.setInformativeText('Llenar campos vacios')
                msg.setWindowTitle("Llenar campos")
                msg.exec_()

            else:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Error de inicio de sesión")
                msg.setInformativeText('Sesión incorrecta')
                msg.setWindowTitle("Error")
                msg.exec_()
                self.txt_clave.clear()
                self.txt_usuario.clear()

    # A parir de aca estamos en la ventana Login Admin==========================================================================
    def ir_ventana_registrar_Admin(self):
        print("estas en login admin")
        uic.loadUi("ventana_login_Admin.ui", self)
        self.setWindowTitle("Login administrador")
        self.btn_Admin_registrar.clicked.connect(self.validarLoginAdmin)
        self.btn_Admin_Volver.clicked.connect(self.volver)


    def validarLoginAdmin(self):
        print("estas en validarLogin")
        admin = self.txt_usuario_Admin.text()
        claveAdmin = self.txt_clave_Admin.text()
        print(admin,claveAdmin)
        if self.txt_clave_Admin.text() == "" or self.txt_usuario_Admin.text() == "":
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Usuario y/o contraseña vacios")
            msg.setInformativeText('Llenar campos vacios')
            msg.setWindowTitle("Llenar campos")
            msg.exec_()
        else:
            if self.txt_clave_Admin.text() == "admin" and self.txt_usuario_Admin.text() == "admin":
                self.ir_ventana_registrar()
            else:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Error de inicio de sesión")
                msg.setInformativeText('Sesión incorrecta')
                msg.setWindowTitle("Error")
                msg.exec_()
                self.txt_clave_Admin.clear()
                self.txt_usuario_Admin.clear()




    # A parir de aca estamos en la ventana registrar==========================================================================
    def ir_ventana_registrar(self):
        print("estas en registrar")
        uic.loadUi("ventana_registro_usuario.ui", self)
        self.setWindowTitle("REGISTRO DE USUARIO")
        self.btn_registrar_usuario.clicked.connect(self.registrarUsuario)
        self.btn_modificar.clicked.connect(self.modificararUsuario)
        self.btn_modificar.setDisabled(False)
        self.btn_modificar.setStyleSheet('''background-color : yellow
                                                                   text-decoration: none;font-family: georgia;
                                                                   padding: 10px;
                                                                   font-weight: 600;
                                                                   font-size: 20px;
                                                                   color: #0c343d;
                                                                   border-radius: 6px;
                                                                   border: 2px solid #cfe2f3;
                                                                    ''')
        self.btn_volver.clicked.connect(self.volver)
        self.btn_cancelar.clicked.connect(self.cancelarRegistro)
        # estas 3 lineas permiten solo numeros
        restrictOnlyNum = QRegExp("[0-9_]+")
        validator = QRegExpValidator(restrictOnlyNum)
        self.txt_ci_usuario.setValidator(validator)
        # Para el onfocus funciona esto es para validar el CI
        self.txt_ci_usuario.textEdited.connect(self.verificarCi)

        # En esta parte ejecutamos la funcion para ver la lista
        self.verListaUsuarios()

    def verificarCi(self):
        print("Estas en la verificación")
        ci = self.txt_ci_usuario.text()

        print("Captura de datos exitoso: ", ci)
        contadorCI = 0
        '''aca realizo la consulta a la bd para validar el login'''
        conexion.cursor.execute(
            "SELECT ci_medico FROM medico where ci_medico='{0}'".format(
                ci))
        '''verificacion de existencia de registro'''
        for row in conexion.cursor:
            contadorCI = contadorCI + 1
            print(row)
            print(contadorCI)
            self.txt_ci_usuario.clear()
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("El C.I. que ingresó ya se encuentra registrado")
            msg.setInformativeText('Llenar campos vacios')
            msg.setWindowTitle("Llenar campos")
            msg.exec_()

    def registrarUsuario(self):
        print("estas en registrar usuario")
        ci = self.txt_ci_usuario.text()
        nombre = self.txt_nombre.text()
        paterno = self.txt_paterno.text()
        materno = self.txt_materno.text()
        cargo = self.txt_cargo.text()
        telefono = self.txt_telefono.text()
        usuario = self.txt_usuario_reg.text()
        clave = self.txt_clave_reg.text()
        estado = self.cb_estado_usu.currentText()
        valnumEstado = 0
        if (estado == "Habilitado"):
            valnumEstado = 1
        # print(ci, nombre, paterno, materno, cargo, telefono, usuario, clave, valnumEstado)
        if ci == "" or nombre == "" or paterno == "" or materno == "" and cargo == "" or telefono == "" or usuario == "" or clave == "":
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Los campos se encuentra vacios")
            msg.setInformativeText('Llenar campos vacios')
            msg.setWindowTitle("Llenar campos")
            msg.exec_()

        else:
            conexion.cursor.execute('''INSERT INTO medico (id_medico,ci_medico,nombre_medico,paterno_medico,materno_medico,cargo_medico,telefono_medico,estado_medico)
                                        VALUES (NULL,'{0}','{1}','{2}','{3}','{4}','{5}',{6});                                                                    
                                        '''.format(ci, nombre, paterno, materno, cargo, telefono, valnumEstado))
            conexion.db.commit()
            conexion.cursor.execute('''INSERT INTO login_usuario (id_login_usuario,usuario,clave,id_medico_fk,estado_login_usuario) 
                                        VALUES(NULL,'{0}','{1}',(SELECT id_medico FROM medico ORDER BY id_medico desc limit 1),{2});
    
                                        '''.format(usuario, clave, valnumEstado))
            conexion.db.commit()

            self.verListaUsuarios()
            self.cancelarRegistro()

    def modificararUsuario(self):
        print("estas en registrar usuario")
        ci = self.txt_ci_usuario.text()
        nombre = self.txt_nombre.text()
        paterno = self.txt_paterno.text()
        materno = self.txt_materno.text()
        cargo = self.txt_cargo.text()
        telefono = self.txt_telefono.text()
        usuario = self.txt_usuario_reg.text()
        clave = self.txt_clave_reg.text()
        estado = self.cb_estado_usu.currentText()
        valnumEstado = 1
        if estado == "Habilitado":
            valnumEstado = 0
        # print(ci, nombre, paterno, materno, cargo, telefono, usuario, clave, valnumEstado)

        conexion.cursor.execute('''UPDATE medico SET nombre_medico='{1}',paterno_medico='{2}',materno_medico='{3}',cargo_medico='{4}',telefono_medico='{5}'
                                    WHERE ci_medico='{0}' ;                                                                    
                                    '''.format(ci, nombre, paterno, materno, cargo, telefono))
        conexion.db.commit()
        conexion.cursor.execute('''UPDATE login_usuario SET usuario='{0}',clave='{1}',estado_login_usuario={2} 
                                WHERE id_medico_fk=(SELECT id_medico from medico where ci_medico='{3}');

                                    '''.format(usuario, clave, valnumEstado, ci))
        conexion.db.commit()

        self.verListaUsuarios()
        self.cancelarRegistro()

    # Esta es la parte para ver la ista de usuarios
    def verListaUsuarios(self):
        # esta linea es para limpiar la lista
        self.lista_usuarios_reg.clear()
        # Esta parte es para llenar la lista de usuarios en registrar usuario
        '''aca realizo la consulta a la bd para validar el login'''
        conexion.cursor.execute(
            "SELECT usuario FROM login_usuario")
        '''RECORREMOS TODA LOS DATOS PARA MOSTRAR EN LA LISTVIEW'''
        for row in conexion.cursor:
            # print(row)
            self.lista_usuarios_reg.addItems(row)
        # esta linea de cod es para hacer algo cuando seleccionemos un ITEM en este caso el nombre de paciente ,le mandamos a la funcion obtenerItemSeleccionado
        self.lista_usuarios_reg.itemSelectionChanged.connect(self.obtenerItemSeleccionado)

    def obtenerItemSeleccionado(self):
        if not self.lista_usuarios_reg.hasFocus(): return
        for selectedItem in self.lista_usuarios_reg.selectedItems():
            if not selectedItem: continue
            if selectedItem.isHidden(): continue
            # imprimo el item seleccionado
            # print(selectedItem.text())
            # realiz la consulta en base al item seleccionado ,para que muetre en los texbox
            conexion.cursor.execute(
                "SELECT med.ci_medico, med.nombre_medico, med.paterno_medico, med.materno_medico, med.cargo_medico, med.telefono_medico,usu.usuario,usu.clave,usu.estado_login_usuario  FROM medico as med, login_usuario as usu WHERE med.id_medico=usu.id_medico_fk and usu.usuario='{0}'".format(
                    selectedItem.text()))
            for row in conexion.cursor:
                # imprimo los resultados por separado
                # print("=" * 10, "RESULTADOS DE LA CONSUTA", "=" * 10)
                # print(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8])
                # Aca desabilito el editText de Ci y el boton registrar y habilito el boton modificar
                self.btn_registrar_usuario.setDisabled(True)
                self.btn_modificar.setDisabled(False)
                self.btn_modificar.setStyleSheet('''text-decoration: none;font-family: georgia;
                                                                    padding: 10px;
                                                                    font-weight: 600;
                                                                    font-size: 20px;
                                                                    color: #0c343d;
                                                                    background-color: #cfe2f3;
                                                                    border-radius: 6px;
                                                                    border: 2px solid #cfe2f3;
                                                                    ''')

                self.btn_registrar_usuario.setStyleSheet('''background-color : yellow
                                                            text-decoration: none;font-family: georgia;
                                                            padding: 10px;
                                                            font-weight: 600;
                                                            font-size: 20px;
                                                            color: #0c343d;
                                                            border-radius: 6px;
                                                            border: 2px solid #cfe2f3;
                                                             ''')
                self.txt_ci_usuario.setDisabled(True)
                self.txt_ci_usuario.setText(row[0])
                self.txt_nombre.setText(row[1])
                self.txt_paterno.setText(row[2])
                self.txt_materno.setText(row[3])
                self.txt_cargo.setText(row[4])
                self.txt_telefono.setText(row[5])
                self.txt_usuario_reg.setText(row[6])
                self.txt_clave_reg.setText(row[7])
                if row[8] == 0:
                    self.cb_estado_usu.setCurrentIndex(0)
                else:
                    self.cb_estado_usu.setCurrentIndex(1)

            return selectedItem.text()

    def cancelarRegistro(self):
        # limpiamos el formulario
        self.txt_ci_usuario.setDisabled(False)
        self.txt_ci_usuario.clear()
        self.txt_nombre.clear()
        self.txt_paterno.clear()
        self.txt_materno.clear()
        self.txt_cargo.clear()
        self.txt_telefono.clear()
        self.txt_usuario_reg.clear()
        self.txt_clave_reg.clear()
        self.cb_estado_usu.setCurrentIndex(0)
        self.btn_registrar_usuario.setStyleSheet('''text-decoration: none;font-family: georgia;
                                                    padding: 10px;
                                                    font-weight: 600;
                                                    font-size: 20px;
                                                    color: #0c343d;
                                                    background-color: #cfe2f3;
                                                    border-radius: 6px;
                                                    border: 2px solid #cfe2f3;
                                                    ''')
        self.btn_modificar.setStyleSheet('''background-color : yellow
                                            text-decoration: none;font-family: georgia;
                                            padding: 10px;
                                            font-weight: 600;
                                            font-size: 20px;
                                            color: #0c343d;
                                            border-radius: 6px;
                                            border: 2px solid #cfe2f3;
                                             ''')

    # A parir de aca estamos en la ventana elegir que hacer==========================================================================
    def irMenuPrincipal(self):
        # Aca redirecciono a las ventanas de entrenar y examen
        uic.loadUi("ventana_menu_principal.ui", self)
        self.setWindowTitle("Menu principal")
        self.volver_venmenu.clicked.connect(self.volver)
        self.btn_ventana_examen.clicked.connect(self.ventanaregistrarPaciente)
        self.btn_entrenar.clicked.connect(self.entrenar)

    # A parir de aca estamos en la ventana registrar paceinte==========================================================================
    def ventanaregistrarPaciente(self):
        # Aca redirecciono a la ventana registrar paciente
        uic.loadUi("ventana_registro_paciente.ui", self)
        self.setWindowTitle("Registrar Paceinte")
        self.volverMenu.clicked.connect(self.irMenuPrincipal)
        # estas 3 lineas permiten solo numeros
        restrictOnlyNum2 = QRegExp("[0-9_]+")
        validator2 = QRegExpValidator(restrictOnlyNum2)
        self.txt_ci_paciente.setValidator(validator2)
        self.btn_reg_paciente.clicked.connect(self.registrarPaciente)
        self.btn_cancelar_reg_paciente.clicked.connect(self.cancelarRegPaci)

    def registrarPaciente(self):
        print("estas en registrar PACIENTE")
        ciPaciente = self.txt_ci_paciente.text()
        #extencionPaciente = self.txt_ci_extencion_paciente.text()
        extencionPaciente = self.cb_ci_extencion_paciente.currentText()
        # esta variable es para el carotipo
        global nombrePacienteExam, fechNacExam, ciExamReport
        nombrePacienteExam = self.txt_nombre_paciente.text() + " " + self.txt_paterno_paciente.text() + " " + self.txt_materno_paciente.text()
        fechNacExam = self.fech_nac_paciente.text()
        ciExamReport = self.txt_ci_paciente.text()

        nombrePaciente = self.txt_nombre_paciente.text()
        paternoPaciente = self.txt_paterno_paciente.text()
        maternoPaciente = self.txt_materno_paciente.text()
        telefonoPaciente = self.txt_telef_paciente.text()
        fechaPaciente = self.fech_nac_paciente.text()
        print(ciPaciente,extencionPaciente, nombrePaciente, paternoPaciente, maternoPaciente, telefonoPaciente, fechaPaciente)
        if ciPaciente == "" or nombrePaciente == "" or paternoPaciente == "" or maternoPaciente == "" and telefonoPaciente == "" or fechaPaciente == "":
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Los campos se encuentra vacios")
            msg.setInformativeText('Llenar campos vacios')
            msg.setWindowTitle("Llenar campos")
            msg.exec_()
            self.irVentanaPrincipal()

        else:
            conexion.cursor.execute('''INSERT INTO `paciente`(`id_paciente`, `ci_paciente`,`ci_extencion_paciente`, `nombre_paciente`, `paterno_paciente`, `materno_paciente`, `telefono_paciente`, `fecha_nacimiento`, `estado_paciente`) 
                                        VALUES  (NULL,'{0}','{1}','{2}','{3}','{4}','{5}','{6}',0);                                                                    
                                        '''.format(ciPaciente, extencionPaciente, nombrePaciente, paternoPaciente,
                                                   maternoPaciente,
                                                   telefonoPaciente, fechaPaciente))
            conexion.db.commit()
            # Una vez registrado el paciente se habre la ventana principal
            self.irVentanaPrincipal()

    def cancelarRegPaci(self):
        self.txt_ci_paciente.clear()
        self.txt_nombre_paciente.clear()
        self.txt_paterno_paciente.clear()
        self.txt_materno_paciente.clear()
        self.txt_telef_paciente.clear()
        self.fech_nac_paciente.clear()

    # A parir de aca estamos en la ventana principal ==========================================================================
    def irVentanaPrincipal(self):
        # Aca redirecciono a las ventanas de entrenar y examen
        uic.loadUi("ventana_principal.ui", self)
        self.setWindowTitle("Cariotipo")
        # self.btn_salir_examen.clicked.connect(self.volver)
        self.initUI()
        self.btn_procesar.clicked.connect(self.procesar)
        self.btn_generar_reporte.clicked.connect(self.generarReporte)
        self.btn_actualizar_reportes.clicked.connect(self.Buscar)

        self.btn_limpiar.clicked.connect(self.limpiarTabla)
        self.btn_vistaPrevia.clicked.connect(self.vistaPrevia)
        self.btn_imprimir.clicked.connect(self.Imprimir)
        self.btn_exportar.clicked.connect(self.exportarPDF)
        self.btn_buscar.clicked.connect(self.buscarPorDato)
        # Botones de salir
        self.btn_salir_examen.clicked.connect(self.volver)
        self.btn_salir_reportes.clicked.connect(self.volver)

        # Esto es para la tabla
        self.tabla_Exam.setFont(QFont(self.tabla_Exam.font().family(), 10, False))
        self.tabla_Exam.setRootIsDecorated(False)
        self.tabla_Exam.setHeaderLabels(("Medico", "Paciente", "Fecha Examen", "Nombre Imagen",
                                         "Alto Imagen", "Ancho Imagen", "Extension Imagen", "Resultado"))

        self.model = self.tabla_Exam.model()

        for indice, ancho in enumerate((110, 110, 110, 110, 110, 110, 110, 110), start=0):
            self.model.setHeaderData(indice, Qt.Horizontal, Qt.AlignCenter, Qt.TextAlignmentRole)
            self.tabla_Exam.setColumnWidth(indice, ancho)

        self.tabla_Exam.setAlternatingRowColors(True)

        # self.verExamenes()

    # ======================= FUNCIONES PARA IMPRESION ============================

    # ======================= FUNCIONES ============================

    def Buscar(self):
        conexion.cursor.execute(
            "SELECT medico.nombre_medico, paciente.nombre_paciente, `fecha_examen`, `nombre_imagen`, `alto_imagen`, `ancho_imagen`, `extension_imagen`, `resultado` FROM `examen`,medico,paciente where examen.id_medico_fk=medico.id_medico and examen.id_paciente_fk=paciente.id_paciente ")
        # verificacion de existencia de registro
        datosDB = conexion.cursor.fetchall()

        if datosDB:
            self.documento.clear()
            self.tabla_Exam.clear()

            datos = ""
            item_widget = []
            for dato in datosDB:
                datos += "<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" % dato
                item_widget.append(QTreeWidgetItem((
                                                   str(dato[0]), str(dato[1]), str(dato[2]), str(dato[3]), str(dato[4]),
                                                   str(dato[5]), str(dato[6]), str(dato[7]))))

            reporteHtml = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
h3 {
    font-family: Helvetica-Bold;
    text-align: center;
    }

table {
        font-family: arial, sans-serif;
        border-collapse: collapse;
        width: 100%;
        }

td {
    text-align: left;
    padding-top: 4px;
    padding-right: 6px;
    padding-bottom: 2px;
    padding-left: 6px;
    }

th {
    text-align: left;
    padding: 4px;
    background-color: black;
    color: white;
    }

tr:nth-child(even) {
                    background-color: #dddddd;
                    }
</style>
</head>
<body>

<h3>LISTADO DE CARIOTIPOS<br/></h3>

<table align="left" width="100%" cellspacing="0">
    <tr>
    <th>Medico</th>
    <th>Paciente</th>
    <th>Fecha Examen</th>
    <th>Nombre Imagen</th>
    <th>Alto Imagen</th>
    <th>Ancho Imagen</th>
    <th>Extension Imagen</th>
    <th>Resultado</th>
    </tr>
    [DATOS]
</table>

</body>
</html>
""".replace("[DATOS]", datos)

            datos = QByteArray()
            datos.append(str(reporteHtml))
            codec = QTextCodec.codecForHtml(datos)
            unistr = codec.toUnicode(datos)

            if Qt.mightBeRichText(unistr):
                self.documento.setHtml(unistr)
            else:
                self.documento.setPlainText(unistr)

            self.tabla_Exam.addTopLevelItems(item_widget)
        else:
            QMessageBox.information(self, "Buscar usuarios", "No se encontraron resultados.",
                                    QMessageBox.Ok)

    def limpiarTabla(self):
        self.documento.clear()
        self.tabla_Exam.clear()

    def vistaPrevia(self):
        if not self.documento.isEmpty():
            impresion = QPrinter(QPrinter.HighResolution)

            vista = QPrintPreviewDialog(impresion, self)
            vista.setWindowTitle("Vista previa")
            vista.setWindowFlags(Qt.Window)
            vista.resize(800, 600)

            exportarPDF = vista.findChildren(QToolBar)
            exportarPDF[0].addAction(QIcon("exportarPDF.png"), "Exportar a PDF", self.exportarPDF)

            vista.paintRequested.connect(self.vistaPreviaImpresion)
            vista.exec_()
        else:
            QMessageBox.critical(self, "Vista previa", "No hay datos para visualizar.   ",
                                 QMessageBox.Ok)

    def vistaPreviaImpresion(self, impresion):
        self.documento.print_(impresion)

    def Imprimir(self):
        if not self.documento.isEmpty():
            impresion = QPrinter(QPrinter.HighResolution)

            dlg = QPrintDialog(impresion, self)
            dlg.setWindowTitle("Imprimir documento")

            if dlg.exec_() == QPrintDialog.Accepted:
                self.documento.print_(impresion)

            del dlg
        else:
            QMessageBox.critical(self, "Imprimir", "No hay datos para imprimir.   ",
                                 QMessageBox.Ok)

    def exportarPDF(self):
        if not self.documento.isEmpty():
            nombreArchivo, _ = QFileDialog.getSaveFileName(self, "Exportar a PDF", "Listado de Cariotipos",
                                                           "Archivos PDF (*.pdf);;All Files (*)",
                                                           options=QFileDialog.Options())

            if nombreArchivo:
                # if QFileInfo(nombreArchivo).suffix():
                #     nombreArchivo += ".pdf"

                impresion = QPrinter(QPrinter.HighResolution)
                impresion.setOutputFormat(QPrinter.PdfFormat)
                impresion.setOutputFileName(nombreArchivo)
                self.documento.print_(impresion)

                QMessageBox.information(self, "Exportar a PDF", "Datos exportados con éxito.   ",
                                        QMessageBox.Ok)
        else:
            QMessageBox.critical(self, "Exportar a PDF", "No hay datos para exportar.   ",
                                 QMessageBox.Ok)

    # def verExamenes(self):
    # conexion.cursor.execute(
    # "SELECT medico.nombre_medico, paciente.nombre_paciente, `fecha_examen`, `nombre_imagen`, `alto_imagen`, `ancho_imagen`, `extension_imagen`, `resultado` FROM `examen`,medico,paciente where examen.id_medico_fk=medico.id_medico and examen.id_paciente_fk=paciente.id_paciente ")
    # verificacion de existencia de registro

    def initUI(self):
        self.documento = QTextDocument()
        self.labelImagen.setAlignment(Qt.AlignCenter)
        # ===================== EVENTO QLABEL ======================

        # Llamar función al hacer clic sobre el label
        # self.labelImagen.clicked.connect(self.seleccionarImagen)

        # ================== EVENTOS QPUSHBUTTON ===================

        self.btn_subir_imagen.clicked.connect(self.seleccionarImagen)
        # self.btn_subir_imagen.clicked.connect(self.onButtonClick)
        self.btn_eliminar_imagen.clicked.connect(lambda: self.labelImagen.clear())

    def seleccionarImagen(self):
        imagen, extension = QFileDialog.getOpenFileName(self, "Seleccionar imagen", getcwd(),
                                                        "Archivos de imagen (*.png *.jpg)",
                                                        options=QFileDialog.Options())
        # esta parte es para ver la direccion de la imagen
        print(imagen, "estoy en imagen")
        global direccionImagen
        direccionImagen = str(imagen)
        print(direccionImagen, "estoy en imagen string")
        # print( extension,"estoy en extencion")
        # Para el tamanio de la imagen
        import cv2
        img = cv2.imread(direccionImagen)
        height, width, channels = img.shape
        print(height, width, channels)

        if imagen:
            # Adaptar imagen
            pixmapImagen = QPixmap(imagen).scaled(700, 250, Qt.KeepAspectRatio,
                                                  Qt.SmoothTransformation)
            self.barraCarga()
            # Mostrar imagen
            self.labelImagen.setPixmap(pixmapImagen)
            # para saber las caracteristicas de la imagen
            import os

            # Formateo de los caracteres
            # Formateo imagen
            ruta = imagen
            rutaImagen = (os.path.split(ruta))
            print(rutaImagen[1])
            extensionImagen = rutaImagen[1]
            extensionNombreImagenEsp = os.path.splitext(extensionImagen)
            print(extensionNombreImagenEsp)
            nombreImagen = str(extensionNombreImagenEsp[0])

            # Formateo extension
            extensionImagen2 = str(extensionNombreImagenEsp[1])
            print(extensionImagen2.split('.'))
            formatExtension = extensionImagen2.split('.')
            # Formateo alto ,ancho
            altoImagen = str(height) + " px"
            anchoImagen = str(width) + " px"
            if height > 600 or width > 600:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setText("Tamaño demasiado grande")
                msg.setInformativeText('Si la imagen es demasiada grande el proceso tardara bastante, procure utilizar imagenes menores a 600 x 600')
                msg.setWindowTitle("Tamaño")
                msg.exec_()




            # Coloco los resultados en los labels de la interfaz
            self.label_nombre.setText(nombreImagen)
            self.label_Extension.setText(str(formatExtension[1]))

            self.label_Alto.setText(altoImagen)
            self.label_Ancho.setText(anchoImagen)
            # para la fecha
            now = datetime.now()
            fechaExam = str(now.date())
            fechaExamFormat = fechaExam.replace("-", "/")
            print(fechaExamFormat)
            self.label_fecha_exam.setText(fechaExamFormat)

            print(nombrePacienteExam)
            print(fechNacExam)
            self.label_nombre_pac_Exam.setText(nombrePacienteExam)

            # Para la edad
            fechaNacExamFormat = fechNacExam.split("/")
            print(fechaNacExamFormat[0])
            print(fechaNacExamFormat[1])
            print(fechaNacExamFormat[2])

            from dateutil.relativedelta import relativedelta

            fecha_nacimiento = date(int(fechaNacExamFormat[0]), int(fechaNacExamFormat[1]), int(fechaNacExamFormat[2]))
            edad = date.today().year - fecha_nacimiento.year
            cumpleanios = fecha_nacimiento + relativedelta(years=edad)
            if cumpleanios > date.today():
                edad = edad - 1
            print(edad)
            self.label_edad_paciente.setText(str(edad))

    # esto es para el progressBar
    def barraCarga(self):
        count = 0
        while count < TIME_LIMIT:
            count += 1
            time.sleep(0.01)
            self.progressBar.setValue(count)

    def procesar(self):
        if direccionImagen == "":
            print("vacio")
        else:
            print(direccionImagen, "Lleno")
            import numpy as np
            from tensorflow.keras.preprocessing.image import load_img, img_to_array
            from tensorflow.keras.models import load_model

            longitud, altura = 224, 224
            modelo = 'C:/Users/HP/Desktop/TALLER/Versiones_Software/BaseFuncional/modelo/modelo.h5'
            pesos_modelo = 'C:/Users/HP/Desktop/TALLER/Versiones_Software/BaseFuncional/modelo/pesos.h5'
            cnn = load_model(modelo)
            cnn.load_weights(pesos_modelo)

            def predict(file):
                x = load_img(file, target_size=(longitud, altura))
                x = img_to_array(x)
                print(x)
                x = np.expand_dims(x, axis=0)
                print(x)
                model_out = cnn.predict([x])[0]
                print(model_out)
                array = cnn.predict(x)
                print(array)
                result = array[0]
                print(result)
                answer = np.argmax(result)

                if answer == 0:
                    print("pred: Descartado")
                    estimacion = 'Descartado'
                elif answer == 1:
                    print("pred: Positivo")
                    estimacion = 'Positivo'

                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Resultado")
                msg.setInformativeText(estimacion)
                msg.setWindowTitle("ESTIMACION DE SINDROME DE DOWN")
                msg.exec_()
                self.label_SD.setText(estimacion)

                return answer

            predict(direccionImagen)

    # Esto es para el boton de generar reporte y guardar
    def generarReporte(self):
        idMedico = codLogExam
        CIPaciente = ciExamReport
        print(idMedico)
        print(CIPaciente)
        resultadoExam = self.label_SD.text()
        nombreIMG = self.label_nombre.text()
        extencionIMG = self.label_Extension.text()
        altoIMG = self.label_Alto.text()
        anchoIMG = self.label_Ancho.text()

        print(resultadoExam)
        print(nombreIMG)
        print(extencionIMG)
        print(altoIMG)
        print(anchoIMG)
        conexion.cursor.execute('''INSERT INTO `examen`(`id_examen`, `id_medico_fk`, `id_paciente_fk`, `fecha_examen`, `nombre_imagen`, `alto_imagen`, `ancho_imagen`, `extension_imagen`, `resultado`, `estado_examen`)
                                    VALUES (NULL,'{0}',(SELECT `id_paciente` FROM `paciente` WHERE`ci_paciente`='{1}'),NOW(),'{2}','{3}','{4}','{5}','{6}',0)
                                '''.format(idMedico, CIPaciente, nombreIMG, altoIMG, anchoIMG, extencionIMG,
                                           resultadoExam))
        conexion.db.commit()

        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Estado")
        msg.setInformativeText("DATOS GUARDADOS")
        msg.setWindowTitle("REPORTE")
        msg.exec_()

    # Entrenamiento =======================================================================================================
    def entrenar(self):
        self.volver_venmenu.setDisabled(True)
        self.btn_ventana_examen.setDisabled(True)
        import sys
        import os
        from tensorflow.python.keras.preprocessing.image import ImageDataGenerator
        from tensorflow.python.keras.models import Sequential
        from tensorflow.python.keras.layers import Dropout, Flatten, Dense, Activation
        from tensorflow.python.keras.layers import Convolution2D, MaxPooling2D
        from tensorflow.python.keras import backend as K
        from tensorflow.python.keras import applications

        from tensorflow.keras.optimizers import Adam

        # new variables
        import numpy as np
        import pandas as pd
        import matplotlib.pyplot as plt
        import matplotlib.image as mpimg
        from mlxtend.evaluate import confusion_matrix
        from keras.preprocessing import image
        from tensorflow.python.keras.applications.mobilenet import preprocess_input
        import itertools

        def modelo():
            vgg = applications.vgg16.VGG16()
            vgg.summary()
            cnn = Sequential()
            for capa in vgg.layers:
                cnn.add(capa)
            cnn.layers.pop()
            for layer in cnn.layers:
                layer.trainable = False
            cnn.add(Dense(2, activation='softmax'))
            return cnn

        K.clear_session()

        data_entrenamiento = 'C:/Users/HP/Desktop/TALLER/Versiones_Software/BaseFuncional/data2/entrenamiento'
        data_validacion = 'C:/Users/HP/Desktop/TALLER/Versiones_Software/BaseFuncional/data2/validacion'

        # numero de iteraciones
        #epocas = 3
        epocas = 15
        longitud, altura = 224, 224
        # Numero de imagenes
        #batch_size = 2
        batch_size = 4
        #pasos = 3
        pasos = 12
        # depues de las epocas con el dataset de validacion
        #validation_steps = 3
        validation_steps = 12
        # numero de filtros por convolucion
        filtrosConv1 = 32
        filtrosConv2 = 64
        tamano_filtro1 = (3, 3)
        tamano_filtro2 = (2, 2)
        tamano_pool = (2, 2)
        clases = 2
        lr = 0.0005

        conexion.cursor.execute('''INSERT INTO `rnc`(`id_rnc`, `id_login_usuario_fk`, `numero_convoluciones`, `numero_polling`, `epocas`, `batch_size`,pasos, `validation_steps`, `lr`) 
                                                        VALUES (Null,'{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}')
                                                        '''.format(idLogin, 2, 2, epocas, batch_size, pasos,
                                                                   validation_steps, lr))
        conexion.db.commit()

        # Se formatean las imagenes

        entrenamiento_datagen = ImageDataGenerator(
            rescale=1. / 255,
            shear_range=0.2,
            zoom_range=0.2,
            horizontal_flip=True)

        test_datagen = ImageDataGenerator(rescale=1. / 255)
        # test_datagen = ImageDataGenerator(rescale=1. / 500)

        entrenamiento_generador = entrenamiento_datagen.flow_from_directory(
            data_entrenamiento,
            target_size=(altura, longitud),
            batch_size=batch_size,
            class_mode='categorical')

        validacion_generador = test_datagen.flow_from_directory(
            data_validacion,
            target_size=(altura, longitud),
            batch_size=batch_size,
            class_mode='categorical')
        print(entrenamiento_generador.class_indices)

        # cnn = Sequential()
        # cnn.add(Convolution2D(filtrosConv1, tamano_filtro1, padding ="same", input_shape=(longitud, altura, 3), activation='relu'))
        # cnn.add(MaxPooling2D(pool_size=tamano_pool))

        # cnn.add(Convolution2D(filtrosConv2, tamano_filtro2, padding ="same"))
        # cnn.add(MaxPooling2D(pool_size=tamano_pool))

        # # aca aumente
        # cnn.add(Convolution2D(filtrosConv2, tamano_filtro2, padding ="same"))
        # cnn.add(MaxPooling2D(pool_size=tamano_pool))
        # cnn.add(Convolution2D(filtrosConv2, tamano_filtro2, padding ="same"))
        # cnn.add(MaxPooling2D(pool_size=tamano_pool))

        # cnn.add(Flatten())
        # cnn.add(Dense(256, activation='relu'))
        # cnn.add(Dropout(0.5))
        # cnn.add(Dense(clases, activation='softmax'))
        cnn = modelo()
        cnn.summary()
        cnn.compile(loss='categorical_crossentropy',
                    optimizer=Adam(lr=lr),
                    metrics=['accuracy'])

        H = cnn.fit_generator(
            entrenamiento_generador,
            steps_per_epoch=pasos,
            epochs=epocas,
            validation_data=validacion_generador,
            validation_steps=validation_steps)

        # cnn.fit_generator(entrenamiento_generador, validacion_generador, batch_size=32, epochs=20,verbose=1, validation_split=0.2)

        N = epocas
        plt.style.use("ggplot")
        plt.figure()
        plt.plot(np.arange(0, N), H.history["loss"], label="train_loss")
        plt.plot(np.arange(0, N), H.history["val_loss"], label="val_loss")
        plt.plot(np.arange(0, N), H.history["accuracy"], label="train_acc")
        plt.plot(np.arange(0, N), H.history["val_accuracy"], label="val_acc")
        plt.title("Training loss and Accuary on Dataset")
        plt.xlabel("Epoch #")
        plt.ylabel("Loss/Accuary")
        plt.legend(loc="lower left")
        plt.savefig("plot.png")
        plt.show()

        test_datagen = ImageDataGenerator(preprocessing_function=preprocess_input)

        test_generator = test_datagen.flow_from_directory(
            directory="C:/Users/HP/Desktop/TALLER/Versiones_Software/BaseFuncional/data2/pruebas",
            target_size=(longitud, altura),
            color_mode="rgb",
            batch_size=1,
            class_mode=None,
            shuffle=False,
            seed=42
        )

        STEP_SIZE_TEST = test_generator.n // test_generator.batch_size
        test_generator.reset()
        pred = cnn.predict_generator(test_generator, steps=STEP_SIZE_TEST, verbose=1)

        predicted_class_indices = np.argmax(pred, axis=1)

        print(predicted_class_indices)
        print(type(predicted_class_indices))

        labels = (entrenamiento_generador.class_indices)
        labels = dict((v, k) for k, v in labels.items())
        predictions = [labels[k] for k in predicted_class_indices]

        filenames = test_generator.filenames
        results = pd.DataFrame({"Filename": filenames,
                                "Predictions": predictions})
        results.to_csv("results1.csv", index=False)

        real_class_indices = []
        for i in range(0, len(filenames)):
            your_path = filenames[i]
            path_list = your_path.split(os.sep)
            if ("descartado" in path_list[1]):
                real_class_indices.append(0)
            if ("positivo" in path_list[1]):
                real_class_indices.append(1)
        print(real_class_indices)
        print(len(real_class_indices))
        real_class_indices = np.array(real_class_indices)
        print(type(real_class_indices))


        # Desde aca no funcionaba
        fig = plt.figure(figsize=(30, 30))
        fig.subplots_adjust(hspace=0.1, wspace=0.1)
        rows = 10
        cols = len(filenames) // rows if len(filenames) % 2 == 0 else len(filenames) // rows + 1
        folder = "C:/Users/HP/Desktop/TALLER/Versiones_Software/BaseFuncional/data2/pruebas/test_images/"
        for i in range(0, len(filenames)):
            your_path = filenames[i]
            path_list = your_path.split(os.sep)
            img = mpimg.imread(folder + path_list[1])
            ax = fig.add_subplot(rows, cols, i + 1)
            ax.axis('off')

            plt.imshow(img, interpolation=None)
            ax.set_title(predictions[i], fontsize=20)
        #Hata aca buscar solucion // ya esta bien solo cambien la linea 916 por == porque esta -- error de igualacion

        cm = confusion_matrix(real_class_indices, predicted_class_indices)

        def plot_confusion_matrix(cm, classes,
                                  normalize=False,
                                  title='Confusion Matrix',
                                  cmap=plt.cm.Blues):
            plt.imshow(cm, interpolation='nearest', cmap=cmap)
            plt.title(title)
            plt.colorbar()
            tick_marks = np.arange(len(classes))
            plt.xticks(tick_marks, classes, rotation=45)
            plt.yticks(tick_marks, classes)

            if normalize:
                cm = cm.astype('float') / cm.sum(axis - 1)[:, np.newaxis]
                print("Normalized confusion Matrix")
            else:
                print("Confusion matrix,sin normalizacion")
            print(cm)

            thresh = cm.max() / 2.
            for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
                plt.text(j, i, cm[i, j],
                         horizontalalignment="center",
                         color="white" if cm[i, j] > thresh else "black")
            plt.tight_layout()
            plt.ylabel('True label')
            plt.xlabel('Predicted label')
            plt.show()

        cm_plot_labels = entrenamiento_generador.class_indices
        plot_confusion_matrix(cm, cm_plot_labels, title='Matriz de confusion')

        target_dir = 'C:/Users/HP/Desktop/TALLER/Versiones_Software/BaseFuncional/modelo/'
        if not os.path.exists(target_dir):
            os.mkdir(target_dir)
        cnn.save('C:/Users/HP/Desktop/TALLER/Versiones_Software/BaseFuncional/modelo/modelo.h5')
        cnn.save_weights('C:/Users/HP/Desktop/TALLER/Versiones_Software/BaseFuncional/modelo/pesos.h5')

        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Estado")
        msg.setInformativeText("Entrenamiento finalizado")
        msg.setWindowTitle("Entrenamiento")
        msg.exec_()
        self.volver_venmenu.setDisabled(False)
        self.btn_ventana_examen.setDisabled(False)

    def buscarPorDato(self):
        dato = self.txt_buscar.text()
        conexion.cursor.execute(
            '''SELECT medico.nombre_medico, paciente.nombre_paciente, `fecha_examen`, `nombre_imagen`, `alto_imagen`, `ancho_imagen`, `extension_imagen`, `resultado` FROM `examen`,medico,paciente where examen.id_medico_fk=medico.id_medico and examen.id_paciente_fk=paciente.id_paciente   and paciente.nombre_paciente like '%{0}%'
                        '''.format(dato))
        # verificacion de existencia de registro
        datosDB = conexion.cursor.fetchall()

        if datosDB:
            self.documento.clear()
            self.tabla_Exam.clear()

            datos = ""
            item_widget = []
            for dato in datosDB:
                datos += "<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" % dato
                item_widget.append(QTreeWidgetItem((
                    str(dato[0]), str(dato[1]), str(dato[2]), str(dato[3]), str(dato[4]),
                    str(dato[5]), str(dato[6]), str(dato[7]))))

            reporteHtml = """
        <!DOCTYPE html>
        <html>
        <head>
        <meta charset="UTF-8">
        <style>
        h3 {
            font-family: Helvetica-Bold;
            text-align: center;
            }

        table {
                font-family: arial, sans-serif;
                border-collapse: collapse;
                width: 100%;
                }

        td {
            text-align: left;
            padding-top: 4px;
            padding-right: 6px;
            padding-bottom: 2px;
            padding-left: 6px;
            }

        th {
            text-align: left;
            padding: 4px;
            background-color: black;
            color: white;
            }

        tr:nth-child(even) {
                            background-color: #dddddd;
                            }
        </style>
        </head>
        <body>

        <h3>LISTADO DE CARIOTIPOS<br/></h3>

        <table align="left" width="100%" cellspacing="0">
            <tr>
            <th>Medico</th>
            <th>Paciente</th>
            <th>Fecha Examen</th>
            <th>Nombre Imagen</th>
            <th>Alto Imagen</th>
            <th>Ancho Imagen</th>
            <th>Extension Imagen</th>
            <th>Resultado</th>
            </tr>
            [DATOS]
        </table>

        </body>
        </html>
        """.replace("[DATOS]", datos)

            datos = QByteArray()
            datos.append(str(reporteHtml))
            codec = QTextCodec.codecForHtml(datos)
            unistr = codec.toUnicode(datos)

            if Qt.mightBeRichText(unistr):
                self.documento.setHtml(unistr)
            else:
                self.documento.setPlainText(unistr)

            self.tabla_Exam.addTopLevelItems(item_widget)
        else:
            QMessageBox.information(self, "Buscar usuarios", "No se encontraron resultados.",
                                    QMessageBox.Ok)

    # ==================================================================================================r==========================================================================
    def volver(self):
        # Volver a inicio de sesion
        uic.loadUi("ventana_login.ui", self)
        self.setWindowTitle("INICIO DE SESIÓN")
        self.btn_iniciar.clicked.connect(self.validarLogin)
        self.btn_registrar.clicked.connect(self.ir_ventana_registrar_Admin)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    GUI = login()
    GUI.show()
    sys.exit(app.exec())
