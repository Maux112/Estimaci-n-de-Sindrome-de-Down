import conexion
# Prepare SQL query to READ a record into the database.
sql = "SELECT * FROM login_usuario "
# Execute the SQL command
conexion.cursor.execute(sql)
# Fetch all the rows in a list of lists.
results = conexion.cursor.fetchall()
for row in results:
   id = row[0]
   name = row[1]
   email = row[2]
   # Now print fetched result
   print ("id = {0}, name = {1}, email = {2}".format(id,name,email))

# disconnect from server
conexion.db.close()
