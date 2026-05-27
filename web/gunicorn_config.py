# Configuración de Gunicorn para Producción
# 
# Ubicación: /proyecto-final-internet/gunicorn_config.py
# Uso: gunicorn -c gunicorn_config.py web-app.app:app

import multiprocessing
import os

# ============================================
# SERVIDOR
# ============================================

# Interfaz y puerto
bind = "0.0.0.0:5000"

# Número de workers (recomendado: 2-4 * num_cores)
workers = multiprocessing.cpu_count() * 2 + 1

# Tipo de worker (sync por defecto, suficiente para Flask)
worker_class = "sync"

# Timeout de worker (segundos)
timeout = 30

# Máximo requests por worker antes de reiniciar (para evitar memory leaks)
max_requests = 1000
max_requests_jitter = 50

# ============================================
# LOGGING
# ============================================

# Archivo de acceso
accesslog = "logs/access.log"

# Archivo de error
errorlog = "logs/error.log"

# Nivel de log (debug, info, warning, error, critical)
loglevel = "info"

# Formato de acceso personalizado
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# ============================================
# RENDIMIENTO
# ============================================

# Buffer size para envío (bytes)
limit_request_line = 4094
limit_request_fields = 100
limit_request_field_size = 8190

# Backlog de conexiones
backlog = 2048

# ============================================
# SEGURIDAD
# ============================================

# Usar header X-Forwarded-For de proxy reverso
x_forwarded_for_header_count = 1
x_forwarded_proto_header_count = 1

# ============================================
# DESARROLLO
# ============================================

# Para desarrollo (comentar en producción)
# reload = True
# reload_extra_files = ['web-app/templates', 'web-app/static']

# ============================================
# HOOKS (Eventos del servidor)
# ============================================

def on_starting(server):
    """Ejecutado cuando el servidor está por iniciar"""
    print("🚀 Gunicorn iniciando...")
    os.makedirs("logs", exist_ok=True)

def when_ready(server):
    """Ejecutado cuando el servidor está listo"""
    print("✅ Gunicorn listo en http://0.0.0.0:5000")

def on_exit(server):
    """Ejecutado cuando el servidor termina"""
    print("🛑 Gunicorn detenido")

def worker_abort(worker):
    """Ejecutado cuando un worker es abortado"""
    print(f"⚠️  Worker {worker.pid} abortado")
