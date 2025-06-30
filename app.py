from flask import Flask, render_template, request, jsonify
from config import Config
from database import Database
from dashboards.dashboard_definitions import DashboardManager
import json

app = Flask(__name__)
app.config.from_object(Config)

# Inicializar base de datos y dashboard manager
db = Database()
dashboard_manager = DashboardManager(db)

@app.route('/')
def index():
    # Obtener filtros de la URL
    filters = {}
    if request.args.get('carrera'):
        filters['carrera'] = request.args.get('carrera')
    if request.args.get('periodo'):
        filters['periodo'] = request.args.get('periodo')
    if request.args.get('genero'):
        filters['genero'] = request.args.get('genero')
    
    # Generar todos los dashboards implementados
    all_dashboards = []
    implemented_dashboards = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 21, 23, 26, 31, 36]
    
    for dashboard_id in implemented_dashboards:
        dashboard_info = next((d for d in dashboard_manager.dashboards if d["id"] == dashboard_id), None)
        if dashboard_info:
            dashboard_data = dashboard_manager.generate_dashboard(dashboard_id, filters)
            all_dashboards.append({
                'info': dashboard_info,
                'data': dashboard_data
            })
    
    return render_template('unified_dashboard.html', 
                         all_dashboards=all_dashboards,
                         filters=filters)

@app.route('/api/filters')
def get_filters():
    # Obtener opciones para los filtros
    carreras_query = "SELECT DISTINCT codigo, nombre FROM carreras WHERE activa = 1"
    carreras = db.execute_query(carreras_query)
    
    periodos_query = "SELECT DISTINCT periodo_ingreso FROM estudiantes WHERE periodo_ingreso IS NOT NULL"
    periodos = db.execute_query(periodos_query)
    
    generos_query = "SELECT DISTINCT genero FROM estudiantes WHERE genero IS NOT NULL"
    generos = db.execute_query(generos_query)
    
    return jsonify({
        'carreras': carreras,
        'periodos': periodos,
        'generos': generos
    })

if __name__ == '__main__':
    app.run(debug=True)