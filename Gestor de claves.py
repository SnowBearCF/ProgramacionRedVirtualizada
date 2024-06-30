from flask import Flask, request, jsonify
from passlib.hash import sha256_crypt
import sqlite3

app = Flask(__name__)

# Función para conectar a la base de datos SQLite
def conectar_db():
    conn = sqlite3.connect('usuarios.db')
    return conn

# Función para crear la tabla de usuarios si no existe
def inicializar_db():
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Función para hashear la contraseña
def hash_password(password):
    hashed_password = sha256_crypt.hash(password)
    return hashed_password

# Ruta para la página de inicio del sitio web
@app.route('/')
def index():
    return "Bienvenido al sitio web de gestión de usuarios y contraseñas."

# Ruta para registrar un nuevo usuario
@app.route('/registrar', methods=['POST'])
def registrar_usuario():
    data = request.get_json()
    nombre = data.get('nombre')
    password = data.get('password')

    # Validar si nombre y contraseña están presentes
    if not nombre or not password:
        return jsonify({'message': 'Debe proporcionar nombre y contraseña'}), 400

    # Hashear la contraseña antes de almacenarla
    hashed_password = hash_password(password)

    # Conectar a la base de datos
    conn = conectar_db()
    cursor = conn.cursor()

    # Insertar usuario y contraseña hasheada en la base de datos
    cursor.execute('INSERT INTO usuarios (nombre, password) VALUES (?, ?)', (nombre, hashed_password))
    conn.commit()

    # Cerrar la conexión con la base de datos
    conn.close()

    return jsonify({'message': 'Usuario registrado correctamente'})

# Ruta para autenticar un usuario
@app.route('/login', methods=['POST'])
def validar_usuario():
    data = request.get_json()
    nombre = data.get('nombre')
    password = data.get('password')

    # Conectar a la base de datos
    conn = conectar_db()
    cursor = conn.cursor()

    # Buscar el usuario en la base de datos
    cursor.execute('SELECT * FROM usuarios WHERE nombre = ?', (nombre,))
    usuario = cursor.fetchone()

    if usuario:
        stored_password = usuario[2]  # El índice 2 corresponde al campo 'password' en la tabla
        # Verificar la contraseña hasheada
        if sha256_crypt.verify(password, stored_password):
            return jsonify({'message': 'Inicio de sesión exitoso'})
        else:
            return jsonify({'message': 'Contraseña incorrecta'}), 401
    else:
        return jsonify({'message': 'Usuario no encontrado'}), 404

    # Cerrar la conexión con la base de datos
    conn.close()

# Inicializar la base de datos al iniciar la aplicación
if __name__ == '__main__':
    inicializar_db()
    app.run(port=5800, debug=True)

