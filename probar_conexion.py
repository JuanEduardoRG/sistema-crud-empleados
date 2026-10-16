import pyodbc

conexion = (
    "DRIVER={ODBC Driver 18 for SQL Server};"
    "SERVER=localhost\\SQLEXPRESS;"
    "DATABASE=EmpresaDB;"
    "Trusted_Connection=yes;"
    "TrustServerCertificate=yes;"
)

try:
    with pyodbc.connect(conexion) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT @@VERSION")
        version = cursor.fetchone()

        print("¡Conexión exitosa con SQL Server!")
        print(version[0])

except pyodbc.Error as error:
    print("No se pudo conectar:")
    print(error)
    