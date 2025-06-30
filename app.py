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
    
    # Generar TODOS los 40 dashboards
    all_dashboards = []
    
    # Iterar por todos los dashboards definidos (1-40)
    for dashboard_info in dashboard_manager.dashboards:
        dashboard_id = dashboard_info["id"]
        
        try:
            dashboard_data = dashboard_manager.generate_dashboard(dashboard_id, filters)
            
            if dashboard_data:
                all_dashboards.append({
                    "info": dashboard_info,
                    "data": dashboard_data
                })
            else:
                # Si no hay datos, crear un placeholder
                all_dashboards.append({
                    "info": dashboard_info,
                    "data": {"error": f"No se pudieron cargar los datos para {dashboard_info['name']}"}
                })
                
        except Exception as e:
            # Manejo de errores por dashboard individual
            all_dashboards.append({
                "info": dashboard_info,
                "data": {"error": f"Error en {dashboard_info['name']}: {str(e)}"}
            })
    
    return render_template('unified_dashboard.html', 
                         all_dashboards=all_dashboards,
                         filters=filters)

@app.route('/api/filters')
def get_filters():
    """API endpoint para obtener opciones de filtros"""
    try:
        # Obtener carreras activas
        carreras_query = """
        SELECT DISTINCT codigo, nombre 
        FROM carreras 
        WHERE activa = 1 
        ORDER BY nombre
        """
        carreras = db.execute_query(carreras_query)
        
        # Obtener períodos únicos
        periodos_query = """
        SELECT DISTINCT periodo_ingreso 
        FROM estudiantes 
        WHERE periodo_ingreso IS NOT NULL 
        ORDER BY periodo_ingreso DESC
        """
        periodos = db.execute_query(periodos_query)
        
        # Obtener géneros únicos
        generos_query = """
        SELECT DISTINCT genero 
        FROM estudiantes 
        WHERE genero IS NOT NULL 
        ORDER BY genero
        """
        generos = db.execute_query(generos_query)
        
        return jsonify({
            "carreras": carreras,
            "periodos": periodos,
            "generos": generos
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/dashboard/<int:dashboard_id>')
def single_dashboard(dashboard_id):
    """Endpoint para un dashboard individual"""
    filters = {}
    if request.args.get('carrera'):
        filters['carrera'] = request.args.get('carrera')
    if request.args.get('periodo'):
        filters['periodo'] = request.args.get('periodo')
    if request.args.get('genero'):
        filters['genero'] = request.args.get('genero')
    
    try:
        dashboard_info = next((d for d in dashboard_manager.dashboards if d["id"] == dashboard_id), None)
        if not dashboard_info:
            return jsonify({"error": "Dashboard no encontrado"}), 404
        
        dashboard_data = dashboard_manager.generate_dashboard(dashboard_id, filters)
        
        return jsonify({
            "info": dashboard_info,
            "data": dashboard_data
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/dashboard/<int:dashboard_id>/data')
def get_dashboard_data(dashboard_id):
    """API endpoint para obtener solo los datos de un dashboard"""
    try:
        dashboard_info = next((d for d in dashboard_manager.dashboards if d["id"] == dashboard_id), None)
        if not dashboard_info:
            return jsonify({"error": "Dashboard no encontrado"}), 404
        
        filters = {}
        if request.args.get('carrera'):
            filters['carrera'] = request.args.get('carrera')
        if request.args.get('periodo'):
            filters['periodo'] = request.args.get('periodo')
        if request.args.get('genero'):
            filters['genero'] = request.args.get('genero')
        
        dashboard_data = dashboard_manager.generate_dashboard(dashboard_id, filters)
        
        return jsonify({
            "dashboard_id": dashboard_id,
            "name": dashboard_info["name"],
            "data": dashboard_data.get("data", []) if dashboard_data else []
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/dashboards/list')
def get_dashboards_list():
    """API endpoint para obtener la lista de todos los dashboards"""
    try:
        return jsonify({
            "dashboards": dashboard_manager.dashboards,
            "total": len(dashboard_manager.dashboards)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/stats/summary')
def get_summary_stats():
    """API endpoint para estadísticas generales del sistema"""
    try:
        # Estadísticas básicas
        stats_query = """
        SELECT 
            (SELECT COUNT(*) FROM estudiantes WHERE activo = 1) as estudiantes_activos,
            (SELECT COUNT(*) FROM carreras WHERE activa = 1) as carreras_activas,
            (SELECT COUNT(*) FROM calificaciones) as total_calificaciones,
            (SELECT COUNT(*) FROM egresados) as total_egresados,
            (SELECT COUNT(*) FROM estudiantes WHERE beca = 1) as estudiantes_con_beca
        """
        
        result = db.execute_query(stats_query)
        
        if result:
            return jsonify({
                "summary": result[0],
                "generated_at": "2024-01-01T00:00:00Z"
            })
        else:
            return jsonify({"error": "No se pudieron obtener las estadísticas"}), 500
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

# Rutas adicionales para navegación
@app.route('/categoria/<category>')
def dashboard_by_category(category):
    """Mostrar dashboards filtrados por categoría"""
    filters = {}
    if request.args.get('carrera'):
        filters['carrera'] = request.args.get('carrera')
    if request.args.get('periodo'):
        filters['periodo'] = request.args.get('periodo')
    if request.args.get('genero'):
        filters['genero'] = request.args.get('genero')
    
    # Filtrar dashboards por categoría
    category_dashboards = [d for d in dashboard_manager.dashboards if d["category"] == category]
    
    all_dashboards = []
    for dashboard_info in category_dashboards:
        dashboard_id = dashboard_info["id"]
        
        try:
            dashboard_data = dashboard_manager.generate_dashboard(dashboard_id, filters)
            
            if dashboard_data:
                all_dashboards.append({
                    "info": dashboard_info,
                    "data": dashboard_data
                })
            else:
                all_dashboards.append({
                    "info": dashboard_info,
                    "data": {"error": f"No se pudieron cargar los datos para {dashboard_info['name']}"}
                })
                
        except Exception as e:
            all_dashboards.append({
                "info": dashboard_info,
                "data": {"error": f"Error en {dashboard_info['name']}: {str(e)}"}
            })
    
    return render_template('unified_dashboard.html', 
                         all_dashboards=all_dashboards,
                         filters=filters,
                         current_category=category)

@app.route('/test-connection')
def test_connection():
    """Endpoint para probar la conexión a la base de datos"""
    try:
        # Prueba simple de conexión
        test_query = "SELECT 1 as test"
        result = db.execute_query(test_query)
        
        if result:
            return jsonify({
                "status": "success",
                "message": "Conexión a la base de datos exitosa",
                "result": result
            })
        else:
            return jsonify({
                "status": "error",
                "message": "No se pudo ejecutar la consulta de prueba"
            }), 500
            
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Error de conexión: {str(e)}"
        }), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)