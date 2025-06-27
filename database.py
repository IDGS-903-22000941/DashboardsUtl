import mysql.connector
from config import Config
import pandas as pd

class Database:
    def __init__(self):
        self.config = {
            'host': Config.DB_HOST,
            'user': Config.DB_USER,
            'password': Config.DB_PASSWORD,
            'database': Config.DB_NAME
        }
    
    def connect(self):
        try:
            connection = mysql.connector.connect(**self.config)
            return connection
        except mysql.connector.Error as e:
            print(f"Error conectando a la base de datos: {e}")
            return None
    
    def execute_query(self, query, params=None):
        connection = self.connect()
        if connection:
            try:
                cursor = connection.cursor(dictionary=True)
                cursor.execute(query, params)
                result = cursor.fetchall()
                cursor.close()
                connection.close()
                return result
            except mysql.connector.Error as e:
                print(f"Error ejecutando query: {e}")
                return []
        return []
    
    def get_dataframe(self, query, params=None):
        connection = self.connect()
        if connection:
            try:
                df = pd.read_sql(query, connection, params=params)
                connection.close()
                return df
            except Exception as e:
                print(f"Error creando dataframe: {e}")
                return pd.DataFrame()
        return pd.DataFrame()
    
    # Métodos específicos para obtener datos
    def get_estudiantes_stats(self):
        query = """
        SELECT 
            COUNT(*) as total_estudiantes,
            COUNT(CASE WHEN activo = 1 THEN 1 END) as activos,
            COUNT(CASE WHEN beca = 1 THEN 1 END) as con_beca,
            AVG(edad) as edad_promedio
        FROM estudiantes
        """
        return self.execute_query(query)
    
    def get_carreras_stats(self):
        query = """
        SELECT 
            c.nombre as carrera,
            c.nivel,
            COUNT(e.id) as total_estudiantes
        FROM carreras c
        LEFT JOIN estudiantes e ON c.codigo = e.carrera_codigo
        WHERE c.activa = 1
        GROUP BY c.id, c.nombre, c.nivel
        ORDER BY total_estudiantes DESC
        """
        return self.execute_query(query)
    
    def get_abandono_stats(self):
        query = """
        SELECT 
            tipo,
            COUNT(*) as cantidad,
            AVG(promedio_al_abandono) as promedio_abandono
        FROM abandonos
        GROUP BY tipo
        """
        return self.execute_query(query)
    
    def get_riesgo_academico_stats(self):
        query = """
        SELECT 
            nivel_riesgo,
            COUNT(*) as cantidad,
            AVG(promedio_actual) as promedio_actual
        FROM riesgo_academico
        WHERE activo = 1
        GROUP BY nivel_riesgo
        """
        return self.execute_query(query)