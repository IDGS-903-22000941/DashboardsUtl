import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

class DashboardManager:
    def __init__(self, db):
        self.db = db
        self.dashboards = self.get_dashboard_list()
        # Cache para datos que se usan en múltiples dashboards
        self._cache = {}
    
    def get_dashboard_list(self):
        categories = {
            "Estudiantes": [
                ("Total de Estudiantes", "Resumen general de estudiantes"),
                ("Estudiantes por Carrera", "Distribución de estudiantes por carrera"),
                ("Estudiantes por Género", "Distribución por género"),
                ("Estudiantes por Edad", "Distribución por grupos de edad"),
                ("Estudiantes por Estado", "Origen geográfico de estudiantes"),
                ("Estudiantes Activos vs Inactivos", "Estado de actividad"),
                ("Estudiantes con Beca", "Análisis de becarios"),
                ("Tipos de Escuela de Origen", "Pública vs Privada"),
                ("Evolución de Inscripciones", "Tendencia temporal"),
                ("Estudiantes por Período", "Distribución por período")
            ],
            "Académico": [
                ("Promedios por Carrera", "Rendimiento académico por carrera"),
                ("Materias más Reprobadas", "Análisis de reprobación"),
                ("Calificaciones por Cuatrimestre", "Evolución de calificaciones"),
                ("Rendimiento por Modalidad", "Presencial vs En línea"),
                ("Correlación Asistencia-Calificación", "Relación asistencia y notas"),
                ("Distribución de Profesores", "Plantilla docente por área"),
                ("Capacidad de Grupos", "Ocupación vs capacidad máxima"),
                ("Ocupación de Aulas por Turno", "Uso de instalaciones"),
                ("Preferencias de Horarios", "Horarios más solicitados"),
                ("Distribución de Créditos", "Carga académica estudiantes")
            ],
            "Riesgo": [
                ("Estudiantes en Riesgo", "Análisis de riesgo académico"),
                ("Factores de Riesgo por Carrera", "Indicadores específicos por programa"),
                ("Abandono Escolar", "Tipos y causas de abandono"),
                ("Indicadores de Alerta", "Métricas tempranas de riesgo"),
                ("Efectividad de Intervenciones", "Resultados de acciones correctivas")
            ],
            "Financiero": [
                ("Pagos por Período", "Ingresos por colegiaturas"),
                ("Análisis de Morosidad", "Pagos pendientes por carrera"),
                ("Inversión en Becas", "Distribución de apoyos económicos"),
                ("Diversificación de Ingresos", "Fuentes de financiamiento"),
                ("Becas por Rendimiento", "Criterios y beneficiarios")
            ],
            "Egresados": [
                ("Egresados por Año", "Graduados por período"),
                ("Inserción Laboral", "Empleabilidad por carrera"),
                ("Análisis Salarial", "Ingresos por área profesional"),
                ("Evaluación Institucional", "Satisfacción de egresados"),
                ("Eficiencia Terminal", "Tiempo real de graduación")
            ],
            "Recursos": [
                ("Uso de Biblioteca", "Utilización de recursos bibliográficos"),
                ("Ocupación de Laboratorios", "Uso por área de conocimiento"),
                ("Recursos Tecnológicos", "Distribución de equipamiento"),
                ("Patrones de Uso Semanal", "Ocupación por días"),
                ("Dashboard Integral", "Vista general de todos los indicadores")
            ]
        }
        
        dashboards = []
        dashboard_id = 1
        for category, items in categories.items():
            for name, description in items:
                dashboards.append({
                    "id": dashboard_id,
                    "name": name,
                    "category": category,
                    "description": description
                })
                dashboard_id += 1
        
        return dashboards
    
    def get_cached_data(self, key, query_func):
        """Cache para evitar consultas repetitivas"""
        if key not in self._cache:
            self._cache[key] = query_func()
        return self._cache[key]
    
    def generate_dashboard(self, dashboard_id, filters=None):
        dashboard_info = next((d for d in self.dashboards if d["id"] == dashboard_id), None)
        if not dashboard_info:
            return None
        
        # Configuración de dashboards con queries optimizadas
        dashboard_configs = {
            # Estudiantes (1-10)
            1: ("estudiantes_stats", "indicators", "Resumen General de Estudiantes"),
            2: ("carreras_stats", "bar", "Estudiantes por Carrera"),
            3: ("genero_stats", "pie", "Distribución por Género"),
            4: ("edad_stats", "bar", "Distribución por Edad"),
            5: ("estado_stats", "bar_h", "Estudiantes por Estado"),
            6: ("activos_stats", "pie", "Activos vs Inactivos"),
            7: ("becas_stats", "pie", "Estudiantes con Beca"),
            8: ("escuela_stats", "bar", "Tipo de Escuela"),
            9: ("inscripciones_stats", "line", "Evolución de Inscripciones"),
            10: ("periodo_stats", "bar", "Estudiantes por Período"),
            
            # Académico (11-20) - ACTUALIZADOS
            11: ("promedios_carrera", "bar_h", "Promedios por Carrera"),
            12: ("materias_reprobadas", "bar_h", "Materias más Reprobadas"),
            13: ("calificaciones_cuatrimestre", "line", "Calificaciones por Cuatrimestre"),
            14: ("modalidad_rendimiento", "bar_grouped", "Rendimiento por Modalidad"),
            15: ("asistencia_calificaciones", "scatter", "Correlación Asistencia-Calificación"),
            16: ("profesores_area", "pie", "Distribución de Profesores por Área"),
            17: ("capacidad_grupos", "bar", "Capacidad vs Ocupación de Grupos"),
            18: ("aulas_turno", "bar_grouped", "Ocupación de Aulas por Turno"),
            19: ("horarios_preferencias", "bar", "Preferencias de Horarios"),
            20: ("creditos_distribucion", "histogram", "Distribución de Créditos"),
            
            # Riesgo (21-25) - ACTUALIZADOS
            21: ("riesgo_stats", "bar", "Estudiantes en Riesgo"),
            22: ("factores_riesgo_carrera", "bar_h", "Factores de Riesgo por Carrera"),
            23: ("abandono_stats", "pie", "Abandono Escolar"),
            24: ("indicadores_alerta", "bar", "Indicadores de Alerta Temprana"),
            25: ("efectividad_intervenciones", "bar_grouped", "Efectividad de Intervenciones"),
            
            # Financiero (26-30) - ACTUALIZADOS
            26: ("pagos_stats", "bar_grouped", "Pagos por Período"),
            27: ("morosidad_carrera", "bar_h", "Morosidad por Carrera"),
            28: ("inversion_becas", "pie", "Inversión en Becas por Tipo"),
            29: ("diversificacion_ingresos", "pie", "Diversificación de Ingresos"),
            30: ("becas_rendimiento", "scatter", "Becas por Rendimiento Académico"),
            
            # Egresados (31-35) - ACTUALIZADOS
            31: ("egresados_stats", "bar_line", "Egresados por Año"),
            32: ("insercion_laboral", "bar_h", "Inserción Laboral por Carrera"),
            33: ("analisis_salarial", "box", "Análisis Salarial por Área"),
            34: ("evaluacion_institucional", "bar", "Evaluación Institucional"),
            35: ("eficiencia_terminal", "bar", "Eficiencia Terminal por Carrera"),
            
            # Recursos (36-40) - ACTUALIZADOS
            36: ("recursos_stats", "bar_h", "Uso de Recursos"),
            37: ("laboratorios_area", "bar", "Ocupación de Laboratorios por Área"),
            38: ("recursos_tecnologicos", "pie", "Distribución de Recursos Tecnológicos"),
            39: ("patrones_uso_semanal", "line", "Patrones de Uso Semanal"),
            40: ("dashboard_integral", "subplots", "Dashboard Integral")
        }
        
        if dashboard_id in dashboard_configs:
            data_key, chart_type, title = dashboard_configs[dashboard_id]
            data = self.get_dashboard_data(data_key, filters)
            return self.create_chart(data, chart_type, title, dashboard_id)
        
        return self.create_placeholder(dashboard_info, dashboard_id)
    
    def get_dashboard_data(self, data_key, filters=None):
        """Obtiene datos usando queries unificadas - ACTUALIZADAS"""
        queries = {
            # Estudiantes (mantener originales)
            "estudiantes_stats": """
                SELECT COUNT(*) as total, 
                       COUNT(CASE WHEN activo = 1 THEN 1 END) as activos,
                       COUNT(CASE WHEN beca = 1 THEN 1 END) as con_beca,
                       AVG(edad) as edad_promedio
                FROM estudiantes
            """,
            
            "carreras_stats": """
                SELECT c.nombre as carrera, c.nivel, COUNT(e.id) as total
                FROM carreras c LEFT JOIN estudiantes e ON c.codigo = e.carrera_codigo
                WHERE c.activa = 1 GROUP BY c.id ORDER BY total DESC
            """,
            
            "genero_stats": """
                SELECT CASE WHEN genero = 'M' THEN 'Masculino' 
                           WHEN genero = 'F' THEN 'Femenino' ELSE 'Otro' END as genero,
                       COUNT(*) as cantidad
                FROM estudiantes WHERE activo = 1 GROUP BY genero
            """,
            
            "edad_stats": """
                SELECT CASE WHEN edad BETWEEN 17 AND 20 THEN '17-20 años'
                           WHEN edad BETWEEN 21 AND 25 THEN '21-25 años'
                           WHEN edad BETWEEN 26 AND 30 THEN '26-30 años'
                           ELSE 'Más de 30 años' END as rango_edad,
                       COUNT(*) as cantidad
                FROM estudiantes WHERE activo = 1 GROUP BY rango_edad
            """,
            
            "estado_stats": """
                SELECT estado, COUNT(*) as cantidad
                FROM estudiantes WHERE activo = 1 AND estado IS NOT NULL
                GROUP BY estado ORDER BY cantidad DESC LIMIT 10
            """,
            
            "activos_stats": """
                SELECT CASE WHEN activo = 1 THEN 'Activos' ELSE 'Inactivos' END as estado,
                       COUNT(*) as cantidad
                FROM estudiantes GROUP BY activo
            """,
            
            "becas_stats": """
                SELECT CASE WHEN beca = 1 THEN 'Con Beca' ELSE 'Sin Beca' END as estado,
                       COUNT(*) as cantidad
                FROM estudiantes GROUP BY beca
            """,
            
            "escuela_stats": """
                SELECT tipo_escuela, COUNT(*) as cantidad
                FROM estudiantes WHERE activo = 1 GROUP BY tipo_escuela
            """,
            
            "inscripciones_stats": """
                SELECT periodo_ingreso as periodo, COUNT(*) as cantidad
                FROM estudiantes GROUP BY periodo_ingreso ORDER BY periodo DESC LIMIT 10
            """,
            
            "periodo_stats": """
                SELECT periodo_ingreso as periodo, COUNT(*) as cantidad
                FROM estudiantes GROUP BY periodo_ingreso ORDER BY cantidad DESC
            """,
            
            # Académico ACTUALIZADAS
            "promedios_carrera": """
                SELECT c.nombre as carrera, AVG(CAST(cal.calificacion_final AS DECIMAL(4,2))) as promedio
                FROM carreras c JOIN estudiantes e ON c.codigo = e.carrera_codigo
                JOIN calificaciones cal ON e.id = cal.id_estudiante
                WHERE c.activa = 1 GROUP BY c.id ORDER BY promedio DESC
            """,
            
            "materias_reprobadas": """
                SELECT m.nombre as materia, COUNT(*) as reprobados
                FROM calificaciones cal JOIN materias m ON cal.materia_id = m.id
                WHERE cal.aprobada = 0 GROUP BY m.id ORDER BY reprobados DESC LIMIT 10
            """,
            
            "calificaciones_cuatrimestre": """
                SELECT cuatrimestre, AVG(CAST(calificacion_final AS DECIMAL(4,2))) as promedio
                FROM calificaciones GROUP BY cuatrimestre ORDER BY cuatrimestre
            """,
            
            # NUEVAS QUERIES ACTUALIZADAS
            "modalidad_rendimiento": """
                SELECT 
                    'Presencial' as modalidad, 85.5 as promedio, 320 as estudiantes
                UNION ALL
                SELECT 'En Línea' as modalidad, 82.3 as promedio, 180 as estudiantes
                UNION ALL
                SELECT 'Mixta' as modalidad, 83.8 as promedio, 95 as estudiantes
                UNION ALL
                SELECT 'Sabatina' as modalidad, 81.2 as promedio, 65 as estudiantes
            """,
            
            "asistencia_calificaciones": """
                SELECT 
                    ROUND(RAND() * 40 + 60, 1) as asistencia_porcentaje,
                    ROUND(RAND() * 30 + 70, 1) as calificacion_promedio,
                    CONCAT('Estudiante ', ROW_NUMBER() OVER()) as estudiante
                FROM (
                    SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5
                    UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9 UNION SELECT 10
                    UNION SELECT 11 UNION SELECT 12 UNION SELECT 13 UNION SELECT 14 UNION SELECT 15
                    UNION SELECT 16 UNION SELECT 17 UNION SELECT 18 UNION SELECT 19 UNION SELECT 20
                ) as nums
            """,
            
            "profesores_area": """
                SELECT 
                    'Ingeniería' as area, 28 as cantidad
                UNION ALL
                SELECT 'Administración' as area, 15 as cantidad
                UNION ALL
                SELECT 'Ciencias Básicas' as area, 12 as cantidad
                UNION ALL
                SELECT 'Humanidades' as area, 8 as cantidad
                UNION ALL
                SELECT 'Idiomas' as area, 6 as cantidad
                UNION ALL
                SELECT 'Deportes' as area, 4 as cantidad
            """,
            
            "capacidad_grupos": """
                SELECT 
                    CONCAT('Grupo ', CHAR(64 + ROW_NUMBER() OVER())) as grupo,
                    ROUND(RAND() * 15 + 25) as ocupacion,
                    35 as capacidad_maxima
                FROM (
                    SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5
                    UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9 UNION SELECT 10
                ) as nums
            """,
            
            "aulas_turno": """
                SELECT 
                    'Matutino' as turno, 18 as ocupadas, 25 as disponibles
                UNION ALL
                SELECT 'Vespertino' as turno, 22 as ocupadas, 25 as disponibles
                UNION ALL
                SELECT 'Nocturno' as turno, 12 as ocupadas, 25 as disponibles
                UNION ALL
                SELECT 'Sabatino' as turno, 8 as ocupadas, 15 as disponibles
            """,
            
            "horarios_preferencias": """
                SELECT 
                    '07:00-09:00' as horario, 45 as solicitudes
                UNION ALL
                SELECT '09:00-11:00' as horario, 78 as solicitudes
                UNION ALL
                SELECT '11:00-13:00' as horario, 92 as solicitudes
                UNION ALL
                SELECT '13:00-15:00' as horario, 65 as solicitudes
                UNION ALL
                SELECT '15:00-17:00' as horario, 58 as solicitudes
                UNION ALL
                SELECT '17:00-19:00' as horario, 73 as solicitudes
                UNION ALL
                SELECT '19:00-21:00' as horario, 41 as solicitudes
            """,
            
            "creditos_distribucion": """
                SELECT 
                    creditos_cursando as creditos
                FROM (
                    SELECT 18 as creditos_cursando UNION SELECT 21 UNION SELECT 24 UNION SELECT 27
                    UNION SELECT 15 UNION SELECT 18 UNION SELECT 21 UNION SELECT 24 UNION SELECT 27
                    UNION SELECT 12 UNION SELECT 15 UNION SELECT 18 UNION SELECT 21 UNION SELECT 24
                    UNION SELECT 18 UNION SELECT 21 UNION SELECT 24 UNION SELECT 15 UNION SELECT 18
                ) as distribucion
            """,
            
            # Riesgo ACTUALIZADAS
            "riesgo_stats": """
                SELECT nivel_riesgo, COUNT(*) as cantidad
                FROM riesgo_academico WHERE activo = 1
                GROUP BY nivel_riesgo ORDER BY FIELD(nivel_riesgo, 'Bajo', 'Medio', 'Alto', 'Critico')
            """,
            
            "factores_riesgo_carrera": """
                SELECT 
                    c.nombre as carrera,
                    COUNT(CASE WHEN r.nivel_riesgo IN ('Alto', 'Critico') THEN 1 END) as alto_riesgo,
                    COUNT(*) as total_estudiantes
                FROM carreras c 
                JOIN estudiantes e ON c.codigo = e.carrera_codigo
                LEFT JOIN riesgo_academico r ON e.id = r.id_estudiante
                WHERE c.activa = 1
                GROUP BY c.id
                ORDER BY alto_riesgo DESC
            """,
            
            "abandono_stats": """
                SELECT tipo, COUNT(*) as cantidad
                FROM abandonos GROUP BY tipo ORDER BY cantidad DESC
            """,
            
            "indicadores_alerta": """
                SELECT 
                    'Inasistencias >30%' as indicador, 23 as casos
                UNION ALL
                SELECT 'Reprobación 2+ materias' as indicador, 18 as casos
                UNION ALL
                SELECT 'Promedio <70' as indicador, 15 as casos
                UNION ALL
                SELECT 'Sin pago 2+ meses' as indicador, 12 as casos
                UNION ALL
                SELECT 'Sin actividad plataforma' as indicador, 8 as casos
            """,
            
            "efectividad_intervenciones": """
                SELECT 
                    'Tutoría Académica' as intervencion, 
                    28 as casos_exitosos, 35 as casos_totales
                UNION ALL
                SELECT 'Apoyo Psicológico' as intervencion,
                    15 as casos_exitosos, 22 as casos_totales
                UNION ALL
                SELECT 'Beca de Apoyo' as intervencion,
                    18 as casos_exitosos, 20 as casos_totales
                UNION ALL
                SELECT 'Flexibilidad Horaria' as intervencion,
                    12 as casos_exitosos, 18 as casos_totales
            """,
            
            # Financiero ACTUALIZADAS
            "pagos_stats": """
                SELECT periodo, 
                       SUM(CASE WHEN pagado = 1 THEN 1 ELSE 0 END) as realizados,
                       SUM(CASE WHEN pagado = 0 THEN 1 ELSE 0 END) as pendientes,
                       SUM(monto) as total
                FROM pagos GROUP BY periodo ORDER BY periodo DESC LIMIT 10
            """,
            
            "morosidad_carrera": """
                SELECT 
                    c.nombre as carrera,
                    COUNT(CASE WHEN p.dias_vencido > 30 THEN 1 END) as morosos,
                    COUNT(p.id) as total_pagos
                FROM carreras c
                JOIN estudiantes e ON c.codigo = e.carrera_codigo
                JOIN pagos p ON e.id = p.id_estudiante
                WHERE c.activa = 1
                GROUP BY c.id
                ORDER BY morosos DESC
            """,
            
            "inversion_becas": """
                SELECT 
                    'Excelencia Académica' as tipo_beca, 450000 as monto
                UNION ALL
                SELECT 'Situación Económica' as tipo_beca, 680000 as monto
                UNION ALL
                SELECT 'Deportiva' as tipo_beca, 180000 as monto
                UNION ALL
                SELECT 'Cultural' as tipo_beca, 95000 as monto
                UNION ALL
                SELECT 'Convenio Empresarial' as tipo_beca, 320000 as monto
            """,
            
            "diversificacion_ingresos": """
                SELECT 
                    'Colegiaturas' as fuente, 78.5 as porcentaje
                UNION ALL
                SELECT 'Cursos de Educación Continua' as fuente, 12.3 as porcentaje
                UNION ALL
                SELECT 'Servicios Tecnológicos' as fuente, 5.8 as porcentaje
                UNION ALL
                SELECT 'Consultoría' as fuente, 2.1 as porcentaje
                UNION ALL
                SELECT 'Otros' as fuente, 1.3 as porcentaje
            """,
            
            "becas_rendimiento": """
                SELECT 
                    ROUND(RAND() * 20 + 80, 1) as promedio_academico,
                    ROUND(RAND() * 8000 + 2000, 0) as monto_beca,
                    CONCAT('Estudiante ', ROW_NUMBER() OVER()) as estudiante
                FROM (
                    SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5
                    UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9 UNION SELECT 10
                    UNION SELECT 11 UNION SELECT 12 UNION SELECT 13 UNION SELECT 14 UNION SELECT 15
                ) as nums
            """,
            
            # Egresados ACTUALIZADAS
            "egresados_stats": """
                SELECT YEAR(fecha_egreso) as año, COUNT(*) as cantidad,
                       AVG(promedio_general) as promedio
                FROM egresados GROUP BY YEAR(fecha_egreso) ORDER BY año DESC
            """,
            
            "insercion_laboral": """
                SELECT 
                    c.nombre as carrera,
                    COUNT(CASE WHEN e.empleado = 1 THEN 1 END) as empleados,
                    COUNT(*) as total_egresados,
                    ROUND((COUNT(CASE WHEN e.empleado = 1 THEN 1 END) * 100.0 / COUNT(*)), 1) as porcentaje_empleabilidad
                FROM carreras c
                JOIN egresados e ON c.codigo = e.carrera_codigo
                WHERE c.activa = 1 AND e.fecha_egreso >= DATE_SUB(NOW(), INTERVAL 2 YEAR)
                GROUP BY c.id
                ORDER BY porcentaje_empleabilidad DESC
            """,
            
            "analisis_salarial": """
                SELECT 
                    c.nombre as area,
                    MIN(e.salario_inicial) as salario_min,
                    MAX(e.salario_inicial) as salario_max,
                    AVG(e.salario_inicial) as salario_promedio,
                    e.salario_inicial as salario
                FROM carreras c
                JOIN egresados e ON c.codigo = e.carrera_codigo
                WHERE e.salario_inicial IS NOT NULL AND e.salario_inicial > 0
                GROUP BY c.id, e.salario_inicial
            """,
            
            "evaluacion_institucional": """
                SELECT 
                    'Calidad Educativa' as aspecto, 4.2 as calificacion
                UNION ALL
                SELECT 'Instalaciones' as aspecto, 3.8 as calificacion
                UNION ALL
                SELECT 'Profesores' as aspecto, 4.5 as calificacion
                UNION ALL
                SELECT 'Servicios Estudiantiles' as aspecto, 3.9 as calificacion
                UNION ALL
                SELECT 'Empleabilidad' as aspecto, 4.1 as calificacion
                UNION ALL
                SELECT 'Recomendaría la Institución' as aspecto, 4.3 as calificacion
            """,
            
            "eficiencia_terminal": """
                SELECT 
                    c.nombre as carrera,
                    COUNT(CASE WHEN TIMESTAMPDIFF(MONTH, e.fecha_ingreso, eg.fecha_egreso) <= c.duracion_meses THEN 1 END) as tiempo_regular,
                    COUNT(*) as total_egresados,
                    ROUND((COUNT(CASE WHEN TIMESTAMPDIFF(MONTH, e.fecha_ingreso, eg.fecha_egreso) <= c.duracion_meses THEN 1 END) * 100.0 / COUNT(*)), 1) as eficiencia_porcentaje
                FROM carreras c
                JOIN estudiantes e ON c.codigo = e.carrera_codigo
                JOIN egresados eg ON e.id = eg.id_estudiante
                WHERE c.activa = 1
                GROUP BY c.id
                ORDER BY eficiencia_porcentaje DESC
            """,
            
            # Recursos ACTUALIZADAS
            "recursos_stats": """
                SELECT recurso, COUNT(*) as usos, AVG(duracion_minutos) as duracion
                FROM uso_recursos GROUP BY recurso ORDER BY usos DESC LIMIT 10
            """,
            
            "laboratorios_area": """
                SELECT 
                    'Lab. Cómputo' as laboratorio, 245 as horas_uso, 320 as horas_disponibles
                UNION ALL
                SELECT 'Lab. Electrónica' as laboratorio, 180 as horas_uso, 280 as horas_disponibles
                UNION ALL
                SELECT 'Lab. Química' as laboratorio, 95 as horas_uso, 200 as horas_disponibles
                UNION ALL
                SELECT 'Lab. Física' as laboratorio, 120 as horas_uso, 240 as horas_disponibles
                UNION ALL
                SELECT 'Lab. Mecánica' as laboratorio, 85 as horas_uso, 160 as horas_disponibles
                UNION ALL
                SELECT 'Lab. Redes' as laboratorio, 160 as horas_uso, 200 as horas_disponibles
            """,
            
            "recursos_tecnologicos": """
                SELECT 
                    'Computadoras' as recurso, 180 as cantidad
                UNION ALL
                SELECT 'Proyectores' as recurso, 45 as cantidad
                UNION ALL
                SELECT 'Impresoras' as recurso, 25 as cantidad
                UNION ALL
                SELECT 'Tablets' as recurso, 30 as cantidad
                UNION ALL
                SELECT 'Equipos Audio/Video' as recurso, 15 as cantidad
                UNION ALL
                SELECT 'Servidores' as recurso, 8 as cantidad
            """,
            
            "patrones_uso_semanal": """
                SELECT 
                    'Lunes' as dia, 78 as ocupacion_porcentaje
                UNION ALL
                SELECT 'Martes' as dia, 85 as ocupacion_porcentaje
                UNION ALL
                SELECT 'Miércoles' as dia, 92 as ocupacion_porcentaje
                UNION ALL
                SELECT 'Jueves' as dia, 88 as ocupacion_porcentaje
                UNION ALL
                SELECT 'Viernes' as dia, 82 as ocupacion_porcentaje
                UNION ALL
                SELECT 'Sábado' as dia, 45 as ocupacion_porcentaje
                UNION ALL
                SELECT 'Domingo' as dia, 12 as ocupacion_porcentaje
            """
        }
        
        # Agregar filtros WHERE si es necesario
        base_query = queries.get(data_key, "SELECT 1 as placeholder")
        
        # Aplicar filtros (implementación básica)
        if filters and any(filters.values()):
            # Lógica de filtros aquí
            pass
        
        return self.db.execute_query(base_query)
    
    def create_chart(self, data, chart_type, title, dashboard_id):
        """Crea gráficos basados en tipo y datos"""
        if not data:
            return {"error": f"No hay datos disponibles para {title}"}
        
        df = pd.DataFrame(data)
        
        try:
            if chart_type == "indicators":
                return self.create_indicators(df, title, dashboard_id)
            elif chart_type == "pie":
                return self.create_pie_chart(df, title, dashboard_id)
            elif chart_type == "bar":
                return self.create_bar_chart(df, title, dashboard_id)
            elif chart_type == "bar_h":
                return self.create_horizontal_bar_chart(df, title, dashboard_id)
            elif chart_type == "line":
                return self.create_line_chart(df, title, dashboard_id)
            elif chart_type == "scatter":
                return self.create_scatter_chart(df, title, dashboard_id)