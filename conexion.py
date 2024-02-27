import pymysql
############### CONFIGURAR ESTO ###################
# Open database connection
try:
    db = pymysql.connect("localhost","root","","rnc")
##################################################
# prepare a cursor object using cursor() method
    cursor = db.cursor()
except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:
	print("Ocurrió un error al conectar: ", e)