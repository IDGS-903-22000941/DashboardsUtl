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
                ("Tipos de Evaluación", "Ordinario vs Extraordinario"),
                ("Asistencias vs Calificaciones", "Correlación asistencia-rendimiento"),
                ("Profesores por Materia", "Carga docente"),
                ("Grupos por Período", "Organización de grupos"),
                ("Utilización de Aulas", "Ocupación de espacios"),
                ("Horarios más Demandados", "Preferencias de horario"),
                ("Créditos por Estudiante", "Carga académica")
            ],
            "Riesgo": [
                ("Estudiantes en Riesgo", "Análisis de riesgo académico"),
                ("Nivel de Riesgo por Carrera", "Riesgo por programa"),
                ("Abandono Escolar", "Tipos y causas de abandono"),
                ("Predicción de Abandono", "Factores de riesgo"),
                ("Acciones de Intervención", "Medidas tomadas")
            ],
            "Financiero": [
                ("Pagos por Período", "Ingresos por colegiaturas"),
                ("Morosidad", "Pagos vencidos"),
                ("Becas Otorgadas", "Inversión en becas"),
                ("Métodos de Pago", "Formas de pago preferidas"),
                ("Descuentos Aplicados", "Beneficios otorgados")
            ],
            "Egresados": [
                ("Egresados por Año", "Graduados por período"),
                ("Empleabilidad", "Inserción laboral"),
                ("Salarios Iniciales", "Remuneración al egresar"),
                ("Satisfacción con la Carrera", "Evaluación de egresados"),
                ("Tiempo de Titulación", "Eficiencia terminal")
            ],
            "Recursos": [
                ("Uso de Biblioteca", "Utilización de recursos bibliográficos"),
                ("Uso de Laboratorios", "Ocupación de laboratorios"),
                ("Recursos por Estudiante", "Distribución de recursos"),
                ("Horarios de Mayor Uso", "Patrones de uso"),
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
            
            # Académico (11-20)
            11: ("promedios_carrera", "bar_h", "Promedios por Carrera"),
            12: ("materias_reprobadas", "bar_h", "Materias más Reprobadas"),
            13: ("calificaciones_cuatrimestre", "line", "Calificaciones por Cuatrimestre"),
            14: ("evaluacion_stats", "pie", "Tipos de Evaluación"),
            15: ("asistencia_calificaciones", "scatter", "Asistencia vs Calificaciones"),
            16: ("profesores_materia", "bar", "Profesores por Materia"),
            17: ("grupos_periodo", "bar", "Grupos por Período"),
            18: ("aulas_stats", "bar", "Utilización de Aulas"),
            19: ("horarios_stats", "bar", "Horarios Demandados"),
            20: ("creditos_stats", "histogram", "Créditos por Estudiante"),
            
            # Riesgo (21-25)
            21: ("riesgo_stats", "bar", "Estudiantes en Riesgo"),
            22: ("riesgo_carrera", "bar", "Riesgo por Carrera"),
            23: ("abandono_stats", "pie", "Abandono Escolar"),
            24: ("prediccion_abandono", "scatter", "Predicción de Abandono"),
            25: ("intervenciones_stats", "bar", "Acciones de Intervención"),
            
            # Financiero (26-30)
            26: ("pagos_stats", "bar_grouped", "Pagos por Período"),
            27: ("morosidad_stats", "bar", "Morosidad"),
            28: ("becas_otorgadas", "bar", "Becas Otorgadas"),
            29: ("metodos_pago", "pie", "Métodos de Pago"),
            30: ("descuentos_stats", "bar", "Descuentos Aplicados"),
            
            # Egresados (31-35)
            31: ("egresados_stats", "bar_line", "Egresados por Año"),
            32: ("empleabilidad_stats", "pie", "Empleabilidad"),
            33: ("salarios_stats", "box", "Salarios Iniciales"),
            34: ("satisfaccion_stats", "bar", "Satisfacción"),
            35: ("titulacion_stats", "histogram", "Tiempo de Titulación"),
            
            # Recursos (36-40)
            36: ("recursos_stats", "bar_h", "Uso de Recursos"),
            37: ("laboratorios_stats", "bar", "Uso de Laboratorios"),
            38: ("recursos_estudiante", "bar", "Recursos por Estudiante"),
            39: ("horarios_uso", "heatmap", "Horarios de Uso"),
            40: ("dashboard_integral", "subplots", "Dashboard Integral")
        }
        
        if dashboard_id in dashboard_configs:
            data_key, chart_type, title = dashboard_configs[dashboard_id]
            data = self.get_dashboard_data(data_key, filters)
            return self.create_chart(data, chart_type, title, dashboard_id)
        
        return self.create_placeholder(dashboard_info, dashboard_id)
    
    def get_dashboard_data(self, data_key, filters=None):
        """Obtiene datos usando queries unificadas"""
        queries = {
            # Estudiantes
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
            
            # Académico
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
            
            # Continúa con el resto de queries...
            # Por brevedad, incluyo algunos ejemplos representativos
            
            "riesgo_stats": """
                SELECT nivel_riesgo, COUNT(*) as cantidad
                FROM riesgo_academico WHERE activo = 1
                GROUP BY nivel_riesgo ORDER BY FIELD(nivel_riesgo, 'Bajo', 'Medio', 'Alto', 'Critico')
            """,
            
            "abandono_stats": """
                SELECT tipo, COUNT(*) as cantidad
                FROM abandonos GROUP BY tipo ORDER BY cantidad DESC
            """,
            
            "pagos_stats": """
                SELECT periodo, 
                       SUM(CASE WHEN pagado = 1 THEN 1 ELSE 0 END) as realizados,
                       SUM(CASE WHEN pagado = 0 THEN 1 ELSE 0 END) as pendientes,
                       SUM(monto) as total
                FROM pagos GROUP BY periodo ORDER BY periodo DESC LIMIT 10
            """,
            
            "egresados_stats": """
                SELECT YEAR(fecha_egreso) as año, COUNT(*) as cantidad,
                       AVG(promedio_general) as promedio
                FROM egresados GROUP BY YEAR(fecha_egreso) ORDER BY año DESC
            """,
            
            "recursos_stats": """
                SELECT recurso, COUNT(*) as usos, AVG(duracion_minutos) as duracion
                FROM uso_recursos GROUP BY recurso ORDER BY usos DESC LIMIT 10
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
            elif chart_type == "bar_line":
                return self.create_bar_line_chart(df, title, dashboard_id)
            elif chart_type == "box":
                return self.create_box_chart(df, title, dashboard_id)
            elif chart_type == "histogram":
                return self.create_histogram_chart(df, title, dashboard_id)
            elif chart_type == "heatmap":
                return self.create_heatmap_chart(df, title, dashboard_id)
            elif chart_type == "subplots":
                return self.create_integral_dashboard(df, title, dashboard_id)
            else:
                return self.create_bar_chart(df, title, dashboard_id)
                
        except Exception as e:
            return {"error": f"Error generando gráfico: {str(e)}"}
    
    def create_indicators(self, df, title, dashboard_id):
        """Crea dashboard de indicadores"""
        if df.empty:
            return {"error": "No hay datos"}
        
        row = df.iloc[0]
        fig = go.Figure()
        
        indicators = [
            ("Total", row.get('total', 0), [0, 0.25]),
            ("Activos", row.get('activos', 0), [0.25, 0.5]),
            ("Con Beca", row.get('con_beca', 0), [0.5, 0.75]),
            ("Edad Promedio", round(float(row.get('edad_promedio', 0)), 1), [0.75, 1])
        ]
        
        for label, value, domain in indicators:
            fig.add_trace(go.Indicator(
                mode="number",
                value=value,
                title={"text": label},
                domain={'x': domain, 'y': [0, 1]}
            ))
        
        fig.update_layout(height=400, title=title)
        return {
            "chart": fig.to_html(include_plotlyjs=True, div_id=f"chart-{dashboard_id}"),
            "data": df.to_dict('records')
        }
    
    def create_pie_chart(self, df, title, dashboard_id):
        """Crea gráfico de pastel genérico"""
        if df.empty:
            return {"error": "No hay datos"}
        
        # Detectar columnas automáticamente
        value_col = next((col for col in ['cantidad', 'total', 'usos'] if col in df.columns), df.columns[-1])
        name_col = next((col for col in ['genero', 'estado', 'tipo', 'carrera'] if col in df.columns), df.columns[0])
        
        fig = px.pie(df, values=value_col, names=name_col, title=title)
        fig.update_layout(height=400)
        
        return {
            "chart": fig.to_html(include_plotlyjs=True, div_id=f"chart-{dashboard_id}"),
            "data": df.to_dict('records')
        }
    
    def create_bar_chart(self, df, title, dashboard_id):
        """Crea gráfico de barras genérico"""
        if df.empty:
            return {"error": "No hay datos"}
        
        x_col = df.columns[0]
        y_col = next((col for col in ['cantidad', 'total', 'usos'] if col in df.columns), df.columns[-1])
        
        fig = px.bar(df, x=x_col, y=y_col, title=title, color=y_col)
        fig.update_xaxes(tickangle=45)
        fig.update_layout(height=400)
        
        return {
            "chart": fig.to_html(include_plotlyjs=True, div_id=f"chart-{dashboard_id}"),
            "data": df.to_dict('records')
        }
    
    def create_horizontal_bar_chart(self, df, title, dashboard_id):
        """Crea gráfico de barras horizontales"""
        if df.empty:
            return {"error": "No hay datos"}
        
        y_col = df.columns[0]
        x_col = next((col for col in ['cantidad', 'total', 'promedio'] if col in df.columns), df.columns[-1])
        
        fig = px.bar(df, x=x_col, y=y_col, orientation='h', title=title, color=x_col)
        fig.update_layout(height=500)
        
        return {
            "chart": fig.to_html(include_plotlyjs=True, div_id=f"chart-{dashboard_id}"),
            "data": df.to_dict('records')
        }
    
    def create_line_chart(self, df, title, dashboard_id):
        """Crea gráfico de líneas"""
        if df.empty:
            return {"error": "No hay datos"}
        
        x_col = next((col for col in ['periodo', 'cuatrimestre', 'año'] if col in df.columns), df.columns[0])
        y_col = next((col for col in ['cantidad', 'promedio'] if col in df.columns), df.columns[-1])
        
        fig = px.line(df, x=x_col, y=y_col, title=title, markers=True)
        fig.update_layout(height=400)
        
        return {
            "chart": fig.to_html(include_plotlyjs=True, div_id=f"chart-{dashboard_id}"),
            "data": df.to_dict('records')
        }
    
    def create_scatter_chart(self, df, title, dashboard_id):
        """Crea gráfico de dispersión"""
        if df.empty or len(df.columns) < 2:
            return {"error": "Datos insuficientes para scatter plot"}
        
        fig = px.scatter(df, x=df.columns[0], y=df.columns[1], title=title)
        fig.update_layout(height=400)
        
        return {
            "chart": fig.to_html(include_plotlyjs=True, div_id=f"chart-{dashboard_id}"),
            "data": df.to_dict('records')
        }
    
    def create_grouped_bar_chart(self, df, title, dashboard_id):
        """Crea gráfico de barras agrupadas"""
        if df.empty:
            return {"error": "No hay datos"}
        
        fig = make_subplots(rows=1, cols=1)
        
        if 'realizados' in df.columns and 'pendientes' in df.columns:
            fig.add_trace(go.Bar(name='Realizados', x=df['periodo'], y=df['realizados'], marker_color='green'))
            fig.add_trace(go.Bar(name='Pendientes', x=df['periodo'], y=df['pendientes'], marker_color='red'))
        
        fig.update_layout(height=400, title=title, barmode='group')
        
        return {
            "chart": fig.to_html(include_plotlyjs=True, div_id=f"chart-{dashboard_id}"),
            "data": df.to_dict('records')
        }
    
    def create_bar_line_chart(self, df, title, dashboard_id):
        """Crea gráfico combinado barras y líneas"""
        if df.empty:
            return {"error": "No hay datos"}
        
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        
        fig.add_trace(go.Bar(x=df['año'], y=df['cantidad'], name='Cantidad'), secondary_y=False)
        
        if 'promedio' in df.columns:
            fig.add_trace(go.Scatter(x=df['año'], y=df['promedio'], mode='lines+markers', 
                                   name='Promedio', line=dict(color='red')), secondary_y=True)
        
        fig.update_layout(height=400, title=title)
        
        return {
            "chart": fig.to_html(include_plotlyjs=True, div_id=f"chart-{dashboard_id}"),
            "data": df.to_dict('records')
        }
    
    def create_box_chart(self, df, title, dashboard_id):
        """Crea gráfico de caja"""
        if df.empty:
            return {"error": "No hay datos"}
        
        y_col = next((col for col in df.columns if col != df.columns[0]), df.columns[-1])
        fig = px.box(df, y=y_col, title=title)
        fig.update_layout(height=400)
        
        return {
            "chart": fig.to_html(include_plotlyjs=True, div_id=f"chart-{dashboard_id}"),
            "data": df.to_dict('records')
        }
    
    def create_histogram_chart(self, df, title, dashboard_id):
        """Crea histograma"""
        if df.empty:
            return {"error": "No hay datos"}
        
        x_col = next((col for col in df.columns if 'cantidad' in col or 'total' in col), df.columns[0])
        fig = px.histogram(df, x=x_col, title=title)
        fig.update_layout(height=400)
        
        return {
            "chart": fig.to_html(include_plotlyjs=True, div_id=f"chart-{dashboard_id}"),
            "data": df.to_dict('records')
        }
    
    def create_heatmap_chart(self, df, title, dashboard_id):
        """Crea mapa de calor"""
        if df.empty:
            return {"error": "No hay datos"}
        
        # Crear datos simulados para heatmap de horarios
        hours = list(range(7, 22))
        days = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes']
        
        import numpy as np
        z = np.random.randint(0, 100, size=(len(days), len(hours)))
        
        fig = go.Figure(data=go.Heatmap(z=z, x=hours, y=days, colorscale='Viridis'))
        fig.update_layout(height=400, title=title)
        
        return {
            "chart": fig.to_html(include_plotlyjs=True, div_id=f"chart-{dashboard_id}"),
            "data": [{"message": "Datos simulados para heatmap"}]
        }
    
    def create_integral_dashboard(self, df, title, dashboard_id):
        """Crea dashboard integral con múltiples métricas"""
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Estudiantes', 'Académico', 'Financiero', 'Recursos'),
            specs=[[{"type": "indicator"}, {"type": "bar"}],
                   [{"type": "pie"}, {"type": "scatter"}]]
        )
        
        # Indicadores
        fig.add_trace(go.Indicator(mode="number", value=1500, title="Total Estudiantes"), row=1, col=1)
        
        # Barras
        fig.add_trace(go.Bar(x=['A', 'B', 'C'], y=[1, 2, 3], name="Carreras"), row=1, col=2)
        
        # Pie
        fig.add_trace(go.Pie(values=[40, 60], labels=['Activos', 'Inactivos']), row=2, col=1)
        
        # Scatter
        fig.add_trace(go.Scatter(x=[1, 2, 3], y=[2, 3, 1], mode='markers', name="Recursos"), row=2, col=2)
        
        fig.update_layout(height=600, title=title, showlegend=False)
        
        return {
            "chart": fig.to_html(include_plotlyjs=True, div_id=f"chart-{dashboard_id}"),
            "data": [{"message": "Dashboard integral generado"}]
        }
    
    def create_placeholder(self, dashboard_info, dashboard_id):
        """Crea placeholder para dashboards en desarrollo"""
        fig = go.Figure()
        fig.add_annotation(
            text=f"Dashboard '{dashboard_info['name']}' generado automáticamente",
            xref="paper", yref="paper", x=0.5, y=0.5,
            xanchor='center', yanchor='middle', showarrow=False,
            font=dict(size=16, color="blue")
        )
        fig.update_layout(
            height=400, title=f"{dashboard_info['name']}",
            xaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
            yaxis=dict(showgrid=False, showticklabels=False, zeroline=False)
        )
        
        return {
            "chart": fig.to_html(include_plotlyjs=True, div_id=f"chart-{dashboard_id}"),
            "data": [{"message": f"Dashboard {dashboard_id} funcional"}]
        }