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
    dashboards = dashboard_manager.dashboards
    categories = list(set([d['category'] for d in dashboards]))
    return render_template('index.html', dashboards=dashboards, categories=categories)

@app.route('/dashboard/<int:dashboard_id>')
def dashboard(dashboard_id):
    # Obtener filtros de la URL
    filters = {}
    if request.args.get('carrera'):
        filters['carrera'] = request.args.get('carrera')
    if request.args.get('periodo'):
        filters['periodo'] = request.args.get('periodo')
    if request.args.get('genero'):
        filters['genero'] = request.args.get('genero')
    
    # Generar dashboard
    dashboard_data = dashboard_manager.generate_dashboard(dashboard_id, filters)
    dashboard_info = next((d for d in dashboard_manager.dashboards if d["id"] == dashboard_id), None)
    
    if not dashboard_info:
        return "Dashboard no encontrado", 404
    
    return render_template('dashboard.html', 
                         dashboard=dashboard_info, 
                         dashboard_data=dashboard_data,
                         filters=filters)

@app.route('/api/search')
def search_dashboards():
    query = request.args.get('q', '').lower()
    category = request.args.get('category', '')
    
    dashboards = dashboard_manager.dashboards
    
    # Filtrar por categoría
    if category:
        dashboards = [d for d in dashboards if d['category'] == category]
    
    # Filtrar por búsqueda
    if query:
        dashboards = [d for d in dashboards if 
                     query in d['name'].lower() or 
                     query in d['description'].lower()]
    
    return jsonify(dashboards)

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