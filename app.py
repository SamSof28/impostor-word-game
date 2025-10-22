import random
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, join_room

#Banco de Palabras
PALABRAS = {
    "Comida": ["Pizza", "Taco", "Sushi", "Ensalada", "Hamburguesa", "Pasta", "Chocolate"],
    "Animales": ["Perro", "Gato", "León", "Elefante", "Jirafa", "Tigre", "Zorro"],
    "Países": ["Chile", "Perú", "México", "España", "Colombia", "Canadá", "Japón"],
    "Instrumentos": ["Guitarra", "Piano", "Batería", "Trompeta", "Violín", "Flauta", "Saxofón"],
    # Puedes añadir más temas y palabras...
}

def seleccionar_palabra_y_tema():
    """Selecciona un tema y una palabra al azar."""
    tema = random.choice(list(PALABRAS.keys()))
    palabra = random.choice(PALABRAS[tema])
    return tema, palabra

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mi_clave_secreta'
Socketio = SocketIO(app)

# ESTADO GLOBAL DEL JUEGO: Única fuente de verdad
juego = {
    'estado': 'espera',  # 'espera', 'jugando', 'votacion'
    'tema': None,
    'palabra_secreta': None,
    'impostor_sid': None, # Usamos el Session ID para la privacidad
    'jugadores': {},     # { 'sid': {'nombre': 'Juan', 'voto_a': None} }
    'votos_ronda': {},   # { 'nombre_jugador': count }
    'anfitrion_sid': None
}

@app.route('/')
def index():
    return render_template('index.html')

# -- Eventos de SocketIO --

