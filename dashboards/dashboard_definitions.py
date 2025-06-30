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
            17: ("capacidad_grupos", "capacity", "Capacidad vs Ocupación de Grupos"),


            18: ("aulas_turno", "bar_grouped", "Ocupación de Aulas por Turno"),
            19: ("horarios_preferencias", "bar", "Preferencias de Horarios"),
            20: ("rendimiento_cuatrimestre", "bar_grouped", "Rendimiento Académico por Cuatrimestre"),
            
            # Riesgo (21-25) - ACTUALIZADOS
            21: ("riesgo_stats", "bar", "Estudiantes en Riesgo"),
            22: ("factores_riesgo_carrera", "bar_h", "Factores de Riesgo por Carrera"),
            23: ("abandono_stats", "pie", "Abandono Escolar"),
            24: ("indicadores_alerta", "bar", "Indicadores de Alerta Temprana"),
            25: ("efectividad_intervenciones", "bar_grouped", "Efectividad de Intervenciones"),
            
            # Financiero (26-30) - ACTUALIZADOS
            26: ("pagos_stats", "bar_grouped", "Pagos por Período"),
            27: ("morosidad_carrera", "morosity", "Morosidad por Carrera"),

            28: ("inversion_becas", "pie", "Inversión en Becas por Tipo"),
            29: ("diversificacion_ingresos", "pie", "Diversificación de Ingresos"),
            30: ("becas_rendimiento", "scatter", "Becas por Rendimiento Académico"),
            
            # Egresados (31-35) - ACTUALIZADOS
            31: ("egresados_stats", "bar_line", "Egresados por Año"),
            32: ("insercion_laboral", "employment", "Inserción Laboral por Carrera"),
            33: ("analisis_salarial", "salary_analysis", "Análisis Salarial por Área"),


            34: ("evaluacion_institucional", "bar", "Evaluación Institucional"),
            35: ("eficiencia_terminal", "terminal_efficiency", "Eficiencia Terminal por Carrera"),
            
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
        CONCAT(m.nombre, ' - ', g.nombre) as grupo,
        COUNT(DISTINCT e.id) as ocupacion,
        g.capacidad_maxima,
        ROUND((COUNT(DISTINCT e.id) * 100.0 / g.capacidad_maxima), 1) as porcentaje_ocupacion
    FROM grupos g
    LEFT JOIN materias m ON g.materia_id = m.id
    LEFT JOIN inscripciones i ON g.id = i.grupo_id
    LEFT JOIN estudiantes e ON i.estudiante_id = e.id AND e.activo = 1
    WHERE g.activo = 1
    GROUP BY g.id, m.nombre, g.nombre, g.capacidad_maxima
    ORDER BY porcentaje_ocupacion DESC
    LIMIT 15
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
            
            "rendimiento_cuatrimestre": """
    SELECT 
        CONCAT('Cuatrimestre ', c.cuatrimestre) as periodo,
        AVG(CAST(c.calificacion_final AS DECIMAL(4,2))) as promedio,
        COUNT(*) as total_calificaciones,
        COUNT(CASE WHEN c.aprobada = 1 THEN 1 END) as aprobadas,
        ROUND((COUNT(CASE WHEN c.aprobada = 1 THEN 1 END) * 100.0 / COUNT(*)), 1) as porcentaje_aprobacion
    FROM calificaciones c
    WHERE c.calificacion_final IS NOT NULL
    GROUP BY c.cuatrimestre
    ORDER BY c.cuatrimestre
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
        car.nombre as carrera,
        COUNT(DISTINCT CASE WHEN p.estado = 'Pendiente' AND DATEDIFF(CURDATE(), p.fecha_vencimiento) > 30 THEN e.id END) as estudiantes_morosos,
        COUNT(DISTINCT e.id) as total_estudiantes,
        ROUND((COUNT(DISTINCT CASE WHEN p.estado = 'Pendiente' AND DATEDIFF(CURDATE(), p.fecha_vencimiento) > 30 THEN e.id END) * 100.0 / COUNT(DISTINCT e.id)), 1) as porcentaje_morosidad,
        SUM(CASE WHEN p.estado = 'Pendiente' AND DATEDIFF(CURDATE(), p.fecha_vencimiento) > 30 THEN p.monto ELSE 0 END) as monto_moroso
    FROM carreras car
    JOIN estudiantes e ON car.codigo = e.carrera_codigo
    LEFT JOIN pagos p ON e.id = p.estudiante_id
    WHERE car.activa = 1 AND e.activo = 1
    GROUP BY car.id, car.nombre
    HAVING total_estudiantes > 0
    ORDER BY porcentaje_morosidad DESC
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
        COUNT(DISTINCT eg.id) as total_egresados,
        COUNT(DISTINCT CASE WHEN eg.empleado = 1 THEN eg.id END) as empleados,
        COUNT(DISTINCT CASE WHEN eg.empleado = 0 THEN eg.id END) as desempleados,
        AVG(CASE WHEN eg.salario_inicial > 0 THEN eg.salario_inicial END) as salario_promedio,
        ROUND((COUNT(DISTINCT CASE WHEN eg.empleado = 1 THEN eg.id END) * 100.0 / COUNT(DISTINCT eg.id)), 1) as porcentaje_empleabilidad
    FROM carreras c
    JOIN egresados eg ON c.codigo = eg.carrera_codigo
    WHERE c.activa = 1 AND eg.fecha_egreso >= DATE_SUB(CURDATE(), INTERVAL 3 YEAR)
    GROUP BY c.id, c.nombre
    HAVING total_egresados > 0
    ORDER BY porcentaje_empleabilidad DESC
""",
            
            "analisis_salarial": """
    SELECT 
        c.area_conocimiento as area,
        c.nombre as carrera,
        eg.salario_inicial as salario,
        CASE 
            WHEN eg.salario_inicial < 15000 THEN 'Bajo (< 15K)'
            WHEN eg.salario_inicial BETWEEN 15000 AND 25000 THEN 'Medio (15K-25K)'
            WHEN eg.salario_inicial BETWEEN 25001 AND 35000 THEN 'Alto (25K-35K)'
            ELSE 'Muy Alto (> 35K)'
        END as rango_salarial,
        eg.tiempo_empleado_meses,
        eg.satisfaccion_laboral
    FROM carreras c
    JOIN egresados eg ON c.codigo = eg.carrera_codigo
    WHERE c.activa = 1 AND eg.salario_inicial IS NOT NULL AND eg.salario_inicial > 0
    ORDER BY c.area_conocimiento, eg.salario_inicial DESC
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
        c.duracion_cuatrimestres * 4 as duracion_meses_teorica,
        COUNT(DISTINCT eg.id) as total_egresados,
        COUNT(DISTINCT CASE WHEN TIMESTAMPDIFF(MONTH, e.fecha_ingreso, eg.fecha_egreso) <= (c.duracion_cuatrimestres * 4) THEN eg.id END) as egresados_tiempo_regular,
        AVG(TIMESTAMPDIFF(MONTH, e.fecha_ingreso, eg.fecha_egreso)) as promedio_meses_reales,
        ROUND((COUNT(DISTINCT CASE WHEN TIMESTAMPDIFF(MONTH, e.fecha_ingreso, eg.fecha_egreso) <= (c.duracion_cuatrimestres * 4) THEN eg.id END) * 100.0 / COUNT(DISTINCT eg.id)), 1) as eficiencia_porcentaje
    FROM carreras c
    JOIN estudiantes e ON c.codigo = e.carrera_codigo
    JOIN egresados eg ON e.id = eg.estudiante_id
    WHERE c.activa = 1 AND eg.fecha_egreso IS NOT NULL
    GROUP BY c.id, c.nombre, c.duracion_cuatrimestres
    HAVING total_egresados > 0
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
            elif chart_type == "bar_grouped":
                return self.create_grouped_bar_chart(df, title, dashboard_id)
            elif chart_type == "histogram":
                return self.create_histogram_chart(df, title, dashboard_id)
            elif chart_type == "bar_line":
                return self.create_bar_line_chart(df, title, dashboard_id)
            elif chart_type == "box":
                return self.create_box_chart(df, title, dashboard_id)
            elif chart_type == "subplots":
                return self.create_subplots_chart(df, title, dashboard_id)
            elif chart_type == "capacity":
                return self.create_capacity_chart(df, title, dashboard_id)
            elif chart_type == "morosity":
                return self.create_morosity_chart(df, title, dashboard_id)  
            elif chart_type == "employment":
                return self.create_employment_chart(df, title, dashboard_id)
            elif chart_type == "salary_analysis":
                return self.create_salary_analysis_chart(df, title, dashboard_id)
            elif chart_type == "terminal_efficiency":
                return self.create_terminal_efficiency_chart(df, title, dashboard_id)
            
            else:
                return self.create_placeholder({"name": title}, dashboard_id)
                
        except Exception as e:
            return {"error": f"Error creando gráfico {title}: {str(e)}"}
    
    def create_indicators(self, df, title, dashboard_id):
        """Crear indicadores numéricos"""
        try:
            if df.empty:
                return {"error": "No hay datos disponibles"}
            
            row = df.iloc[0]
            html = f"""
            <div class="container-fluid p-3">
                <div class="row text-center">
                    <div class="col-6 col-md-3 mb-3">
                        <div class="border rounded p-3 bg-primary text-white">
                            <h3 class="mb-1">{row.get('total', 0):,}</h3>
                            <small>Total</small>
                        </div>
                    </div>
                    <div class="col-6 col-md-3 mb-3">
                        <div class="border rounded p-3 bg-success text-white">
                            <h3 class="mb-1">{row.get('activos', 0):,}</h3>
                            <small>Activos</small>
                        </div>
                    </div>
                    <div class="col-6 col-md-3 mb-3">
                        <div class="border rounded p-3 bg-info text-white">
                            <h3 class="mb-1">{row.get('con_beca', 0):,}</h3>
                            <small>Con Beca</small>
                        </div>
                    </div>
                    <div class="col-6 col-md-3 mb-3">
                        <div class="border rounded p-3 bg-warning text-white">
                            <h3 class="mb-1">{row.get('edad_promedio', 0):.1f}</h3>
                            <small>Edad Promedio</small>
                        </div>
                    </div>
                </div>
            </div>
            """
            return {"chart": html, "data": df.to_dict('records')}
        except Exception as e:
            return {"error": f"Error en indicadores: {str(e)}"}
    
    def create_pie_chart(self, df, title, dashboard_id):
        """Crear gráfico de pastel"""
        try:
            if df.empty:
                return {"error": "No hay datos disponibles"}
            
            # Detectar columnas automáticamente
            label_col = df.columns[0]
            value_col = df.columns[1]
            
            fig = px.pie(df, values=value_col, names=label_col, title=title)
            fig.update_layout(height=350, margin=dict(t=50, b=0, l=0, r=0))
            
            return {"chart": fig.to_html(div_id=f"chart-{dashboard_id}"), "data": df.to_dict('records')}
        except Exception as e:
            return {"error": f"Error en gráfico de pastel: {str(e)}"}
    
    def create_bar_chart(self, df, title, dashboard_id):
        """Crear gráfico de barras vertical"""
        try:
            if df.empty:
                return {"error": "No hay datos disponibles"}
            
            x_col = df.columns[0]
            y_col = df.columns[1]
            
            fig = px.bar(df, x=x_col, y=y_col, title=title)
            fig.update_layout(height=350, margin=dict(t=50, b=40, l=40, r=40))
            
            return {"chart": fig.to_html(div_id=f"chart-{dashboard_id}"), "data": df.to_dict('records')}
        except Exception as e:
            return {"error": f"Error en gráfico de barras: {str(e)}"}
    
    def create_horizontal_bar_chart(self, df, title, dashboard_id):
        """Crear gráfico de barras horizontal"""
        try:
            if df.empty:
                return {"error": "No hay datos disponibles"}
            
            x_col = df.columns[1]  # Valor
            y_col = df.columns[0]  # Etiqueta
            
            fig = px.bar(df, x=x_col, y=y_col, orientation='h', title=title)
            fig.update_layout(height=350, margin=dict(t=50, b=40, l=100, r=40))
            
            return {"chart": fig.to_html(div_id=f"chart-{dashboard_id}"), "data": df.to_dict('records')}
        except Exception as e:
            return {"error": f"Error en gráfico de barras horizontal: {str(e)}"}
    
    def create_line_chart(self, df, title, dashboard_id):
        """Crear gráfico de líneas"""
        try:
            if df.empty:
                return {"error": "No hay datos disponibles"}
            
            x_col = df.columns[0]
            y_col = df.columns[1]
            
            fig = px.line(df, x=x_col, y=y_col, title=title, markers=True)
            fig.update_layout(height=350, margin=dict(t=50, b=40, l=40, r=40))
            
            return {"chart": fig.to_html(div_id=f"chart-{dashboard_id}"), "data": df.to_dict('records')}
        except Exception as e:
            return {"error": f"Error en gráfico de líneas: {str(e)}"}
    
    def create_scatter_chart(self, df, title, dashboard_id):
        """Crear gráfico de dispersión"""
        try:
            if df.empty:
                return {"error": "No hay datos disponibles"}
            
            x_col = df.columns[0]
            y_col = df.columns[1]
            
            # Si hay una tercera columna, usarla para hover
            hover_data = [df.columns[2]] if len(df.columns) > 2 else None
            
            fig = px.scatter(df, x=x_col, y=y_col, title=title, hover_data=hover_data)
            fig.update_layout(height=350, margin=dict(t=50, b=40, l=40, r=40))
            
            return {"chart": fig.to_html(div_id=f"chart-{dashboard_id}"), "data": df.to_dict('records')}
        except Exception as e:
            return {"error": f"Error en gráfico de dispersión: {str(e)}"}
    
    def create_grouped_bar_chart(self, df, title, dashboard_id):
        """Crear gráfico de barras agrupadas"""
        try:
            if df.empty:
                return {"error": "No hay datos disponibles"}
            
            # Asumir que las columnas son: categoría, valor1, valor2, etc.
            category_col = df.columns[0]
            
            fig = go.Figure()
            
            for col in df.columns[1:]:
                fig.add_trace(go.Bar(
                    name=col.replace('_', ' ').title(),
                    x=df[category_col],
                    y=df[col]
                ))
            
            fig.update_layout(
                title=title,
                barmode='group',
                height=350,
                margin=dict(t=50, b=40, l=40, r=40)
            )
            
            return {"chart": fig.to_html(div_id=f"chart-{dashboard_id}"), "data": df.to_dict('records')}
        except Exception as e:
            return {"error": f"Error en gráfico de barras agrupadas: {str(e)}"}
    
    def create_histogram_chart(self, df, title, dashboard_id):
        """Crear histograma"""
        try:
            if df.empty:
                return {"error": "No hay datos disponibles"}
            
            value_col = df.columns[0]
            
            fig = px.histogram(df, x=value_col, title=title, nbins=10)
            fig.update_layout(height=350, margin=dict(t=50, b=40, l=40, r=40))
            
            return {"chart": fig.to_html(div_id=f"chart-{dashboard_id}"), "data": df.to_dict('records')}
        except Exception as e:
            return {"error": f"Error en histograma: {str(e)}"}
    
    def create_bar_line_chart(self, df, title, dashboard_id):
        """Crear gráfico combinado barras + línea"""
        try:
            if df.empty:
                return {"error": "No hay datos disponibles"}
            
            x_col = df.columns[0]
            y1_col = df.columns[1]
            y2_col = df.columns[2] if len(df.columns) > 2 else df.columns[1]
            
            fig = make_subplots(specs=[[{"secondary_y": True}]])
            
            fig.add_trace(
                go.Bar(x=df[x_col], y=df[y1_col], name=y1_col.replace('_', ' ').title()),
                secondary_y=False,
            )
            
            fig.add_trace(
                go.Scatter(x=df[x_col], y=df[y2_col], mode='lines+markers', 
                          name=y2_col.replace('_', ' ').title()),
                secondary_y=True,
            )
            
            fig.update_layout(title=title, height=350, margin=dict(t=50, b=40, l=40, r=40))
            fig.update_yaxes(title_text="Cantidad", secondary_y=False)
            fig.update_yaxes(title_text="Promedio", secondary_y=True)
            
            return {"chart": fig.to_html(div_id=f"chart-{dashboard_id}"), "data": df.to_dict('records')}
        except Exception as e:
            return {"error": f"Error en gráfico combinado: {str(e)}"}
    
    def create_box_chart(self, df, title, dashboard_id):
        """Crear gráfico de caja (box plot)"""
        try:
            if df.empty:
                return {"error": "No hay datos disponibles"}
            
            # Para box plot, necesitamos los datos expandidos
            category_col = df.columns[0]
            
            fig = go.Figure()
            
            # Si tenemos columnas de salarios min, max, promedio
            if 'salario_min' in df.columns:
                for _, row in df.iterrows():
                    # Simular distribución basada en min, max, promedio
                    salarios = [
                        row['salario_min'], 
                        row['salario_promedio'],
                        row['salario_max']
                    ]
                    fig.add_trace(go.Box(
                        y=salarios,
                        name=row[category_col],
                        boxpoints='all'
                    ))
            else:
                # Box plot simple
                value_col = df.columns[1]
                fig.add_trace(go.Box(y=df[value_col], name=title))
            
            fig.update_layout(title=title, height=350, margin=dict(t=50, b=40, l=40, r=40))
            
            return {"chart": fig.to_html(div_id=f"chart-{dashboard_id}"), "data": df.to_dict('records')}
        except Exception as e:
            return {"error": f"Error en gráfico de caja: {str(e)}"}
    
    def create_subplots_chart(self, df, title, dashboard_id):
        """Crear dashboard integral con múltiples subgráficos"""
        try:
            fig = make_subplots(
                rows=2, cols=2,
                subplot_titles=('Estudiantes por Carrera', 'Calificaciones', 'Pagos', 'Egresados'),
                specs=[[{"type": "bar"}, {"type": "scatter"}],
                       [{"type": "bar"}, {"type": "bar"}]]
            )
            
            # Datos simulados para el dashboard integral
            carreras = ['Sistemas', 'Industrial', 'Mecánica', 'Civil']
            estudiantes = [120, 98, 75, 65]
            calificaciones = [85, 82, 88, 79]
            pagos = [95, 87, 92, 83]
            egresados = [45, 32, 28, 25]
            
            # Gráfico 1: Estudiantes por carrera
            fig.add_trace(
                go.Bar(x=carreras, y=estudiantes, name="Estudiantes"),
                row=1, col=1
            )
            
            # Gráfico 2: Calificaciones
            fig.add_trace(
                go.Scatter(x=carreras, y=calificaciones, mode='lines+markers', name="Promedio"),
                row=1, col=2
            )
            
            # Gráfico 3: Pagos
            fig.add_trace(
                go.Bar(x=carreras, y=pagos, name="% Pagos", marker_color='lightblue'),
                row=2, col=1
            )
            
            # Gráfico 4: Egresados
            fig.add_trace(
                go.Bar(x=carreras, y=egresados, name="Egresados", marker_color='lightgreen'),
                row=2, col=2
            )
            
            fig.update_layout(
                title=title,
                height=500,
                showlegend=False,
                margin=dict(t=80, b=40, l=40, r=40)
            )
            
            return {"chart": fig.to_html(div_id=f"chart-{dashboard_id}"), "data": []}
        except Exception as e:
            return {"error": f"Error en dashboard integral: {str(e)}"}
    
    def create_placeholder(self, dashboard_info, dashboard_id):
        """Crear placeholder para dashboards sin implementar"""
        html = f"""
        <div class="d-flex align-items-center justify-content-center h-100 text-muted">
            <div class="text-center">
                <i class="fas fa-chart-area fa-3x mb-3 opacity-50"></i>
                <h5>Dashboard en Desarrollo</h5>
                <p>#{dashboard_id} - {dashboard_info.get('name', 'Dashboard')}</p>
                <small>Próximamente disponible</small>
            </div>
        </div>
        """
        return {"chart": html, "data": []}
    
    def create_capacity_chart(self, df, title, dashboard_id):
        """Crear gráfico de capacidad vs ocupación"""
        try:
            if df.empty:
                return {"error": "No hay datos disponibles"}
            
            fig = go.Figure()
            
            # Barras de ocupación
            fig.add_trace(go.Bar(
                name='Ocupación Actual',
                x=df['grupo'],
                y=df['ocupacion'],
                marker_color='lightblue'
            ))
            
            # Línea de capacidad máxima
            fig.add_trace(go.Scatter(
                name='Capacidad Máxima',
                x=df['grupo'],
                y=df['capacidad_maxima'],
                mode='lines+markers',
                line=dict(color='red', dash='dash'),
                yaxis='y'
            ))
            
            fig.update_layout(
                title=title,
                xaxis_title="Grupos",
                yaxis_title="Número de Estudiantes",
                height=400,
                margin=dict(t=50, b=100, l=40, r=40),
                xaxis={'tickangle': -45}
            )
            
            return {"chart": fig.to_html(div_id=f"chart-{dashboard_id}"), "data": df.to_dict('records')}
        except Exception as e:
            return {"error": f"Error en gráfico de capacidad: {str(e)}"}

    def create_morosity_chart(self, df, title, dashboard_id):
        """Crear gráfico de morosidad por carrera"""
        try:
            if df.empty:
                return {"error": "No hay datos disponibles"}
            
            fig = make_subplots(specs=[[{"secondary_y": True}]])
            
            # Barras de estudiantes morosos
            fig.add_trace(
                go.Bar(
                    name='Estudiantes Morosos',
                    x=df['carrera'],
                    y=df['estudiantes_morosos'],
                    marker_color='red',
                    opacity=0.7
                ),
                secondary_y=False,
            )
            
            # Línea de porcentaje de morosidad
            fig.add_trace(
                go.Scatter(
                    name='% Morosidad',
                    x=df['carrera'],
                    y=df['porcentaje_morosidad'],
                    mode='lines+markers',
                    line=dict(color='darkred', width=3),
                    marker=dict(size=8)
                ),
                secondary_y=True,
            )
            
            fig.update_layout(
                title=title,
                height=400,
                margin=dict(t=50, b=100, l=40, r=40),
                xaxis={'tickangle': -45}
            )
            
            fig.update_yaxes(title_text="Número de Estudiantes", secondary_y=False)
            fig.update_yaxes(title_text="Porcentaje de Morosidad (%)", secondary_y=True)
            
            return {"chart": fig.to_html(div_id=f"chart-{dashboard_id}"), "data": df.to_dict('records')}
        except Exception as e:
            return {"error": f"Error en gráfico de morosidad: {str(e)}"}

    def create_employment_chart(self, df, title, dashboard_id):
        """Crear gráfico de inserción laboral"""
        try:
            if df.empty:
                return {"error": "No hay datos disponibles"}
            
            fig = go.Figure()
            
            # Barras apiladas para empleados vs desempleados
            fig.add_trace(go.Bar(
                name='Empleados',
                x=df['carrera'],
                y=df['empleados'],
                marker_color='green',
                text=df['empleados'],
                textposition='inside'
            ))
            
            fig.add_trace(go.Bar(
                name='Desempleados',
                x=df['carrera'],
                y=df['desempleados'],
                marker_color='orange',
                text=df['desempleados'],
                textposition='inside'
            ))
            
            # Línea de porcentaje de empleabilidad
            fig.add_trace(go.Scatter(
                name='% Empleabilidad',
                x=df['carrera'],
                y=df['porcentaje_empleabilidad'],
                mode='lines+markers',
                line=dict(color='darkgreen', width=3),
                marker=dict(size=10),
                yaxis='y2'
            ))
            
            fig.update_layout(
                title=title,
                barmode='stack',
                height=400,
                margin=dict(t=50, b=100, l=40, r=40),
                xaxis={'tickangle': -45},
                yaxis=dict(title="Número de Egresados"),
                yaxis2=dict(
                    title="Porcentaje de Empleabilidad (%)",
                    overlaying='y',
                    side='right'
                )
            )
            
            return {"chart": fig.to_html(div_id=f"chart-{dashboard_id}"), "data": df.to_dict('records')}
        except Exception as e:
            return {"error": f"Error en gráfico de empleo: {str(e)}"}

    def create_salary_analysis_chart(self, df, title, dashboard_id):
        """Crear gráfico de análisis salarial por área"""
        try:
            if df.empty:
                return {"error": "No hay datos disponibles"}
            
            # Agrupar por área para crear box plots
            areas = df['area'].unique()
            
            fig = go.Figure()
            
            for area in areas:
                area_data = df[df['area'] == area]
                fig.add_trace(go.Box(
                    y=area_data['salario'],
                    name=area,
                    boxpoints='outliers',
                    hovertemplate=f"<b>{area}</b><br>" +
                                  "Salario: $%{y:,.0f}<br>" +
                                  "<extra></extra>"
                ))
            
            fig.update_layout(
                title=title,
                yaxis_title="Salario Inicial (MXN)",
                height=400,
                margin=dict(t=50, b=40, l=60, r=40)
            )
            
            # Agregar información estadística
            stats_text = []
            for area in areas:
                area_data = df[df['area'] == area]['salario']
                if len(area_data) > 0:
                    stats_text.append(f"{area}: Promedio ${area_data.mean():,.0f}")
            
            return {
                "chart": fig.to_html(div_id=f"chart-{dashboard_id}"), 
                "data": df.to_dict('records'),
                "stats": stats_text
            }
        except Exception as e:
            return {"error": f"Error en análisis salarial: {str(e)}"}

    def create_terminal_efficiency_chart(self, df, title, dashboard_id):
        """Crear gráfico de eficiencia terminal"""
        try:
            if df.empty:
                return {"error": "No hay datos disponibles"}
            
            fig = make_subplots(
                rows=1, cols=1,
                specs=[[{"secondary_y": True}]]
            )
            
            # Barras de eficiencia porcentual
            fig.add_trace(
                go.Bar(
                    name='Eficiencia Terminal (%)',
                    x=df['carrera'],
                    y=df['eficiencia_porcentaje'],
                    marker_color='lightgreen',
                    text=[f"{val}%" for val in df['eficiencia_porcentaje']],
                    textposition='outside'
                ),
                secondary_y=False
            )
            
            # Línea de tiempo promedio real
            fig.add_trace(
                go.Scatter(
                    name='Meses Promedio Real',
                    x=df['carrera'],
                    y=df['promedio_meses_reales'],
                    mode='lines+markers',
                    line=dict(color='red', width=3),
                    marker=dict(size=8)
                ),
                secondary_y=True
            )
            
            # Línea de tiempo teórico
            fig.add_trace(
                go.Scatter(
                    name='Duración Teórica',
                    x=df['carrera'],
                    y=df['duracion_meses_teorica'],
                    mode='lines+markers',
                    line=dict(color='blue', width=2, dash='dash'),
                    marker=dict(size=6)
                ),
                secondary_y=True
            )
            
            fig.update_layout(
                title=title,
                height=400,
                margin=dict(t=50, b=100, l=40, r=40),
                xaxis={'tickangle': -45}
            )
            
            fig.update_yaxes(title_text="Eficiencia Terminal (%)", secondary_y=False)
            fig.update_yaxes(title_text="Duración (Meses)", secondary_y=True)
            
            return {"chart": fig.to_html(div_id=f"chart-{dashboard_id}"), "data": df.to_dict('records')}
        except Exception as e:
            return {"error": f"Error en eficiencia terminal: {str(e)}"}