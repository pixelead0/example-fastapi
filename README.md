# Product Management API

API para gestionar productos y categorías, desarrollada con FastAPI y SQLAlchemy.

## Estructura del Proyecto

El proyecto está organizado por dominios, siguiendo los principios de Domain-Driven Design (DDD):

```
src/
├── core/                # Núcleo de la aplicación
│   ├── config.py        # Configuración de la aplicación
│   ├── database.py      # Configuración de la base de datos
│   ├── exceptions.py    # Excepciones base 
│   ├── repository.py    # Repositorio base
│   └── utils.py         # Utilidades comunes
│
├── product/             # Dominio de productos
│   ├── models.py        # Modelos de datos
│   ├── repository.py    # Acceso a datos
│   ├── router.py        # Endpoints de la API
│   ├── schemas.py       # Esquemas de validación
│   ├── service.py       # Lógica de negocio
│   └── exceptions.py    # Excepciones específicas
│
├── category/            # Dominio de categorías
│   ├── models.py        # Modelos de datos
│   ├── repository.py    # Acceso a datos
│   ├── router.py        # Endpoints de la API
│   ├── schemas.py       # Esquemas de validación
│   ├── service.py       # Lógica de negocio
│   └── exceptions.py    # Excepciones específicas
│
├── log/                 # Dominio de logs
│   ├── models.py        # Modelo de datos
│   └── repository.py    # Acceso a datos
│
└── main.py              # Punto de entrada de la aplicación
```

## Tecnologías Utilizadas

- **FastAPI**: Framework web de alto rendimiento
- **SQLAlchemy**: ORM para interactuar con la base de datos
- **Alembic**: Herramienta de migraciones de base de datos
- **Pydantic**: Validación de datos y serialización
- **SQLite**: Base de datos para desarrollo

## Características

- CRUD completo para productos y categorías
- Sistema de registro de operaciones (logs)
- Validación completa de datos de entrada
- Documentación automática con Swagger UI
- Estructura modular y extensible

## Instalación

1. Clonar el repositorio:
   ```bash
   git clone <url-del-repositorio>
   cd <nombre-del-directorio>
   ```

2. Crear un entorno virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

3. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```

4. Crear un archivo `.env` con las variables de entorno necesarias:
   ```
   DATABASE_URL=sqlite+aiosqlite:///./productdb.db
   SECRET_KEY=tu-clave-secreta
   LOG_LEVEL=INFO
   ```

## Migraciones

1. Inicializar las migraciones (solo la primera vez):
   ```bash
   alembic init migrations
   ```

2. Generar una migración:
   ```bash
   alembic revision --autogenerate -m "Mensaje descriptivo"
   ```

3. Aplicar las migraciones:
   ```bash
   alembic upgrade head
   ```

## Ejecución

Para ejecutar la aplicación en modo desarrollo:

```bash
uvicorn src.main:app --reload
```

La documentación de la API estará disponible en:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Arquitectura

Este proyecto sigue una arquitectura por capas dentro de cada dominio:

1. **Modelos** (`models.py`): Definen la estructura de datos y las relaciones en la base de datos.
2. **Repositorios** (`repository.py`): Encapsulan el acceso a la base de datos.
3. **Servicios** (`service.py`): Contienen la lógica de negocio.
4. **Schemas** (`schemas.py`): Definen la estructura de los datos para la API.
5. **Routers** (`router.py`): Definen los endpoints de la API.
6. **Excepciones** (`exceptions.py`): Excepciones específicas del dominio.

## Licencia

Este proyecto está licenciado bajo [insertar licencia]. 