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
        
        # Mapeo de dashboards
        dashboard_methods = {
            1: self.dashboard_total_estudiantes,
            2: self.dashboard_estudiantes_por_carrera,
            3: self.dashboard_estudiantes_por_genero,
            4: self.dashboard_estudiantes_por_edad,
            5: self.dashboard_estudiantes_por_estado,
            6: self.dashboard_activos_inactivos,
            7: self.dashboard_estudiantes_beca,
            8: self.dashboard_tipo_escuela,
            9: self.dashboard_evolución_inscripciones,
            10: self.dashboard_estudiantes_periodo,
            11: self.dashboard_promedios_por_carrera,
            12: self.dashboard_materias_reprobadas,
            13: self.dashboard_calificaciones_cuatrimestre,
            21: self.dashboard_estudiantes_riesgo,
            23: self.dashboard_abandono_escolar,
            26: self.dashboard_pagos_periodo,
            31: self.dashboard_egresados_año,
            36: self.dashboard_uso_recursos
        }
        
        if dashboard_id in dashboard_methods:
            return dashboard_methods[dashboard_id](filters, dashboard_id)
        else:
            return self.dashboard_placeholder(dashboard_info, dashboard_id)
    
    def dashboard_total_estudiantes(self, filters=None, dashboard_id=1):
        data = self.db.get_estudiantes_stats()
        if not data:
            return {"error": "No se pudieron obtener los datos de estudiantes"}
        
        stats = data[0]
        
        # Crear gráfico de tarjetas con ID único
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
            value = round(float(stats['edad_promedio']) if stats['edad_promedio'] else 0, 1),
            title = {"text": "Edad Promedio"},
            domain = {'x': [0.75, 1], 'y': [0, 1]}
        ))
        
        fig.update_layout(height=400, title="Resumen General de Estudiantes")
        
        return {
            "chart": fig.to_html(include_plotlyjs=True, div_id=f"chart-{dashboard_id}"),
            "data": stats
        }
    
    def dashboard_estudiantes_por_carrera(self, filters=None, dashboard_id=2):
        data = self.db.get_carreras_stats()
        if not data:
            return {"error": "No se pudieron obtener los datos de carreras"}
        
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
        fig.update_xaxes(tickangle=45)
        fig.update_layout(height=500)
        
        return {
            "chart": fig.to_html(include_plotlyjs=True, div_id=f"chart-{dashboard_id}"),
            "data": data
        }
    
    def dashboard_estudiantes_por_genero(self, filters=None, dashboard_id=3):
        data = self.db.get_genero_stats()
        
        if not data:
            return {"error": "No se pudieron obtener los datos de género"}
        
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
            "chart": fig.to_html(include_plotlyjs=True, div_id=f"chart-{dashboard_id}"),
            "data": data
        }
    
    def dashboard_estudiantes_por_edad(self, filters=None, dashboard_id=4):
        data = self.db.get_estudiantes_por_edad()
        
        if not data:
            return {"error": "No se pudieron obtener los datos de edad"}
        
        df = pd.DataFrame(data)
        
        fig = px.bar(
            df,
            x='rango_edad',
            y='cantidad',
            title='Distribución por Rangos de Edad',
            color='cantidad',
            color_continuous_scale='Blues'
        )
        fig.update_layout(height=400)
        
        return {
            "chart": fig.to_html(include_plotlyjs=True, div_id=f"chart-{dashboard_id}"),
            "data": data
        }
    
    def dashboard_estudiantes_por_estado(self, filters=None, dashboard_id=5):
        data = self.db.get_estudiantes_por_estado()
        
        if not data:
            return {"error": "No se pudieron obtener los datos por estado"}
        
        df = pd.DataFrame(data)
        
        fig = px.bar(
            df,
            y='estado',
            x='cantidad',
            orientation='h',
            title='Estudiantes por Estado (Top 10)',
            color='cantidad',
            color_continuous_scale='Viridis'
        )
        fig.update_layout(height=500)
        
        return {
            "chart": fig.to_html(include_plotlyjs=True, div_id=f"chart-{dashboard_id}"),
            "data": data
        }
    
    def dashboard_activos_inactivos(self, filters=None, dashboard_id=6):
        # Consulta directa para activos/inactivos
        query = """
        SELECT 
            CASE WHEN activo = 1 THEN 'Activos' ELSE 'Inactivos' END as estado,
            COUNT(*) as cantidad
        FROM estudiantes
        GROUP BY activo
        """
        data = self.db.execute_query(query)
        
        if not data:
            return {"error": "No se pudieron obtener los datos de estado"}
        
        df = pd.DataFrame(data)
        
        fig = px.pie(
            df,
            values='cantidad',
            names='estado',
            title='Estudiantes Activos vs Inactivos',
            color_discrete_map={'Activos': 'green', 'Inactivos': 'red'}
        )
        fig.update_layout(height=400)
        
        return {
            "chart": fig.to_html(include_plotlyjs=True, div_id=f"chart-{dashboard_id}"),
            "data": data
        }
    
    def dashboard_estudiantes_beca(self, filters=None, dashboard_id=7):
        data = self.db.get_becas_stats()
        
        if not data:
            return {"error": "No se pudieron obtener los datos de becas"}
        
        df = pd.DataFrame(data)
        
        fig = px.pie(
            df,
            values='cantidad',
            names='estado_beca',
            title='Estudiantes con y sin Beca'
        )
        fig.update_layout(height=400)
        
        return {
            "chart": fig.to_html(include_plotlyjs=True, div_id=f"chart-{dashboard_id}"),
            "data": data
        }
    
    def dashboard_tipo_escuela(self, filters=None, dashboard_id=8):
        data = self.db.get_tipo_escuela_stats()
        
        if not data:
            return {"error": "No se pudieron obtener los datos de tipo de escuela"}
        
        df = pd.DataFrame(data)
        
        fig = px.bar(
            df,
            x='tipo_escuela',
            y='cantidad',
            title='Estudiantes por Tipo de Escuela de Origen',
            color='tipo_escuela'
        )
        fig.update_layout(height=400)
        
        return {
            "chart": fig.to_html(include_plotlyjs=True, div_id=f"chart-{dashboard_id}"),
            "data": data
        }
    
    def dashboard_evolución_inscripciones(self, filters=None, dashboard_id=9):
        data = self.db.get_inscripciones_por_periodo()
        
        if not data:
            return {"error": "No se pudieron obtener los datos de inscripciones"}
        
        df = pd.DataFrame(data)
        
        fig = px.line(
            df,
            x='periodo',
            y='cantidad',
            title='Evolución de Inscripciones por Período',
            markers=True
        )
        fig.update_layout(height=400)
        
        return {
            "chart": fig.to_html(include_plotlyjs=True, div_id=f"chart-{dashboard_id}"),
            "data": data
        }
    
    def dashboard_estudiantes_periodo(self, filters=None, dashboard_id=10):
        data = self.db.get_inscripciones_por_periodo()
        
        if not data:
            return {"error": "No se pudieron obtener los datos por período"}
        
        df = pd.DataFrame(data)
        
        fig = px.bar(
            df,
            x='periodo',
            y='cantidad',
            title='Estudiantes por Período de Ingreso'
        )
        fig.update_xaxes(tickangle=45)
        fig.update_layout(height=400)
        
        return {
            "chart": fig.to_html(include_plotlyjs=True, div_id=f"chart-{dashboard_id}"),
            "data": data
        }
    
    def dashboard_promedios_por_carrera(self, filters=None, dashboard_id=11):
        data = self.db.get_promedios_carrera()
        
        if not data:
            return {"error": "No se pudieron obtener los datos de promedios"}
        
        df = pd.DataFrame(data)
        
        # Convertir promedio a numérico
        df['promedio'] = pd.to_numeric(df['promedio'], errors='coerce')
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
            "chart": fig.to_html(include_plotlyjs=True, div_id=f"chart-{dashboard_id}"),
            "data": data
        }
    
    def dashboard_materias_reprobadas(self, filters=None, dashboard_id=12):
        data = self.db.get_materias_reprobadas()
        
        if not data:
            return {"error": "No se pudieron obtener los datos de materias reprobadas"}
        
        df = pd.DataFrame(data)
        
        fig = px.bar(
            df,
            y='materia',
            x='reprobados',
            orientation='h',
            title='Materias más Reprobadas (Top 10)',
            color='reprobados',
            color_continuous_scale='Reds'
        )
        fig.update_layout(height=500)
        
        return {
            "chart": fig.to_html(include_plotlyjs=True, div_id=f"chart-{dashboard_id}"),
            "data": data
        }
    
    def dashboard_calificaciones_cuatrimestre(self, filters=None, dashboard_id=13):
        data = self.db.get_calificaciones_por_cuatrimestre()
        
        if not data:
            return {"error": "No se pudieron obtener los datos de calificaciones por cuatrimestre"}
        
        df = pd.DataFrame(data)
        df['promedio'] = pd.to_numeric(df['promedio'], errors='coerce')
        
        fig = px.line(
            df,
            x='cuatrimestre',
            y='promedio',
            title='Promedio de Calificaciones por Cuatrimestre',
            markers=True
        )
        fig.update_layout(height=400)
        
        return {
            "chart": fig.to_html(include_plotlyjs=True, div_id=f"chart-{dashboard_id}"),
            "data": data
        }
    
    def dashboard_estudiantes_riesgo(self, filters=None, dashboard_id=21):
        data = self.db.get_riesgo_academico_stats()
        
        if not data:
            return {"error": "No se pudieron obtener los datos de riesgo académico"}
        
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
            "chart": fig.to_html(include_plotlyjs=True, div_id=f"chart-{dashboard_id}"),
            "data": data
        }

    def dashboard_abandono_escolar(self, filters=None, dashboard_id=23):
        data = self.db.get_abandono_stats()
        
        if not data:
            return {"error": "No se pudieron obtener los datos de abandono"}
        
        df = pd.DataFrame(data)
        
        fig = px.pie(
            df,
            values='cantidad',
            names='tipo',
            title='Distribución de Tipos de Abandono Escolar'
        )
        fig.update_layout(height=400)
        
        return {
            "chart": fig.to_html(include_plotlyjs=True, div_id=f"chart-{dashboard_id}"),
            "data": data
        }
    
    def dashboard_pagos_periodo(self, filters=None, dashboard_id=26):
        data = self.db.get_pagos_por_periodo()
        
        if not data:
            return {"error": "No se pudieron obtener los datos de pagos"}
        
        df = pd.DataFrame(data)
        
        # Crear gráfico de barras agrupadas
        fig = make_subplots(
            rows=2, cols=1,
            subplot_titles=('Pagos por Período', 'Montos Totales'),
            vertical_spacing=0.15
        )
        
        fig.add_trace(
            go.Bar(
                x=df['periodo'],
                y=df['pagos_realizados'],
                name='Pagos Realizados',
                marker_color='green'
            ),
            row=1, col=1
        )
        
        fig.add_trace(
            go.Bar(
                x=df['periodo'],
                y=df['pagos_pendientes'],
                name='Pagos Pendientes',
                marker_color='red'
            ),
            row=1, col=1
        )
        
        fig.add_trace(
            go.Bar(
                x=df['periodo'],
                y=df['monto_total'],
                name='Monto Total',
                marker_color='blue'
            ),
            row=2, col=1
        )
        
        fig.update_layout(height=600, title="Análisis de Pagos por Período")
        
        return {
            "chart": fig.to_html(include_plotlyjs=True, div_id=f"chart-{dashboard_id}"),
            "data": data
        }
    
    def dashboard_egresados_año(self, filters=None, dashboard_id=31):
        data = self.db.get_egresados_por_año()
        
        if not data:
            return {"error": "No se pudieron obtener los datos de egresados"}
        
        df = pd.DataFrame(data)
        
        # Convertir promedio a numérico
        df['promedio_general'] = pd.to_numeric(df['promedio_general'], errors='coerce')
        
        # Crear gráfico de líneas con dos ejes Y
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        
        fig.add_trace(
            go.Bar(
                x=df['año'],
                y=df['cantidad'],
                name='Número de Egresados',
                marker_color='lightblue'
            ),
            secondary_y=False,
        )
        
        fig.add_trace(
            go.Scatter(
                x=df['año'],
                y=df['promedio_general'],
                mode='lines+markers',
                name='Promedio General',
                line=dict(color='red', width=3)
            ),
            secondary_y=True,
        )
        
        fig.update_xaxes(title_text="Año")
        fig.update_yaxes(title_text="Número de Egresados", secondary_y=False)
        fig.update_yaxes(title_text="Promedio General", secondary_y=True)
        fig.update_layout(height=400, title="Egresados por Año y Promedio General")
        
        return {
            "chart": fig.to_html(include_plotlyjs=True, div_id=f"chart-{dashboard_id}"),
            "data": data
        }
    
    def dashboard_uso_recursos(self, filters=None, dashboard_id=36):
        data = self.db.get_uso_recursos()
        
        if not data:
            return {"error": "No se pudieron obtener los datos de uso de recursos"}
        
        df = pd.DataFrame(data)
        
        # Convertir duración a numérico
        df['duracion_promedio'] = pd.to_numeric(df['duracion_promedio'], errors='coerce')
        
        fig = px.bar(
            df,
            y='recurso',
            x='usos',
            orientation='h',
            title='Uso de Recursos (Top 10)',
            color='duracion_promedio',
            color_continuous_scale='Viridis',
            hover_data=['duracion_promedio']
        )
        fig.update_layout(height=500)
        
        return {
            "chart": fig.to_html(include_plotlyjs=True, div_id=f"chart-{dashboard_id}"),
            "data": data
        }
    
    def dashboard_placeholder(self, dashboard_info, dashboard_id):
        """Método para dashboards no implementados"""
        fig = go.Figure()
        fig.add_annotation(
            text=f"Dashboard '{dashboard_info['name']}' en desarrollo",
            xref="paper", yref="paper",
            x=0.5, y=0.5, xanchor='center', yanchor='middle',
            showarrow=False,
            font=dict(size=16, color="gray")
        )
        fig.update_layout(
            height=400,
            title=f"{dashboard_info['name']} - En Desarrollo",
            xaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
            yaxis=dict(showgrid=False, showticklabels=False, zeroline=False)
        )
        
        return {
            "chart": fig.to_html(include_plotlyjs=True, div_id=f"chart-{dashboard_id}"),
            "data": {"message": "Dashboard en desarrollo"}
        }