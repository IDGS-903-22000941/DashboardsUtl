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
            dashboard_data = dashboard_manager.