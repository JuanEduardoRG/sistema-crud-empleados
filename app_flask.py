
from flask import Flask, request, redirect, url_for
import pyodbc

app = Flask(__name__)


# CONEXION CON SQL SERVER
def conectar_bd():
    conexion = (
        "DRIVER={ODBC Driver 18 for SQL Server};"
        "SERVER=localhost\\SQLEXPRESS;"
        "DATABASE=EmpresaDB;"
        "Trusted_Connection=yes;"
        "TrustServerCertificate=yes;"
    )
    return pyodbc.connect(conexion)


# PAGINA PRINCIPAL: MOSTRAR EMPLEADOS
@app.route("/")
def inicio():
    with conectar_bd() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, nombre, puesto, salario
            FROM Empleados
            ORDER BY id
        """)
        empleados = cursor.fetchall()

    filas = ""

    for empleado in empleados:
        filas += f"""
        <tr>
            <td>{empleado.id}</td>
            <td>{empleado.nombre}</td>
            <td>{empleado.puesto}</td>
            <td>${empleado.salario:,.2f}</td>
            <td>
                <a class="editar"
                   href="/editar/{empleado.id}">Editar</a>

                <form class="form-eliminar"
                      action="/eliminar/{empleado.id}"
                      method="POST"
                      onsubmit="return confirm('¿Seguro que deseas eliminar a este empleado?');">
                    <button class="eliminar" type="submit">
                        Eliminar
                    </button>
                </form>
            </td>
        </tr>
        """

    return f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Sistema de empleados</title>

        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 30px;
                background: #f4f6f8;
                color: #222;
            }}

            .contenedor {{
                max-width: 1100px;
                margin: auto;
            }}

            .formulario {{
                background: white;
                padding: 24px;
                margin-bottom: 30px;
                border-radius: 8px;
            }}

            input {{
                display: block;
                width: 100%;
                box-sizing: border-box;
                padding: 10px;
                margin: 8px 0 15px;
            }}

            button, .editar {{
                display: inline-block;
                padding: 9px 13px;
                border: none;
                border-radius: 4px;
                color: white;
                text-decoration: none;
                cursor: pointer;
                font-size: 14px;
            }}

            button.guardar {{
                background: #222;
            }}

            .editar {{
                background: #1769aa;
            }}

            .eliminar {{
                background: #c62828;
            }}

            .form-eliminar {{
                display: inline;
                margin-left: 5px;
            }}

            table {{
                border-collapse: collapse;
                width: 100%;
                background: white;
            }}

            th, td {{
                border: 1px solid #ccc;
                padding: 12px;
                text-align: left;
            }}

            th {{
                background: #222;
                color: white;
            }}
        </style>
    </head>

    <body>
        <div class="contenedor">
            <h1>Mi sistema de empleados</h1>

            <div class="formulario">
                <h2>Registrar empleado</h2>

                <form action="/registrar" method="POST">
                    <label for="nombre">Nombre:</label>
                    <input type="text" id="nombre" name="nombre"
                           maxlength="100" required>

                    <label for="puesto">Puesto:</label>
                    <input type="text" id="puesto" name="puesto"
                           maxlength="100" required>

                    <label for="salario">Salario:</label>
                    <input type="number" id="salario" name="salario"
                           min="0" max="99999999.99" step="0.01" required>

                    <button class="guardar" type="submit">
                        Guardar empleado
                    </button>
                </form>
            </div>

            <h2>Empleados registrados</h2>

            <table>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Nombre</th>
                        <th>Puesto</th>
                        <th>Salario</th>
                        <th>Acciones</th>
                    </tr>
                </thead>

                <tbody>
                    {filas}
                </tbody>
            </table>
        </div>
    </body>
    </html>
    """


# REGISTRAR EMPLEADO
@app.route("/registrar", methods=["POST"])
def registrar():
    nombre = request.form["nombre"].strip()
    puesto = request.form["puesto"].strip()

    try:
        salario = float(request.form["salario"])

        if not nombre or not puesto:
            return "El nombre y el puesto son obligatorios.", 400

        if salario < 0 or salario > 99999999.99:
            return "El salario está fuera del rango permitido.", 400

        with conectar_bd() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO Empleados (nombre, puesto, salario)
                VALUES (?, ?, ?)
            """, (nombre, puesto, salario))
            conn.commit()

        return redirect(url_for("inicio"))

    except ValueError:
        return "El salario debe ser un número válido.", 400


# MOSTRAR FORMULARIO DE EDICION
@app.route("/editar/<int:id>")
def editar(id):
    with conectar_bd() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, nombre, puesto, salario
            FROM Empleados
            WHERE id = ?
        """, (id,))
        empleado = cursor.fetchone()

    if empleado is None:
        return "Empleado no encontrado.", 404

    return f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Editar empleado</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 30px;
                background: #f4f6f8;
            }}
            form {{
                background: white;
                padding: 24px;
                max-width: 500px;
                border-radius: 8px;
            }}
            input {{
                display: block;
                box-sizing: border-box;
                width: 100%;
                padding: 10px;
                margin: 8px 0 16px;
            }}
            button, a {{
                display: inline-block;
                padding: 10px 14px;
                border: none;
                border-radius: 4px;
                text-decoration: none;
                cursor: pointer;
            }}
            button {{
                background: #1769aa;
                color: white;
            }}
        </style>
    </head>
    <body>
        <h1>Editar empleado #{empleado.id}</h1>

        <form action="/actualizar/{empleado.id}" method="POST">
            <label for="nombre">Nombre:</label>
            <input type="text" id="nombre" name="nombre"
                   maxlength="100" value="{empleado.nombre}" required>

            <label for="puesto">Puesto:</label>
            <input type="text" id="puesto" name="puesto"
                   maxlength="100" value="{empleado.puesto}" required>

            <label for="salario">Salario:</label>
            <input type="number" id="salario" name="salario"
                   min="0" max="99999999.99" step="0.01"
                   value="{empleado.salario}" required>

            <button type="submit">Guardar cambios</button>
            <a href="/">Cancelar</a>
        </form>
    </body>
    </html>
    """


# ACTUALIZAR EMPLEADO
@app.route("/actualizar/<int:id>", methods=["POST"])
def actualizar(id):
    nombre = request.form["nombre"].strip()
    puesto = request.form["puesto"].strip()

    try:
        salario = float(request.form["salario"])

        if not nombre or not puesto:
            return "El nombre y el puesto son obligatorios.", 400

        if salario < 0 or salario > 99999999.99:
            return "El salario está fuera del rango permitido.", 400

        with conectar_bd() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE Empleados
                SET nombre = ?, puesto = ?, salario = ?
                WHERE id = ?
            """, (nombre, puesto, salario, id))

            if cursor.rowcount == 0:
                return "Empleado no encontrado.", 404

            conn.commit()

        return redirect(url_for("inicio"))

    except ValueError:
        return "El salario debe ser un número válido.", 400


# ELIMINAR EMPLEADO
@app.route("/eliminar/<int:id>", methods=["POST"])
def eliminar(id):
    with conectar_bd() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            DELETE FROM Empleados
            WHERE id = ?
        """, (id,))

        if cursor.rowcount == 0:
            return "Empleado no encontrado.", 404

        conn.commit()

    return redirect(url_for("inicio"))


# INICIAR APLICACION
if __name__ == "__main__":
    app.run(debug=True)
