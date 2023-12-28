from flask import Flask, render_template, request, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
import sqlite3
import os

app = Flask(__name__, static_folder='static')

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Extensiones de archivos permitidas
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



@app.route('/unidades')
def mostrar_unidades():
    # Conexión a la base de datos
    conn = sqlite3.connect('GourmetCS50.db')
    cursor = conn.cursor()

    # Seleccionar todos los elementos de la tabla 'Unidades'
    cursor.execute('SELECT * FROM Unidades ORDER BY Unidades')
    unidades = cursor.fetchall()

    conn.close()

    return render_template('Unidades.html', unidades=unidades)

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/ingredientes')
def ingredientes():
    # Conexión a la base de datos
    conn = sqlite3.connect('GourmetCS50.db')
    cursor = conn.cursor()

    # Seleccionar todos los elementos de la tabla 'Ingredientes'
    cursor.execute('SELECT * FROM Ingredientes ORDER BY NombreIngre')
    ingredientes = cursor.fetchall()

    conn.close()

    return render_template('Ingredientes.html', ingredientes=ingredientes)

@app.route('/validar_unidad', methods=['POST'])
def validar_unidad():
    unidad_ingresada = request.form['unidad']

    # Conexión a la base de datos
    conn = sqlite3.connect('GourmetCS50.db')
    cursor = conn.cursor()

    # Verificar si la unidad ya existe en la tabla 'Unidades'
    cursor.execute('SELECT * FROM Unidades WHERE Unidades = ?', (unidad_ingresada,))
    existing_unit = cursor.fetchone()

    mensaje = None

    if existing_unit:
        mensaje = "La unidad ya existe."
    else:
        # Insertar la nueva unidad en la tabla 'Unidades'
        cursor.execute('INSERT INTO Unidades (Unidades) VALUES (?)', (unidad_ingresada,))
        conn.commit()
        mensaje = "La unidad ha sido incorporada con éxito."

    # Seleccionar todos los elementos de la tabla 'Unidades' después de la operación
    cursor.execute('SELECT * FROM Unidades ORDER BY Unidades')
    unidades = cursor.fetchall()

    conn.close()

    return render_template('Unidades.html', unidades=unidades, mensaje=mensaje)


@app.route('/eliminar_unidad', methods=['POST'])
def eliminar_unidad():
    unidad_id = request.form['unidad_id']
    conn = sqlite3.connect('GourmetCS50.db')
    cursor = conn.cursor()

    if request.method == 'POST':
        # Eliminar la unidad de la base de datos
        cursor.execute('DELETE FROM Unidades WHERE CodUni = ?', (unidad_id,))
        conn.commit()

        conn.close()
        return redirect(url_for('mostrar_unidades'))

    # Obtener la información de la unidad antes de eliminarla
    cursor.execute('SELECT * FROM Unidades WHERE CodUni = ?', (unidad_id,))
    unidad = cursor.fetchone()

    conn.close()

    return render_template('unidades.html', unidad=unidad)

@app.route('/editar_unidad', methods=['POST'])
def editar_unidad():
    # Obtener el ID de la unidad a editar desde el formulario
    unidad_id = request.form.get('editar_unidad_id')

    # Conectar a la base de datos SQLite
    conn = sqlite3.connect('GourmetCS50.db')
    cursor = conn.cursor()

    # Obtener los detalles de la unidad a editar
    cursor.execute('SELECT * FROM Unidades WHERE CodUni = ?', (unidad_id,))
    unidad = cursor.fetchone()

    # Cerrar la conexión a la base de datos
    conn.close()

    # Renderizar el formulario de edición con los detalles de la unidad
    return render_template('editar_unidad.html', unidad=unidad)

@app.route('/validar_edicion', methods=['POST'])
def validar_edicion():
    # Obtener los datos del formulario de edición
    unidad_id = request.form.get('unidad_id')
    unidad_ingresada = request.form.get('unidadNueva')

    # Conexión a la base de datos
    conn = sqlite3.connect('GourmetCS50.db')
    cursor = conn.cursor()

    # Verificar si la unidad ya existe en la tabla 'Unidades'
    cursor.execute('SELECT * FROM Unidades WHERE Unidades = ?', (unidad_ingresada,))
    existing_unit = cursor.fetchone()

    mensaje = None

    if existing_unit:
        mensaje = "La unidad ya existe."
    else:
        # La nueva unidad no existe, proceder con la edición
        cursor.execute('UPDATE Unidades SET Unidades = ? WHERE CodUni = ?', (unidad_ingresada, unidad_id))
        conn.commit()

    # Obtener la lista actualizada de unidades
    cursor.execute('SELECT * FROM Unidades ORDER BY Unidades')
    unidades = cursor.fetchall()

    conn.close()

    return render_template('Unidades.html', unidades=unidades, mensaje=mensaje)

@app.route('/reporte_unidades')
def reporte_unidades():
    # Conexión a la base de datos
    conn = sqlite3.connect('GourmetCS50.db')
    cursor = conn.cursor()

    # Seleccionar todos los elementos de la tabla 'Unidades'
    cursor.execute('SELECT * FROM Unidades ORDER BY Unidades')
    unidades = cursor.fetchall()

    conn.close()

    return render_template('Reporte_Unidades.html', unidades=unidades)

#-------------------------------------------------------------------------------------

@app.route('/ingredientes')
def mostrar_ingre():
    # Conexión a la base de datos
    conn = sqlite3.connect('GourmetCS50.db')
    cursor = conn.cursor()

    # Seleccionar todos los elementos de la tabla 'Ingredientes'
    cursor.execute('SELECT * FROM Ingredientes ORDER BY NombreIngre')
    ingredientes_lista = cursor.fetchall()  # Cambié el nombre de la variable

    conn.close()

    return render_template('ingredientes.html', ingredientes=ingredientes_lista)  # Cambié el nombre de la variable


@app.route('/eliminar_ingre', methods=['POST'])
def eliminar_ingre():
    ingre_nombre = request.form['ingre_nombre']
    conn = sqlite3.connect('GourmetCS50.db')
    cursor = conn.cursor()

    if request.method == 'POST':
        # Eliminar ingrediente de la base de datos
        cursor.execute('DELETE FROM Ingredientes WHERE NombreIngre = ?', (ingre_nombre,))
        conn.commit()

        conn.close()
        return redirect(url_for('mostrar_ingre'))

    cursor.execute('SELECT * FROM Ingredientes WHERE NombreIngre = ?', (ingre_nombre,))
    ingre = cursor.fetchone()

    conn.close()

    return render_template('Ingredientes.html', ingre=ingre)


@app.route('/ingremodifi')
def ingremodifi():
    # Conexión a la base de datos
    conn = sqlite3.connect('GourmetCS50.db')
    cursor = conn.cursor()

    # Seleccionar todos los elementos de la tabla 'Unidades'
    cursor.execute('SELECT * FROM Unidades ORDER BY Unidades')
    unidadesmodifi = cursor.fetchall()

    # Seleccionar todos los elementos de la tabla 'Ingredientes'
    cursor.execute('SELECT * FROM Ingredientes ORDER BY NombreIngre')
    ingredientes = cursor.fetchall()

    conn.close()

    return render_template('Ingremodifi.html', unidades=unidadesmodifi, ingredientes=ingredientes)

@app.route('/ingremodifi_actualizar', methods=['GET', 'POST'])
def ingremodifi_actualizar():
    nombre_ingrediente = request.form.get('ingreComboBox')
    unidadComboBox = request.form.get('unidadComboBox')
    costo = request.form.get('costo')
    fecha = request.form.get('fecha')
    comercio = request.form.get('comercio')
    grasasSat = request.form.get('grasasSat')
    grasasNosat = request.form.get('grasasNosat')
    hc = request.form.get('hc')
    azucares = request.form.get('azucares')
    proteinas = request.form.get('proteinas')
    sal = request.form.get('sal')
    calcio = request.form.get('calcio')
    colesterol = request.form.get('colesterol')
    omega3 = request.form.get('omega3')
    kcal = request.form.get('kcal')

    # Conexión a la base de datos
    conn = sqlite3.connect('GourmetCS50.db')
    cursor = conn.cursor()

    mensaje = None

    try:
        # Actualiza el Ingrediente en la tabla 'Ingredientes'
        cursor.execute('UPDATE Ingredientes SET CodUni=?, Costo=?, Fecha=?, Comercio=?, GrasasSat=?, GrasasNosat=?, HC=?, Azucares=?, Proteinas=?, Sal=?, Calcio=?, Colesterol=?, Omega3=?, kCal=? WHERE CodIngre=?',
                       (unidadComboBox, costo, fecha, comercio, grasasSat, grasasNosat, hc, azucares, proteinas, sal, calcio, colesterol, omega3, kcal, nombre_ingrediente))
        conn.commit()
        mensaje = "El ingrediente ha sido actualizado con éxito."
    except Exception as e:
        # Captura cualquier excepción y muestra un mensaje de error
        mensaje = f"Error al actualizar el ingrediente: {str(e)}"

    # Obtener la lista actualizada de unidades
    cursor.execute('SELECT * FROM Unidades ORDER BY Unidades')
    unidades = cursor.fetchall()

    # Obtener la lista actualizada de ingredientes
    cursor.execute('SELECT * FROM Ingredientes ORDER BY NombreIngre')
    ingredientes = cursor.fetchall()

    conn.close()

    # Pasar la lista de unidades a la plantilla
    return render_template('Ingremodifi.html', ingredientes=ingredientes, mensaje=mensaje, unidades=unidades)

@app.route('/valida_ingre', methods=['GET', 'POST'])
def valida_ingre():
     # Conexión a la base de datos
    ingre_nombre = request.form['ingreComboBox']
    conn = sqlite3.connect('GourmetCS50.db')
    cursor = conn.cursor()

    # Seleccionar todos los elementos de la tabla 'Ingredientes'
    cursor.execute('SELECT * FROM Ingredientes ORDER BY NombreIngre')
    ingredientes = cursor.fetchall()

    # Seleccionar todos los elementos de la tabla 'Unidades'
    cursor.execute('SELECT * FROM Unidades ORDER BY Unidades')
    unidades = cursor.fetchall()

    # Pasar la lista de unidades a la plantilla
    return render_template('Ingremodifi.html', ingredientes=ingredientes, unidades=unidades)

@app.route('/get_costo_by_ingre', methods=['POST'])
def get_datos_by_ingre():
    ingre_id = request.form.get('ingreComboBox')

    # Conexión a la base de datos
    conn = sqlite3.connect('GourmetCS50.db')
    cursor = conn.cursor()

    # Obtener todos los datos del ingrediente seleccionado
    cursor.execute('SELECT * FROM Ingredientes WHERE CodIngre = ?', (ingre_id,))
    ingrediente = cursor.fetchone()

    conn.close()

    # Crear un diccionario con los datos del ingrediente
    datos_ingrediente = {
        'unidad': ingrediente[2],
        'costo': ingrediente[3],
        'fecha': ingrediente[4],
        'comercio': ingrediente[5],
        'grasasSat': ingrediente[6],
        'grasasNosat': ingrediente[7],
        'hc': ingrediente[8],
        'azucares': ingrediente[9],
        'proteinas': ingrediente[10],
        'sal': ingrediente[11],
        'calcio': ingrediente[12],
        'colesterol': ingrediente[13],
        'omega3': ingrediente[14],
        'kcal': ingrediente[15],
    }

    return jsonify(datos_ingrediente)

@app.route('/ingrealta', methods=['GET', 'POST'])
def ingrealta():
    # Conexión a la base de datos
    conn = sqlite3.connect('GourmetCS50.db')
    cursor = conn.cursor()

    # Seleccionar todos los elementos de la tabla 'Unidades'
    cursor.execute('SELECT * FROM Unidades ORDER BY Unidades')
    unidades = cursor.fetchall()

    conn.close()

    return render_template('Ingrealta.html', unidades=unidades)
 
@app.route('/validar_ingre', methods=['GET', 'POST'])
def validar_ingre():
    nombre_ingrediente = request.form.get('nombre_ingre')
    unidadComboBox = request.form.get('unidadComboBox')
    costo = request.form.get('costo')
    fecha = request.form.get('fecha')
    comercio = request.form.get('comercio')
    grasasSat = request.form.get('grasasSat')
    grasasNosat = request.form.get('grasasNosat')
    hc = request.form.get('hc')
    azucares = request.form.get('azucares')
    proteinas = request.form.get('proteinas')
    sal = request.form.get('sal')
    calcio = request.form.get('calcio')
    colesterol = request.form.get('colesterol')
    omega3 = request.form.get('omega3')
    kcal = request.form.get('kcal')

    # Obtener la lista de unidades desde la base de datos
    conn = sqlite3.connect('GourmetCS50.db')
    cursor = conn.cursor()

    # Obtener las unidades para el combo box
    cursor.execute('SELECT NombreIngre FROM Ingredientes WHERE NombreIngre = ?', (nombre_ingrediente,))
    ingrediente = cursor.fetchone()

    mensaje = None

    if ingrediente:
        mensaje = "El ingrediente ya existe."
    else:
        # Insertar la nueva unidad en la tabla 'Unidades'
        cursor.execute('INSERT INTO Ingredientes (NombreIngre, CodUni, Costo, Fecha, Comercio, GrasasSat, GrasasNosat, HC, Azucares, Proteinas, Sal, Calcio, Colesterol, Omega3, kCal) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                       (nombre_ingrediente, unidadComboBox, costo, fecha, comercio, grasasSat, grasasNosat, hc, azucares, proteinas, sal, calcio, colesterol, omega3, kcal))
        conn.commit()
        mensaje = "El ingrediente ha sido incorporado con éxito."

    # Obtener la lista actualizada de unidades
    cursor.execute('SELECT NombreIngre FROM Ingredientes')
    ingredientes = cursor.fetchall()

    # Seleccionar todos los elementos de la tabla 'Unidades' después de la operación
    cursor.execute('SELECT * FROM Unidades ORDER BY Unidades')
    unidades = cursor.fetchall()

    conn.close()

    # Pasar la lista de unidades a la plantilla
    return render_template('Ingrealta.html', ingredientes=ingredientes, mensaje=mensaje, unidades=unidades)

@app.route('/unidadesIngre')
def mostrar_unidadesIngre():
    # Conexión a la base de datos
    conn = sqlite3.connect('GourmetCS50.db')
    cursor = conn.cursor()

    # Seleccionar todos los elementos de la tabla 'Unidades'
    cursor.execute('SELECT * FROM Unidades ORDER BY Unidades')
    unidades = cursor.fetchall()

    conn.close()

    return render_template('Ingrealta.html', unidades_ingre=unidades)

@app.route('/reporte_ingre')
def reporte_ingre():
    # Conexión a la base de datos
    conn = sqlite3.connect('GourmetCS50.db')
    cursor = conn.cursor()

    # Seleccionar todos los elementos de la tabla 'Ingredientes'
    cursor.execute('SELECT i.CodIngre, i.NombreIngre, u.Unidades, i.Costo, i.Fecha, i.Comercio, i.GrasasSat, i.GrasasNosat, i.HC, i.Azucares, i.Proteinas, i.Sal, i.Calcio, i.Colesterol, i.Omega3, i.kCal FROM Ingredientes i JOIN Unidades u ON i.CodUni = u.CodUni ORDER BY NombreIngre;')
    ingredientes = cursor.fetchall()

    conn.close()

    return render_template('Reporte_Ingre.html', ingredientes=ingredientes)

@app.route('/clase_recetas')
def clase_recetas():
    # Conexión a la base de datos
    conn = sqlite3.connect('GourmetCS50.db')
    cursor = conn.cursor()

    # Seleccionar todos los elementos de la tabla 'ClasePrepa'
    cursor.execute('SELECT * FROM ClasePrepa ORDER BY ClasePrepa')
    clases = cursor.fetchall()

    conn.close()

    return render_template('Clase_recetas.html', clases=clases)


@app.route('/reporte_clases')
def reporte_clases():
    # Conexión a la base de datos
    conn = sqlite3.connect('GourmetCS50.db')
    cursor = conn.cursor()

    # Seleccionar todos los elementos de la tabla 'ClasePrepa'
    cursor.execute('SELECT * FROM ClasePrepa ORDER BY ClasePrepa')
    clases = cursor.fetchall()

    conn.close()

    return render_template('Reporte_clases.html', clases=clases)

@app.route('/validar_clase', methods=['POST'])
def validar_clase():
    clase_ingresada = request.form['clase']

    # Conexión a la base de datos
    conn = sqlite3.connect('GourmetCS50.db')
    cursor = conn.cursor()

    # Verificar si la clase ya existe en la tabla 'ClasePrepa'
    cursor.execute('SELECT * FROM ClasePrepa WHERE ClasePrepa = ?', (clase_ingresada,))
    existing_clase = cursor.fetchone()

    mensaje = None

    if existing_clase:
        mensaje = "La clase ya existe."
    else:
        # Insertar la nueva unidad en la tabla 'Unidades'
        cursor.execute('INSERT INTO ClasePrepa (ClasePrepa) VALUES (?)', (clase_ingresada,))
        conn.commit()
        mensaje = "La clase ha sido incorporada con éxito."

    # Seleccionar todos los elementos de la tabla 'Clases' después de la operación
    cursor.execute('SELECT * FROM ClasePrepa ORDER BY ClasePrepa')
    clases = cursor.fetchall()

    conn.close()

    return render_template('Clase_recetas.html', clases=clases, mensaje=mensaje)

@app.route('/clases')
def mostrar_clases():
    # Conexión a la base de datos
    conn = sqlite3.connect('GourmetCS50.db')
    cursor = conn.cursor()

    # Seleccionar todos los elementos de la tabla 'Unidades'
    cursor.execute('SELECT * FROM ClasePrepa ORDER BY ClasePrepa')
    clases = cursor.fetchall()

    conn.close()

    return render_template('Clase_recetas.html', clases=clases)

@app.route('/eliminar_clase', methods=['POST'])
def eliminar_clase():
    clase_id = request.form['clase_id']
    conn = sqlite3.connect('GourmetCS50.db')
    cursor = conn.cursor()

    if request.method == 'POST':
        # Eliminar la clase de la base de datos
        cursor.execute('DELETE FROM ClasePrepa WHERE CodClasePrepa = ?', (clase_id,))
        conn.commit()

        conn.close()
        return redirect(url_for('mostrar_clases'))

    # Obtener la información de la unidad antes de eliminarla
    cursor.execute('SELECT * FROM ClasePrepa WHERE CodClasePrepa = ?', (clase_id,))
    clase = cursor.fetchone()

    conn.close()

    return render_template('Clase_recetas.html', clase=clase)

@app.route('/validar_edicion_clase', methods=['POST'])
def validar_edicion_clase():
    # Obtener los datos del formulario de edición
    clase_id = request.form.get('clase_id')
    clase_ingresada = request.form.get('claseNueva')

    # Conexión a la base de datos
    conn = sqlite3.connect('GourmetCS50.db')
    cursor = conn.cursor()

    # Verificar si la unidad ya existe en la tabla 'Unidades'
    cursor.execute('SELECT * FROM ClasePrepa WHERE CodClasePrepa = ?', (clase_ingresada,))
    existing_clase = cursor.fetchone()

    mensaje = None

    if existing_clase:
        mensaje = "La clase ya existe."
    else:
        # La nueva clase no existe, proceder con la edición
        cursor.execute('UPDATE ClasePrepa SET ClasePrepa = ? WHERE CodClasePrepa = ?', (clase_ingresada, clase_id))
        conn.commit()

    # Obtener la lista actualizada de unidades
    cursor.execute('SELECT * FROM ClasePrepa ORDER BY ClasePrepa')
    clases = cursor.fetchall()

    conn.close()

    return render_template('Clase_recetas.html', clases=clases, mensaje=mensaje)

@app.route('/editar_clase', methods=['POST'])
def editar_clase():
    # Obtener el ID de la clase a editar desde el formulario
    clase_id = request.form.get('editar_clase_id')

    # Conectar a la base de datos SQLite
    conn = sqlite3.connect('GourmetCS50.db')
    cursor = conn.cursor()

    # Obtener los detalles de la clase a editar
    cursor.execute('SELECT * FROM ClasePrepa WHERE CodClasePrepa = ?', (clase_id,))
    clase = cursor.fetchone()

    # Cerrar la conexión a la base de datos
    conn.close()

    # Renderizar el formulario de edición con los detalles de la unidad
    return render_template('Clase_recetas.html', clase=clase)

@app.route('/eliminar_receta', methods=['POST'])
def eliminar_receta():
    receta_nombre = request.form['receta_nombre']
    conn = sqlite3.connect('GourmetCS50.db')
    cursor = conn.cursor()

    if request.method == 'POST':
        cursor.execute('DELETE FROM Prepa WHERE CodPrepa = ?', (receta_nombre,))
        conn.commit()

        conn.close()
        return redirect(url_for('mostrar_receta'))

    cursor.execute('SELECT * FROM Prepa WHERE CodPrepa = ?', (receta_nombre,))
    receta = cursor.fetchone()

    conn.close()

    return render_template('Recetas.html', receta=receta)

@app.route('/mostrar_recetas')
def mostrar_recetas():
    # Conexión a la base de datos
    conn = sqlite3.connect('GourmetCS50.db')
    cursor = conn.cursor()

    cursor.execute('SELECT c.CodClasePrepa, c.ClasePrepa, p.NombrePrepa FROM ClasePrepa c JOIN Prepa p ON c.CodClasePrepa = p.CodClasePrepa ORDER BY c.ClasePrepa, p.NombrePrepa;')
    recetas_lista = cursor.fetchall() 

    conn.close()

    return render_template('Recetas.html', recetas=recetas_lista) 

@app.route('/reporte_recetas')
def reporte_recetas():
    # Conexión a la base de datos
    conn = sqlite3.connect('GourmetCS50.db')
    cursor = conn.cursor()

    cursor.execute('SELECT c.ClasePrepa, p.NombrePrepa, p.Receta FROM ClasePrepa c JOIN Prepa p ON c.CodClasePrepa = p.CodClasePrepa ORDER BY c.ClasePrepa, p.NombrePrepa;')
    recetas = cursor.fetchall()

    cursor.execute('SELECT * FROM ClasePrepa ORDER BY ClasePrepa')
    clases = cursor.fetchall()

    conn.close()

    return render_template('Reporte_Recetas.html', recetas=recetas, clases=clases)

@app.route('/recetas_alta', methods=['GET', 'POST'])
def recetas_alta():
    # Conexión a la base de datos
    conn = sqlite3.connect('GourmetCS50.db')
    cursor = conn.cursor()

    # Seleccionar todos los elementos de la tabla 'ClasePrepa'
    cursor.execute('SELECT * FROM ClasePrepa ORDER BY ClasePrepa')
    clases = cursor.fetchall()

    conn.close()

    return render_template('Recetas_alta.html', clases=clases)
 
@app.route('/validar_receta', methods=['POST'])
def validar_receta():
    nombre_receta = request.form['nombre_receta']
    claseComboBox = request.form['claseComboBox']
    porciones = request.form['porciones']
    receta = request.form['receta']

    # Asignar un valor predeterminado a filepath
    filepath = None

    # Verificar si se proporcionó una imagen
    if 'foto' in request.files:
        foto = request.files['foto']
        # Verificar si el nombre del archivo es válido y tiene una extensión permitida
        if foto and allowed_file(foto.filename):
            # Guardar la imagen en el directorio UPLOAD_FOLDER
            filename = secure_filename(foto.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            foto.save(filepath)
        else:
            # Si la imagen no es válida, asignar None o un valor predeterminado a 'foto'
            foto = None
    else:
        # Si no se proporcionó una imagen, asignar None o un valor predeterminado a 'foto'
        foto = None

    # Conexión a la base de datos
    conn = sqlite3.connect('GourmetCS50.db')
    cursor = conn.cursor()

    # Verificar si la receta ya existe en la tabla 'Prepa'
    cursor.execute('SELECT * FROM Prepa WHERE NombrePrepa = ?', (nombre_receta,))
    existing_receta = cursor.fetchone()

    mensaje = None

    if existing_receta:
        mensaje = "La receta ya existe."
    else:
        # Obtener el CodClasePrepa correspondiente al nombre de la clase
        cursor.execute('SELECT CodClasePrepa FROM ClasePrepa WHERE ClasePrepa = ?', (claseComboBox,))
        cod_clase_prepa = cursor.fetchone()[0]

        # Insertar la nueva receta en la tabla 'Prepa'
        cursor.execute('INSERT INTO Prepa (CodClasePrepa, NombrePrepa, Receta, Foto, Porciones) VALUES (?, ?, ?, ?, ?)',
                       (cod_clase_prepa, nombre_receta, receta, filepath, porciones))
        conn.commit()
        mensaje = "La receta ha sido incorporada con éxito."

    # Seleccionar todos los elementos de la tabla 'Prepa' después de la operación
    cursor.execute('SELECT * FROM Prepa ORDER BY NombrePrepa')
    recetas = cursor.fetchall()

    # Seleccionar todos los elementos de la tabla 'ClasePrepa'
    cursor.execute('SELECT * FROM ClasePrepa ORDER BY ClasePrepa')
    clases = cursor.fetchall()

    conn.close()

    return render_template('Recetas_alta.html', recetas=recetas, clases=clases, mensaje=mensaje)

@app.route('/recetamodifi')
def recetamodifi():

    conn = sqlite3.connect('GourmetCS50.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM Prepa ORDER BY NombrePrepa')
    recetas = cursor.fetchall()

    cursor.execute('SELECT * FROM ClasePrepa ORDER BY ClasePrepa')
    clases = cursor.fetchall()

    return render_template('Recetasmodifi.html', recetas=recetas, clases=clases)

@app.route('/recetamodifi_actualizar', methods=['POST'])
def recetamodifi_actualizar():

    clase_id = request.form.get('clase_id')
    clase_ingresada = request.form.get('claseNueva')

    # Conexión a la base de datos
    conn = sqlite3.connect('GourmetCS50.db')
    cursor = conn.cursor()

    # Verificar si la unidad ya existe en la tabla 'Unidades'
    cursor.execute('SELECT * FROM ClasePrepa WHERE CodClasePrepa = ?', (clase_ingresada,))
    existing_clase = cursor.fetchone()

    mensaje = None

    if existing_clase:
        mensaje = "La clase ya existe."
    else:
        # La nueva clase no existe, proceder con la edición
        cursor.execute('UPDATE ClasePrepa SET ClasePrepa = ? WHERE CodClasePrepa = ?', (clase_ingresada, clase_id))
        conn.commit()

    # Obtener la lista actualizada de unidades
    cursor.execute('SELECT * FROM ClasePrepa ORDER BY ClasePrepa')
    clases = cursor.fetchall()

    conn.close()

    return render_template('Recetasmodifi.html', clases=clases, mensaje=mensaje)


@app.route('/get_datos_by_receta', methods=['POST'])
def get_datos_by_receta():
    receta_id = request.form.get('recetaComboBox')

    # Conexión a la base de datos
    conn = sqlite3.connect('GourmetCS50.db')
    cursor = conn.cursor()

    # Obtener todos los datos del ingrediente seleccionado
    cursor.execute('SELECT * FROM Prepa WHERE CodPrepa = ?', (receta_id,))
    prepa = cursor.fetchone()

    conn.close()

    # Crear un diccionario con los datos del ingrediente
    datos_receta = {
        'claseprepa': prepa[0],
        'porciones': prepa[5],
        'receta': prepa[3],
        'foto': prepa[4],
    }

    return jsonify(datos_receta)

@app.route('/propiedades_recetas')
def propiedades_recetas():
    # Conexión a la base de datos
    conn = sqlite3.connect('GourmetCS50.db')
    cursor = conn.cursor()

    # Seleccionar todos los elementos de la tabla 'Ingredientes'
    cursor.execute('SELECT cp.ClasePrepa AS Clase, p.NombrePrepa AS Receta, SUM(i.Costo * ix.CAIngre / p.Porciones) AS CostoTotal, SUM(i.GrasasSat * ix.CAIngre / p.Porciones) AS GrasasSatTotal, SUM(i.GrasasNosat * ix.CAIngre / p.Porciones) AS GrasasNosatTotal, SUM(i.HC * ix.CAIngre / p.Porciones) AS HCTotal, SUM(i.Azucares * ix.CAIngre / p.Porciones) AS AzucaresTotal, SUM(i.Proteinas * ix.CAIngre / p.Porciones) AS ProteinasTotal, SUM(i.Sal * ix.CAIngre / p.Porciones) AS SodioTotal, SUM(i.Calcio * ix.CAIngre / p.Porciones) AS CalcioTotal, SUM(i.Colesterol * ix.CAIngre / p.Porciones) AS ColesterolTotal, SUM(i.Omega3 * ix.CAIngre / p.Porciones) AS Omega3Total, SUM(i.kCal * ix.CAIngre / p.Porciones) AS kCalTotal FROM Prepa p JOIN ClasePrepa cp ON p.CodClasePrepa = cp.CodClasePrepa JOIN IXPre ix ON p.CodPrepa = ix.CodPrepa JOIN Ingredientes i ON ix.CodIngre = i.CodIngre JOIN Unidades u ON i.CodUni = u.CodUni ORDER BY cp.ClasePrepa, p.NombrePrepa;')
    prop_recetas = cursor.fetchall() 

    conn.close()

    return render_template('Propiedades_recetas.html', recetas=prop_recetas) 

@app.route('/ingreXreceta')
def ingreXreceta():
    # Conexión a la base de datos
    conn = sqlite3.connect('GourmetCS50.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM Prepa ORDER BY NombrePrepa;')
    recetas = cursor.fetchall() 

    cursor.execute('SELECT * FROM Ingredientes ORDER BY NombreIngre;')
    ingredientes = cursor.fetchall() 

    conn.close()

    return render_template('IngredientesXReceta.html', recetas=recetas, ingredientes=ingredientes) 


@app.route('/IXPalta', methods=['POST'])
def IXPalta():
    receta = request.form['recetaComboBox']
    ingre = request.form['ingreComboBox']
    caporte = request.form['caporte']

    conn = sqlite3.connect('GourmetCS50.db')
    cursor = conn.cursor()

    try:
        # Obtener el ID de receta
        cursor.execute('SELECT CodPrepa FROM Prepa WHERE NombrePrepa = ?', (receta,))
        receta_result = cursor.fetchone()
        receta_id = receta_result[0] if receta_result else None

        # Obtener el ID de ingrediente
        cursor.execute('SELECT CodIngre FROM Ingredientes WHERE NombreIngre = ?', (ingre,))
        ingre_result = cursor.fetchone()
        ingre_id = ingre_result[0] if ingre_result else None

        print(f"Receta ID: {receta_id}, Ingrediente ID: {ingre_id}")

        if receta_id is None or ingre_id is None:
            mensaje = "Receta o ingrediente no encontrado en la base de datos."
        else:
            # Verificar si ya existe el aporte
            cursor.execute('SELECT * FROM IXPre WHERE CodPrepa = ? AND CodIngre = ?', (receta_id, ingre_id))
            existing_aporte = cursor.fetchone()

            if existing_aporte:
                mensaje = "El aporte ya existe."
            else:
                # Insertar el nuevo aporte
                cursor.execute('INSERT INTO IXPre (CodPrepa, CodIngre, CAIngre) VALUES (?, ?, ?)', (receta_id, ingre_id, caporte))
                conn.commit()
                mensaje = "El aporte ha sido incorporado con éxito."
                print("Aporte insertado con éxito.")
    except Exception as e:
        mensaje = f"Error: {str(e)}"
    
    cursor.execute('SELECT * FROM Prepa ORDER BY NombrePrepa;')
    recetas = cursor.fetchall() 

    cursor.execute('SELECT * FROM Ingredientes ORDER BY NombreIngre;')
    ingredientes = cursor.fetchall() 

    conn.close()

    return render_template('IngredientesXReceta.html', mensaje=mensaje, ingredientes=ingredientes, recetas=recetas)

@app.route('/modifi_ingreXreceta')
def modifi_ingreXreceta():
    # Conexión a la base de datos
    conn = sqlite3.connect('GourmetCS50.db')
    cursor = conn.cursor()

    cursor.execute('SELECT c.CodClasePrepa, c.ClasePrepa, p.CodPrepa, p.NombrePrepa FROM ClasePrepa c JOIN Prepa p ON c.CodClasePrepa = p.CodClasePrepa ORDER BY c.ClasePrepa, p.NombrePrepa;')
    recetas = cursor.fetchall() 

    cursor.execute('SELECT CodIngre, NombreIngre FROM Ingredientes ORDER BY NombreIngre;')
    ingredientes = cursor.fetchall() 

    conn.close()

    return render_template('IngredientesXReceta.html', recetas=recetas, ingredientes=ingredientes) 

@app.route('/receta_selec', methods=['GET', 'POST'])
def receta_selec():
    # Conexión a la base de datos
    conn = sqlite3.connect('GourmetCS50.db')
    cursor = conn.cursor()

    if request.method == 'POST':
        receta_id = request.form['recetaComboBox']

        cursor.execute('SELECT * FROM Prepa WHERE NombrePrepa = ?', (receta_id,))
        receta_data = cursor.fetchone()

        conn.close()
        return render_template('Receta_cons.html', receta=receta_data)

    cursor.execute('SELECT * FROM Prepa ORDER BY NombrePrepa;')
    recetas = cursor.fetchall()

    conn.close()
    return render_template('Receta_selec.html', recetas=recetas)

@app.route('/receta_cons')
def receta_cons():
    if request.method == 'POST':
        receta_id = request.form['recetaComboBox']
    else:
        receta_id = request.args.get('receta')

    # Conexión a la base de datos
    conn = sqlite3.connect('GourmetCS50.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM Prepa WHERE NombrePrepa = ?', (receta_id,))
    receta_data = cursor.fetchone()

    conn.close()
    return render_template('Receta_cons.html', receta=receta_data)


if __name__ == '__main__':
    app.run(debug=True)
