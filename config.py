import os

class Config:
    # Configuración de la base de datos
    DB_HOST = 'localhost'
    DB_USER = 'root'
    DB_PASSWORD = 'conejillo18'  # Cambia por tu password
    DB_NAME = 'alumnos_utl_tarea'
    
    # Configuración de Flask
    SECRET_KEY = 'tu_clave_secreta_aqui'
    DEBUG = True