from flask import Flask, request, jsonify
import mysql.connector
from mysql.connector import Error
from flask_cors import CORS  # Habilita CORS si es necesario

app = Flask(__name__)
CORS(app)  # Esto habilita CORS para todas las rutas

# Configuración de la base de datos MySQL
def get_db_connection():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",  # Cambia esto con tu usuario de MySQL
            password="legendary123",  # Cambia esto con tu contraseña de MySQL
            database="farm_project"  # Asegúrate de que la base de datos esté creada
        )
    except Error as e:
        print(f"Error de conexión a la base de datos: {e}")
        return None

# Ruta para verificar si la API está funcionando
@app.route('/')
def home():
    return '¡API de inicio de sesión en funcionamiento!'

# Ruta para el registro de nuevos usuarios
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()  # Recibe los datos del frontend (JSON)
    
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    
    if not username or not email or not password:
        return jsonify({"error": "Todos los campos son obligatorios"}), 400
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Inserta el nuevo usuario en la base de datos
        cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
                       (username, email, password))
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({"message": "Usuario registrado exitosamente"}), 201
    
    except Error as e:
        return jsonify({"error": str(e)}), 500

# Ruta para el inicio de sesión (verificación de usuario)
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()  # Recibe los datos del frontend (JSON)
    
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({"error": "El nombre de usuario y la contraseña son obligatorios"}), 400
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        user = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        if user:
            return jsonify({"message": "Inicio de sesión exitoso"})
        else:
            return jsonify({"message": "Usuario o contraseña incorrectos"}), 401
    
    except Error as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
