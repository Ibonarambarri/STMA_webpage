from fastapi import FastAPI, Request, Form, HTTPException, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, List, Dict, Any
import os
import datetime
from pydantic import BaseModel, EmailStr
from dotenv import load_dotenv
import httpx
from starlette.middleware.sessions import SessionMiddleware

# Cargar variables de entorno
load_dotenv()

app = FastAPI(title="STMA Intelligent Solutions")

# Middleware CORS para Vercel
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuración de archivos estáticos y plantillas
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Clave secreta para la sesión
app.add_middleware(
    SessionMiddleware,
    secret_key=os.environ.get('SECRET_KEY', 'clave-secreta-por-defecto'),
    max_age=3600  # 1 hora
)

# Configuración para envío de correos
EMAIL_SERVICE_URL = os.environ.get('EMAIL_SERVICE_URL', '')
EMAIL_API_KEY = os.environ.get('EMAIL_API_KEY', '')

# Lista de correos electrónicos de los miembros de la empresa
DESTINATARIOS = [
    os.environ.get('EMAIL_1', ''),
    os.environ.get('EMAIL_2', ''),
    os.environ.get('EMAIL_3', ''),
    os.environ.get('EMAIL_4', '')
]

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
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    request.state.current_year = get_current_year()
    request.state.empresa = empresa_info
    response = await call_next(request)
    return response


# Modelos de datos para el formulario de contacto
class ContactForm(BaseModel):
    nombre: str
    email: EmailStr
    empresa: Optional[str] = None
    telefono: Optional[str] = None
    asunto: str
    mensaje: str
    privacidad: bool


# Función para enviar correo (usando servicio externo)
async def enviar_correo(asunto: str, destinatarios: List[str], contenido: str, remitente: str):
    if not EMAIL_SERVICE_URL:
        # Solo para desarrollo - simulamos el envío
        print(f"Correo enviado a {destinatarios}")
        print(f"Asunto: {asunto}")
        print(f"Contenido: {contenido}")
        return True

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                EMAIL_SERVICE_URL,
                json={
                    "api_key": EMAIL_API_KEY,
                    "to": destinatarios,
                    "subject": asunto,
                    "text": contenido,
                    "from": remitente
                }
            )
            return response.status_code == 200
    except Exception as e:
        print(f"Error al enviar correo: {str(e)}")
        return False


# Rutas de la aplicación
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "proyectos": proyectos[:3]}
    )


@app.get("/nosotros", response_class=HTMLResponse)
async def nosotros(request: Request):
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
    return templates.TemplateResponse(
        "nosotros.html",
        {"request": request, "equipo": equipo}
    )


@app.get("/proyectos", response_class=HTMLResponse)
async def ver_proyectos(request: Request):
    return templates.TemplateResponse(
        "proyectos.html",
        {"request": request, "proyectos": proyectos}
    )


@app.get("/proyecto/{proyecto_id}", response_class=HTMLResponse)
async def detalle_proyecto(request: Request, proyecto_id: int):
    proyecto = next((p for p in proyectos if p['id'] == proyecto_id), None)
    if not proyecto:
        return RedirectResponse(url="/proyectos")

    return templates.TemplateResponse(
        "detalle_proyecto.html",
        {"request": request, "proyecto": proyecto, "proyectos": proyectos}
    )


@app.get("/servicios", response_class=HTMLResponse)
async def servicios(request: Request):
    return templates.TemplateResponse(
        "servicios.html",
        {"request": request}
    )


@app.get("/contacto", response_class=HTMLResponse)
async def contacto_get(request: Request):
    return templates.TemplateResponse(
        "contacto.html",
        {"request": request}
    )


@app.post("/contacto", response_class=HTMLResponse)
async def contacto_post(
        request: Request,
        nombre: str = Form(...),
        email: str = Form(...),
        empresa: Optional[str] = Form(None),
        telefono: Optional[str] = Form(None),
        asunto: str = Form(...),
        mensaje: str = Form(...),
        privacidad: bool = Form(...)
):
    # Validación básica
    if not all([nombre, email, asunto, mensaje, privacidad]):
        return templates.TemplateResponse(
            "contacto.html",
            {
                "request": request,
                "error": "Por favor, rellena todos los campos obligatorios."
            }
        )

    try:
        # Creación del contenido del mensaje
        contenido = f"""
Nuevo mensaje desde el formulario de contacto:

Nombre: {nombre}
Email: {email}
Empresa: {empresa if empresa else 'No especificada'}
Teléfono: {telefono if telefono else 'No especificado'}

Mensaje:
{mensaje}
        """

        # Envío del mensaje
        exito = await enviar_correo(
            asunto=f"STMA Sitio Web: {asunto}",
            destinatarios=DESTINATARIOS,
            contenido=contenido,
            remitente=email
        )

        if exito:
            return templates.TemplateResponse(
                "contacto.html",
                {
                    "request": request,
                    "success": "¡Mensaje enviado correctamente! Nos pondremos en contacto contigo lo antes posible."
                }
            )
        else:
            return templates.TemplateResponse(
                "contacto.html",
                {
                    "request": request,
                    "error": "Error al enviar el mensaje. Por favor, inténtalo de nuevo más tarde."
                }
            )

    except Exception as e:
        return templates.TemplateResponse(
            "contacto.html",
            {
                "request": request,
                "error": f"Error al enviar el mensaje. Por favor, inténtalo de nuevo más tarde."
            }
        )


# Manejador de error 404
@app.exception_handler(404)
async def pagina_no_encontrada(request: Request, exc):
    return templates.TemplateResponse(
        "404.html",
        {"request": request},
        status_code=404
    )

# Para permitir que Vercel importe el app correctamente
# No necesitamos esto para producción pero lo mantenemos por compatibilidad
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)