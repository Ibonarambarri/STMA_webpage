from flask import Flask, render_template, request, flash, redirect, url_for
from flask_mail import Mail, Message
import os
import datetime
from dotenv import load_dotenv

# Cargar variables de entorno desde un archivo .env
load_dotenv()

app = Flask(__name__)

# Configuración de la app
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'clave-secreta-por-defecto')

# Configuración del servidor de correo
app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS', 'True').lower() in ['true', 'yes', '1']
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME', '')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD', '')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER', '')

# Lista de correos electrónicos de los miembros de la empresa
DESTINATARIOS = [
    os.environ.get('EMAIL_1', ''),
    os.environ.get('EMAIL_2', ''),
    os.environ.get('EMAIL_3', ''),
    os.environ.get('EMAIL_4', '')
]

mail = Mail(app)

# Datos para la página principal
empresa_info = {
    'nombre': 'STMA Intelligent Solutions',
    'descripcion': 'Consultoría informática especializada para empresas de todos los tamaños',
    'mision': 'Proporcionar soluciones tecnológicas innovadoras y eficientes para ayudar a nuestros clientes a alcanzar sus objetivos de negocio',
    'servicios': [
        {
            'titulo': 'Consultoría Estratégica',
            'descripcion': 'Analizamos tu infraestructura actual y proponemos mejoras alineadas con tus objetivos empresariales'
        },
        {
            'titulo': 'Desarrollo de Software a Medida',
            'descripcion': 'Creamos aplicaciones personalizadas que se adaptan perfectamente a las necesidades específicas de tu negocio'
        },
        {
            'titulo': 'Ciberseguridad',
            'descripcion': 'Protegemos tus activos digitales con soluciones de seguridad avanzadas y planes de contingencia'
        },
        {
            'titulo': 'Transformación Digital',
            'descripcion': 'Te acompañamos en el proceso de modernización tecnológica para aumentar tu competitividad en el mercado'
        }
    ]
}

# Datos de proyectos (ejemplos)
proyectos = [
    {
        'id': 1,
        'cliente': 'Empresa de Logística',
        'titulo': 'Sistema de Gestión de Flotas',
        'descripcion': 'Desarrollo e implementación de un sistema integral para monitorizar y optimizar la gestión de una flota de 50 vehículos en tiempo real.',
        'tecnologias': ['Python', 'Django', 'React', 'PostgreSQL', 'Docker'],
        'imagen': 'proyecto1.jpg',
    },
    {
        'id': 2,
        'cliente': 'Clínica Médica',
        'titulo': 'Plataforma de Telemedicina',
        'descripcion': 'Diseño y desarrollo de una plataforma de telemedicina segura para permitir consultas médicas virtuales y gestión de expedientes electrónicos.',
        'tecnologias': ['Node.js', 'Express', 'MongoDB', 'WebRTC', 'AWS'],
        'imagen': 'proyecto2.jpg',
    },
    {
        'id': 3,
        'cliente': 'Minorista con Múltiples Sucursales',
        'titulo': 'Migración a Infraestructura Cloud',
        'descripcion': 'Migración completa de infraestructura local a soluciones cloud, optimizando costes y mejorando la escalabilidad y seguridad.',
        'tecnologias': ['Azure', 'Terraform', 'Kubernetes', 'CI/CD', 'Monitoring'],
        'imagen': 'proyecto3.jpg',
    }
]


# Función para obtener el año actual
def get_current_year():
    return datetime.datetime.now().year


# Contexto global para todas las plantillas
@app.context_processor
def inject_current_year():
    return {'current_year': get_current_year()}


# Rutas de la aplicación
@app.route('/')
def index():
    return render_template('index.html', empresa=empresa_info, proyectos=proyectos[:3])


@app.route('/nosotros')
def nosotros():
    equipo = [
        {
            'nombre': 'Socio 1',
            'cargo': 'Director Tecnológico',
            'bio': 'Experto en arquitectura de sistemas y soluciones cloud con más de 10 años de experiencia.',
            'imagen': 'socio1.jpg'
        },
        {
            'nombre': 'Socio 2',
            'cargo': 'Director de Desarrollo',
            'bio': 'Especialista en desarrollo de software empresarial y metodologías ágiles.',
            'imagen': 'socio2.jpg'
        },
        {
            'nombre': 'Socio 3',
            'cargo': 'Director de Seguridad',
            'bio': 'Consultor en ciberseguridad con certificaciones en CISSP y auditoría de sistemas.',
            'imagen': 'socio3.jpg'
        },
        {
            'nombre': 'Socio 4',
            'cargo': 'Director de Operaciones',
            'bio': 'Experto en optimización de procesos y transformación digital de negocios.',
            'imagen': 'socio4.jpg'
        }
    ]
    return render_template('nosotros.html', empresa=empresa_info, equipo=equipo)


@app.route('/proyectos')
def ver_proyectos():
    return render_template('proyectos.html', empresa=empresa_info, proyectos=proyectos)


@app.route('/proyecto/<int:proyecto_id>')
def detalle_proyecto(proyecto_id):
    proyecto = next((p for p in proyectos if p['id'] == proyecto_id), None)
    if proyecto:
        return render_template('detalle_proyecto.html', empresa=empresa_info, proyecto=proyecto)
    return redirect(url_for('ver_proyectos'))


@app.route('/servicios')
def servicios():
    return render_template('servicios.html', empresa=empresa_info)


@app.route('/contacto', methods=['GET', 'POST'])
def contacto():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        email = request.form.get('email')
        empresa = request.form.get('empresa')
        telefono = request.form.get('telefono')
        asunto = request.form.get('asunto')
        mensaje = request.form.get('mensaje')

        # Validación básica
        if not all([nombre, email, asunto, mensaje]):
            flash('Por favor, rellena todos los campos obligatorios.', 'error')
        else:
            try:
                # Creación del mensaje
                msg = Message(
                    subject=f"STMA Sitio Web: {asunto}",
                    recipients=DESTINATARIOS,
                    body=f"""
Nuevo mensaje desde el formulario de contacto:

Nombre: {nombre}
Email: {email}
Empresa: {empresa}
Teléfono: {telefono}

Mensaje:
{mensaje}
                    """,
                    reply_to=email
                )

                # Envío del mensaje
                mail.send(msg)

                flash('¡Mensaje enviado correctamente! Nos pondremos en contacto contigo lo antes posible.', 'success')
                return redirect(url_for('contacto'))

            except Exception as e:
                flash(f'Error al enviar el mensaje. Por favor, inténtalo de nuevo más tarde.', 'error')
                app.logger.error(f"Error de envío de email: {str(e)}")

    return render_template('contacto.html', empresa=empresa_info)


# Manejador de error 404
@app.errorhandler(404)
def pagina_no_encontrada(e):
    return render_template('404.html', empresa=empresa_info), 404


if __name__ == '__main__':
    app.run(debug=True)