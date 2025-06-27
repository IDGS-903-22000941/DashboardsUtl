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
                print(f"Query: {query}")
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
            COALESCE(AVG(edad), 0) as edad_promedio
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
    
    def get_genero_stats(self):
        query = """
        SELECT 
            CASE 
                WHEN genero = 'M' THEN 'Masculino'
                WHEN genero = 'F' THEN 'Femenino'
                ELSE 'Otro'
            END as genero,
            COUNT(*) as cantidad
        FROM estudiantes
        WHERE activo = 1 AND genero IS NOT NULL
        GROUP BY genero
        ORDER BY cantidad DESC
        """
        return self.execute_query(query)
    
    def get_promedios_carrera(self):
        query = """
        SELECT 
            c.nombre as carrera,
            COALESCE(AVG(CAST(cal.calificacion_final AS DECIMAL(4,2))), 0) as promedio
        FROM carreras c
        LEFT JOIN estudiantes e ON c.codigo = e.carrera_codigo
        LEFT JOIN calificaciones cal ON e.id = cal.id_estudiante
        WHERE c.activa = 1 AND cal.calificacion_final IS NOT NULL
        GROUP BY c.id, c.nombre
        HAVING promedio > 0
        ORDER BY promedio DESC
        """
        return self.execute_query(query)
    
    def get_abandono_stats(self):
        query = """
        SELECT 
            tipo,
            COUNT(*) as cantidad,
            COALESCE(AVG(promedio_al_abandono), 0) as promedio_abandono
        FROM abandonos
        GROUP BY tipo
        ORDER BY cantidad DESC
        """
        return self.execute_query(query)
    
    def get_riesgo_academico_stats(self):
        query = """
        SELECT 
            nivel_riesgo,
            COUNT(*) as cantidad,
            COALESCE(AVG(promedio_actual), 0) as promedio_actual
        FROM riesgo_academico
        WHERE activo = 1
        GROUP BY nivel_riesgo
        ORDER BY FIELD(nivel_riesgo, 'Bajo', 'Medio', 'Alto', 'Critico')
        """
        return self.execute_query(query)
    
    def get_estudiantes_por_edad(self):
        query = """
        SELECT 
            CASE 
                WHEN edad BETWEEN 17 AND 20 THEN '17-20 años'
                WHEN edad BETWEEN 21 AND 25 THEN '21-25 años'
                WHEN edad BETWEEN 26 AND 30 THEN '26-30 años'
                WHEN edad > 30 THEN 'Más de 30 años'
                ELSE 'Sin especificar'
            END as rango_edad,
            COUNT(*) as cantidad
        FROM estudiantes
        WHERE activo = 1 AND edad IS NOT NULL
        GROUP BY rango_edad
        ORDER BY cantidad DESC
        """
        return self.execute_query(query)
    
    def get_estudiantes_por_estado(self):
        query = """
        SELECT 
            estado,
            COUNT(*) as cantidad
        FROM estudiantes
        WHERE activo = 1 AND estado IS NOT NULL
        GROUP BY estado
        ORDER BY cantidad DESC
        LIMIT 10
        """
        return self.execute_query(query)
    
    def get_becas_stats(self):
        query = """
        SELECT 
            CASE WHEN beca = 1 THEN 'Con Beca' ELSE 'Sin Beca' END as estado_beca,
            COUNT(*) as cantidad,
            COALESCE(AVG(porcentaje_beca), 0) as promedio_porcentaje
        FROM estudiantes
        WHERE activo = 1
        GROUP BY beca
        """
        return self.execute_query(query)
    
    def get_tipo_escuela_stats(self):
        query = """
        SELECT 
            tipo_escuela,
            COUNT(*) as cantidad
        FROM estudiantes
        WHERE activo = 1 AND tipo_escuela IS NOT NULL
        GROUP BY tipo_escuela
        """
        return self.execute_query(query)
    
    def get_inscripciones_por_periodo(self):
        query = """
        SELECT 
            periodo_ingreso as periodo,
            COUNT(*) as cantidad
        FROM estudiantes
        WHERE periodo_ingreso IS NOT NULL
        GROUP BY periodo_ingreso
        ORDER BY periodo_ingreso DESC
        LIMIT 10
        """
        return self.execute_query(query)
    
    def get_materias_reprobadas(self):
        query = """
        SELECT 
            m.nombre as materia,
            COUNT(*) as reprobados
        FROM calificaciones cal
        JOIN materias m ON cal.materia_id = m.id
        WHERE cal.aprobada = 0
        GROUP BY m.id, m.nombre
        ORDER BY reprobados DESC
        LIMIT 10
        """
        return self.execute_query(query)
    
    def get_calificaciones_por_cuatrimestre(self):
        query = """
        SELECT 
            cuatrimestre,
            COALESCE(AVG(CAST(calificacion_final AS DECIMAL(4,2))), 0) as promedio
        FROM calificaciones
        WHERE calificacion_final IS NOT NULL
        GROUP BY cuatrimestre
        ORDER BY cuatrimestre
        """
        return self.execute_query(query)
    
    def get_pagos_por_periodo(self):
        query = """
        SELECT 
            periodo,
            COUNT(*) as total_pagos,
            SUM(CASE WHEN pagado = 1 THEN 1 ELSE 0 END) as pagos_realizados,
            SUM(CASE WHEN pagado = 0 THEN 1 ELSE 0 END) as pagos_pendientes,
            COALESCE(SUM(monto), 0) as monto_total
        FROM pagos
        GROUP BY periodo
        ORDER BY periodo DESC
        LIMIT 10
        """
        return self.execute_query(query)
    
    def get_egresados_por_año(self):
        query = """
        SELECT 
            YEAR(fecha_egreso) as año,
            COUNT(*) as cantidad,
            COALESCE(AVG(promedio_general), 0) as promedio_general
        FROM egresados
        WHERE fecha_egreso IS NOT NULL
        GROUP BY YEAR(fecha_egreso)
        ORDER BY año DESC
        """
        return self.execute_query(query)
    
    def get_uso_recursos(self):
        query = """
        SELECT 
            recurso,
            COUNT(*) as usos,
            COALESCE(AVG(duracion_minutos), 0) as duracion_promedio
        FROM uso_recursos
        GROUP BY recurso
        ORDER BY usos DESC
        LIMIT 10
        """
        return self.execute_query(query)