from flask import Flask, render_template, request, jsonify
from flask_mail import Mail, Message
import psycopg2
import os
from datetime import datetime
import logging

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__, static_url_path='/static', static_folder='static')

# Configuración de Base de Datos
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "proyecto_final")
DB_USER = os.getenv("DB_USER", "admin")
DB_PASSWORD = os.getenv("DB_PASSWORD", "admin123")
LANGUAGE = os.getenv("LANGUAGE", "es")

# Configuración de Correo
MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'True').lower() in ['true', '1', 'yes']
MAIL_USERNAME = os.getenv('MAIL_USERNAME')
MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER', 'noreply@eafit.edu.co')

app.config['MAIL_SERVER'] = MAIL_SERVER
app.config['MAIL_PORT'] = MAIL_PORT
app.config['MAIL_USE_TLS'] = MAIL_USE_TLS
app.config['MAIL_USERNAME'] = MAIL_USERNAME
app.config['MAIL_PASSWORD'] = MAIL_PASSWORD
app.config['MAIL_DEFAULT_SENDER'] = MAIL_DEFAULT_SENDER

# Validar configuración de email
MAIL_CONFIGURED = bool(MAIL_USERNAME and MAIL_PASSWORD)
if not MAIL_CONFIGURED:
    logger.warning("⚠️ ADVERTENCIA: Sistema de email no configurado. Establece MAIL_USERNAME y MAIL_PASSWORD en .env")

mail = Mail(app)

def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

@app.route("/", methods=["GET", "POST"])
def index():
    mensaje = None

    if request.method == "POST":
        nombre = request.form["nombre"]
        comuna = request.form["comuna"]
        carrera = request.form["carrera"]

        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO registros (nombre, comuna, carrera, idioma) VALUES (%s, %s, %s, %s)",
            (nombre, comuna, carrera, LANGUAGE)
        )
        conn.commit()
        cur.close()
        conn.close()

        mensaje = "Registration saved successfully" if LANGUAGE == "en" else "Registro guardado correctamente"

    if LANGUAGE == "en":
        return render_template("index_en.html", mensaje=mensaje)

    return render_template("index_es.html", mensaje=mensaje)

@app.route("/health")
def health():
    return "OK", 200

@app.route("/api/statistics", methods=["GET"])
def get_statistics():
    """Retorna estadísticas de registros por comuna y carrera"""
    try:
        conn = get_connection()
        cur = conn.cursor()
        
        # Contar por comuna
        cur.execute(
            "SELECT comuna, COUNT(*) as cantidad FROM registros GROUP BY comuna ORDER BY comuna"
        )
        communes = {str(row[0]): row[1] for row in cur.fetchall()}
        
        # Contar por carrera
        cur.execute(
            "SELECT carrera, COUNT(*) as cantidad FROM registros GROUP BY carrera ORDER BY carrera"
        )
        careers = {row[0]: row[1] for row in cur.fetchall()}
        
        # Total de registros
        cur.execute("SELECT COUNT(*) FROM registros")
        total = cur.fetchone()[0]
        
        cur.close()
        conn.close()
        
        return jsonify({
            'communes': communes,
            'careers': careers,
            'total': total
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route("/admin/panel")
def admin_panel():
    """Panel de administrador con gráficas y opciones"""
    return render_template("admin_panel.html")

@app.route("/admin/send-report", methods=["POST"])
def send_report():
    """Genera y envía reporte de estadísticas por correo"""
    
    # Validar que email esté configurado
    if not MAIL_CONFIGURED:
        logger.error("❌ Email no configurado: MAIL_USERNAME o MAIL_PASSWORD faltante")
        return jsonify({
            'success': False,
            'error': 'Sistema de email no configurado. Contacta al administrador.'
        }), 500
    
    try:
        # Obtener correo del request
        data = request.get_json()
        recipient_email = data.get('email', '').strip() if data else ''
        
        # Validar que el email no esté vacío
        if not recipient_email:
            logger.warning("⚠️ Intento de envío sin email")
            return jsonify({
                'success': False,
                'error': 'El correo electrónico es requerido'
            }), 400
        
        # Validar formato de email
        email_regex = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
        import re
        if not re.match(email_regex, recipient_email):
            logger.warning(f"⚠️ Email inválido: {recipient_email}")
            return jsonify({
                'success': False,
                'error': 'Formato de correo electrónico inválido'
            }), 400

        logger.info(f"📧 Iniciando envío de reporte a: {recipient_email}")
        
        conn = get_connection()
        cur = conn.cursor()
        
        # Obtener estadísticas
        cur.execute("SELECT COUNT(*) FROM registros")
        total_registros = cur.fetchone()[0]
        
        logger.info(f"📊 Total de registros: {total_registros}")
        
        # Por comuna
        cur.execute(
            "SELECT comuna, COUNT(*) as cantidad FROM registros GROUP BY comuna ORDER BY comuna"
        )
        communes_data = cur.fetchall()
        
        # Por carrera
        cur.execute(
            "SELECT carrera, COUNT(*) as cantidad FROM registros GROUP BY carrera ORDER BY carrera"
        )
        careers_data = cur.fetchall()
        
        cur.close()
        conn.close()
        
        # Generar tabla HTML de comunas
        communes_html = ""
        if communes_data:
            for comuna, cantidad in communes_data:
                communes_html += f"<tr><td>Comuna {comuna}</td><td>{cantidad}</td></tr>"
        else:
            communes_html = "<tr><td colspan='2' style='text-align:center; color:#999;'>Sin registros</td></tr>"
        
        # Generar tabla HTML de carreras
        careers_html = ""
        if careers_data:
            for carrera, cantidad in careers_data:
                careers_html += f"<tr><td>{carrera}</td><td>{cantidad}</td></tr>"
        else:
            careers_html = "<tr><td colspan='2' style='text-align:center; color:#999;'>Sin registros</td></tr>"
        
        # Crear email HTML
        html_content = f"""
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background-color: #f8f9fa;
                    padding: 20px;
                }}
                .container {{
                    background-color: white;
                    border-radius: 8px;
                    padding: 30px;
                    max-width: 600px;
                    margin: 0 auto;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                }}
                h1 {{
                    color: #2c5aa0;
                    border-bottom: 3px solid #2c5aa0;
                    padding-bottom: 10px;
                }}
                h2 {{
                    color: #333;
                    margin-top: 25px;
                    font-size: 18px;
                }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin-top: 10px;
                }}
                th {{
                    background-color: #2c5aa0;
                    color: white;
                    padding: 10px;
                    text-align: left;
                    border: 1px solid #1e3a5f;
                }}
                td {{
                    padding: 10px;
                    border: 1px solid #ddd;
                }}
                tr:nth-child(even) {{
                    background-color: #f8f9fa;
                }}
                .total {{
                    font-weight: bold;
                    background-color: #e8f0f8;
                    color: #2c5aa0;
                    padding: 15px;
                    border-radius: 5px;
                    margin: 20px 0;
                }}
                .footer {{
                    margin-top: 20px;
                    font-size: 12px;
                    color: #666;
                    border-top: 1px solid #ddd;
                    padding-top: 10px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>📊 Reporte de Registros EAFIT</h1>
                <p><strong>Fecha:</strong> {datetime.now().strftime('%d de %B de %Y a las %H:%M')}</p>
                
                <div class="total">
                    <p>📈 <strong>Total de Registros:</strong> {total_registros}</p>
                </div>
                
                <h2>📍 Registros por Comuna</h2>
                <table>
                    <thead>
                        <tr>
                            <th>Comuna</th>
                            <th>Cantidad</th>
                        </tr>
                    </thead>
                    <tbody>
                        {communes_html}
                    </tbody>
                </table>
                
                <h2>🎓 Registros por Carrera</h2>
                <table>
                    <thead>
                        <tr>
                            <th>Carrera</th>
                            <th>Cantidad</th>
                        </tr>
                    </thead>
                    <tbody>
                        {careers_html}
                    </tbody>
                </table>
                
                <div class="footer">
                    <p>Este es un reporte automático del sistema de registros EAFIT.</p>
                    <p>Proyecto Final - Internet: Arquitectura y Protocolos</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        logger.info(f"📝 Generando HTML del reporte...")
        
        # Enviar correo
        try:
            msg = Message(
                subject='📊 Reporte de Registros EAFIT',
                recipients=[recipient_email],
                html=html_content
            )
            
            mail.send(msg)
            logger.info(f"✅ Reporte enviado exitosamente a: {recipient_email}")
            
            return jsonify({
                'success': True,
                'message': f'Reporte enviado correctamente a {recipient_email}'
            })
            
        except Exception as mail_error:
            error_msg = str(mail_error)
            logger.error(f"❌ Error al enviar correo: {error_msg}")
            
            # Proporcionar mensaje específico según el tipo de error
            if "SMTPAuthenticationError" in error_msg or "login" in error_msg:
                user_msg = "Error de autenticación SMTP. Verifica las credenciales de email en .env"
            elif "SMTPServerDisconnected" in error_msg or "Connection" in error_msg:
                user_msg = "Error de conexión al servidor SMTP. Verifica la configuración."
            else:
                user_msg = f"Error al enviar correo: {error_msg}"
            
            return jsonify({
                'success': False,
                'error': user_msg
            }), 500
        
    except Exception as e:
        error_msg = str(e)
        logger.error(f"❌ Error en send_report: {error_msg}")
        return jsonify({
            'success': False,
            'error': f'Error inesperado: {error_msg}'
        }), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
