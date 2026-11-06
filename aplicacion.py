# Importamos Flask y sus funciones
from flask import Flask, render_template, request, redirect, url_for, flash

# Importamos nuestra funcion de conexion
from conexion import conectar


# Creamos la aplicacion Flask
app = Flask(__name__)

# Configuramos la clave secreta para los mensajes flash
app.secret_key = "clave_examen_flask"


# RUTA PRINCIPAL
@app.route("/")
def inicio():

    return render_template("index.html")


# RUTA NOSOTROS
@app.route("/Nosotros")
def nosotros():

    return render_template("nosotros.html")


# RUTA ESTUDIANTES
@app.route("/estudiantes", methods=["GET", "POST"])
def estudiantes():

    conexion = conectar()

    if conexion is None:
        flash("No fue posible conectar con PostgreSQL", "error")
        return render_template("estudiantes.html", estudiantes=[])

    try:

        # Si el formulario envia datos mediante POST
        if request.method == "POST":

            # Recibimos los datos del formulario
            nombre = request.form.get("nombre", "").strip()
            carnet = request.form.get("carnet", "").strip()
            carrera = request.form.get("carrera", "").strip()
            correo = request.form.get("correo", "").strip()

            # Validamos que no existan campos vacios
            if not all([nombre, carnet, carrera, correo]):

                flash("Todos los campos son obligatorios", "error")

            else:

                try:

                    # Creamos un cursor
                    cursor = conexion.cursor()

                    # Insertamos el estudiante
                    cursor.execute("""
                        INSERT INTO estudiantes
                        (nombre, carnet, carrera, correo)
                        VALUES (%s, %s, %s, %s)
                    """, (nombre, carnet, carrera, correo))

                    # Confirmamos los cambios
                    conexion.commit()

                    flash("Estudiante registrado correctamente", "success")

                except Exception as error:

                    # Revertimos la operacion si ocurre un error
                    conexion.rollback()

                    flash("Error al registrar: carnet o correo duplicado", "error")

                finally:

                    cursor.close()

            # Cerramos la conexion y redirigimos
            conexion.close()

            return redirect(url_for("estudiantes"))

        # Consultamos los estudiantes registrados
        cursor = conexion.cursor()

        cursor.execute("""
            SELECT id, nombre, carnet, carrera, correo
            FROM estudiantes
            ORDER BY id DESC
        """)

        estudiantes = cursor.fetchall()

        cursor.close()

        return render_template("estudiantes.html", estudiantes=estudiantes)

    finally:

        # Cerramos la conexion
        conexion.close()


# EJECUTAMOS EL SERVIDOR
if __name__ == "__main__":

    app.run(debug=True)
