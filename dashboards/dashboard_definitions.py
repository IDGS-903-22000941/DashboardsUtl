import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

class DashboardManager:
    def __init__(self, db):
        self.db = db
        self.dashboards = self.get_dashboard_list()
    
    def get_dashboard_list(self):
        return [
            # Dashboards de Estudiantes (1-10)
            {"id": 1, "name": "Total de Estudiantes", "category": "Estudiantes", "description": "Resumen general de estudiantes"},
            {"id": 2, "name": "Estudiantes por Carrera", "category": "Estudiantes", "description": "Distribución de estudiantes por carrera"},
            {"id": 3, "name": "Estudiantes por Género", "category": "Estudiantes", "description": "Distribución por género"},
            {"id": 4, "name": "Estudiantes por Edad", "category": "Estudiantes", "description": "Distribución por grupos de edad"},
            {"id": 5, "name": "Estudiantes por Estado", "category": "Estudiantes", "description": "Origen geográfico de estudiantes"},
            {"id": 6, "name": "Estudiantes Activos vs Inactivos", "category": "Estudiantes", "description": "Estado de actividad"},
            {"id": 7, "name": "Estudiantes con Beca", "category": "Estudiantes", "description": "Análisis de becarios"},
            {"id": 8, "name": "Tipos de Escuela de Origen", "category": "Estudiantes", "description": "Pública vs Privada"},
            {"id": 9, "name": "Evolución de Inscripciones", "category": "Estudiantes", "description": "Tendencia temporal"},
            {"id": 10, "name": "Estudiantes por Período", "category": "Estudiantes", "description": "Distribución por período"},
            
            # Dashboards Académicos (11-20)
            {"id": 11, "name": "Promedios por Carrera", "category": "Académico", "description": "Rendimiento académico por carrera"},
            {"id": 12, "name": "Materias más Reprobadas", "category": "Académico", "description": "Análisis de reprobación"},
            {"id": 13, "name": "Calificaciones por Cuatrimestre", "category": "Académico", "description": "Evolución de calificaciones"},
            {"id": 14, "name": "Tipos de Evaluación", "category": "Académico", "description": "Ordinario vs Extraordinario"},
            {"id": 15, "name": "Asistencias vs Calificaciones", "category": "Académico", "description": "Correlación asistencia-rendimiento"},
            {"id": 16, "name": "Profesores por Materia", "category": "Académico", "description": "Carga docente"},
            {"id": 17, "name": "Grupos por Período", "category": "Académico", "description": "Organización de grupos"},
            {"id": 18, "name": "Utilización de Aulas", "category": "Académico", "description": "Ocupación de espacios"},
            {"id": 19, "name": "Horarios más Demandados", "category": "Académico", "description": "Preferencias de horario"},
            {"id": 20, "name": "Créditos por Estudiante", "category": "Académico", "description": "Carga académica"},
            
            # Dashboards de Riesgo (21-25)
            {"id": 21, "name": "Estudiantes en Riesgo", "category": "Riesgo", "description": "Análisis de riesgo académico"},
            {"id": 22, "name": "Nivel de Riesgo por Carrera", "category": "Riesgo", "description": "Riesgo por programa"},
            {"id": 23, "name": "Abandono Escolar", "category": "Riesgo", "description": "Tipos y causas de abandono"},
            {"id": 24, "name": "Predicción de Abandono", "category": "Riesgo", "description": "Factores de riesgo"},
            {"id": 25, "name": "Acciones de Intervención", "category": "Riesgo", "description": "Medidas tomadas"},
            
            # Dashboards Financieros (26-30)
            {"id": 26, "name": "Pagos por Período", "category": "Financiero", "description": "Ingresos por colegiaturas"},
            {"id": 27, "name": "Morosidad", "category": "Financiero", "description": "Pagos vencidos"},
            {"id": 28, "name": "Becas Otorgadas", "category": "Financiero", "description": "Inversión en becas"},
            {"id": 29, "name": "Métodos de Pago", "category": "Financiero", "description": "Formas de pago preferidas"},
            {"id": 30, "name": "Descuentos Aplicados", "category": "Financiero", "description": "Beneficios otorgados"},
            
            # Dashboards de Egresados (31-35)
            {"id": 31, "name": "Egresados por Año", "category": "Egresados", "description": "Graduados por período"},
            {"id": 32, "name": "Empleabilidad", "category": "Egresados", "description": "Inserción laboral"},
            {"id": 33, "name": "Salarios Iniciales", "category": "Egresados", "description": "Remuneración al egresar"},
            {"id": 34, "name": "Satisfacción con la Carrera", "category": "Egresados", "description": "Evaluación de egresados"},
            {"id": 35, "name": "Tiempo de Titulación", "category": "Egresados", "description": "Eficiencia terminal"},
            
            # Dashboards de Recursos (36-40)
            {"id": 36, "name": "Uso de Biblioteca", "category": "Recursos", "description": "Utilización de recursos bibliográficos"},
            {"id": 37, "name": "Uso de Laboratorios", "category": "Recursos", "description": "Ocupación de laboratorios"},
            {"id": 38, "name": "Recursos por Estudiante", "category": "Recursos", "description": "Distribución de recursos"},
            {"id": 39, "name": "Horarios de Mayor Uso", "category": "Recursos", "description": "Patrones de uso"},
            {"id": 40, "name": "Dashboard Integral", "category": "General", "description": "Vista general de todos los indicadores"}
        ]
    
    def generate_dashboard(self, dashboard_id, filters=None):
        dashboard_info = next((d for d in self.dashboards if d["id"] == dashboard_id), None)
        if not dashboard_info:
            return None
        
        # Aquí generamos el dashboard específico
        if dashboard_id == 1:
            return self.dashboard_total_estudiantes(filters)
        elif dashboard_id == 2:
            return self.dashboard_estudiantes_por_carrera(filters)
        elif dashboard_id == 3:
            return self.dashboard_estudiantes_por_genero(filters)
        elif dashboard_id == 11:
            return self.dashboard_promedios_por_carrera(filters)
        elif dashboard_id == 21:
            return self.dashboard_estudiantes_riesgo(filters)
        # ... más dashboards
        else:
            return self.dashboard_placeholder(dashboard_info)
    
    def dashboard_total_estudiantes(self, filters=None):
        data = self.db.get_estudiantes_stats()
        if not data:
            return {"error": "No se pudieron obtener los datos"}
        
        stats = data[0]
        
        # Crear gráfico de tarjetas
        fig = go.Figure()
        fig.add_trace(go.Indicator(
            mode = "number",
            value = stats['total_estudiantes'],
            title = {"text": "Total Estudiantes"},
            domain = {'x': [0, 0.25], 'y': [0, 1]}
        ))
        
        fig.add_trace(go.Indicator(
            mode = "number",
            value = stats['activos'],
            title = {"text": "Estudiantes Activos"},
            domain = {'x': [0.25, 0.5], 'y': [0, 1]}
        ))
        
        fig.add_trace(go.Indicator(
            mode = "number",
            value = stats['con_beca'],
            title = {"text": "Con Beca"},
            domain = {'x': [0.5, 0.75], 'y': [0, 1]}
        ))
        
        fig.add_trace(go.Indicator(
            mode = "number",
            value = round(stats['edad_promedio'], 1),
            title = {"text": "Edad Promedio"},
            domain = {'x': [0.75, 1], 'y': [0, 1]}
        ))
        
        fig.update_layout(height=400, title="Resumen General de Estudiantes")
        
        return {
            "chart": fig.to_html(include_plotlyjs=True, div_id="chart"),
            "data": stats
        }
    
    def dashboard_estudiantes_por_carrera(self, filters=None):
        data = self.db.get_carreras_stats()
        if not data:
            return {"error": "No se pudieron obtener los datos"}
        
        df = pd.DataFrame(data)
        
        # Gráfico de barras
        fig = px.bar(
            df, 
            x='carrera', 
            y='total_estudiantes',
            color='nivel',
            title='Estudiantes por Carrera',
            labels={'total_estudiantes': 'Número de Estudiantes', 'carrera': 'Carrera'}
        )
        fig.update_xaxis(tickangle=45)
        fig.update_layout(height=500)
        
        return {
            "chart": fig.to_html(include_plotlyjs=True, div_id="chart"),
            "data": data
        }
    
    def dashboard_estudiantes_por_genero(self, filters=None):
        query = """
        SELECT 
            genero,
            COUNT(*) as cantidad
        FROM estudiantes
        WHERE activo = 1
        GROUP BY genero
        """
        data = self.db.execute_query(query)
        
        if not data:
            return {"error": "No se pudieron obtener los datos"}
        
        df = pd.DataFrame(data)
        
        # Gráfico de pastel
        fig = px.pie(
            df,
            values='cantidad',
            names='genero',
            title='Distribución por Género'
        )
        fig.update_layout(height=400)
        
        return {
            "chart": fig.to_html(include_plotlyjs=True, div_id="chart"),
            "data": data
        }
    
    def dashboard_promedios_por_carrera(self, filters=None):
        query = """
        SELECT 
            c.nombre as carrera,
            AVG(cal.calificacion_final) as promedio
        FROM calificaciones cal
        JOIN estudiantes e ON cal.id_estudiante = e.id
        JOIN carreras c ON e.carrera_codigo = c.codigo
        WHERE cal.calificacion_final IS NOT NULL
        GROUP BY c.nombre
        ORDER BY promedio DESC
        """
        data = self.db.execute_query(query)
        
        if not data:
            return {"error": "No se pudieron obtener los datos"}
        
        df = pd.DataFrame(data)
        
        # AQUI SE ARREGLA EL ERROR: Convierte la columna 'promedio' a tipo numérico
        # 'errors='coerce'' convertirá cualquier valor que no sea un número en NaN (Not a Number)
        df['promedio'] = pd.to_numeric(df['promedio'], errors='coerce')
        
        # Opcional: Si quieres eliminar filas donde 'promedio' se convirtió a NaN
        # df.dropna(subset=['promedio'], inplace=True)

        df['promedio'] = df['promedio'].round(2)
        
        # Gráfico de barras horizontales
        fig = px.bar(
            df,
            x='promedio',
            y='carrera',
            orientation='h',
            title='Promedio de Calificaciones por Carrera',
            color='promedio',
            color_continuous_scale='RdYlGn'
        )
        fig.update_layout(height=500)
        
        return {
            "chart": fig.to_html(include_plotlyjs=True, div_id="chart"),
            "data": data
        }
    
    def dashboard_estudiantes_riesgo(self, filters=None):
        data = self.db.get_riesgo_academico_stats()
        
        if not data:
            return {"error": "No se pudieron obtener los datos"}
        
        df = pd.DataFrame(data)
        
        # Gráfico de barras con colores por nivel de riesgo
        colors = {'Bajo': 'green', 'Medio': 'yellow', 'Alto': 'orange', 'Critico': 'red'}
        fig = px.bar(
            df,
            x='nivel_riesgo',
            y='cantidad',
            title='Estudiantes por Nivel de Riesgo Académico',
            color='nivel_riesgo',
            color_discrete_map=colors
        )
        fig.update_layout(height=400)
        
        return {
            "chart": fig.to_html(include_plotlyjs=True, div_id="chart"),
            "data": data
        }
    
    def dashboard_placeholder(self, dashboard_info):
        # Dashboard temporal para los que no están implementados
        fig = go.Figure()
        fig.add_annotation(
            text=f"Dashboard en construcción<br>{dashboard_info['name']}",
            xref="paper", yref="paper",
            x=0.5, y=0.5, xanchor='center', yanchor='middle',
            showarrow=False,
            font=dict(size=20)
        )
        fig.update_layout(
            height=400,
            title=dashboard_info['name']
        )
        
        return {
            "chart": fig.to_html(include_plotlyjs=True, div_id="chart"),
            "data": {"message": "Dashboard en desarrollo"}
        }