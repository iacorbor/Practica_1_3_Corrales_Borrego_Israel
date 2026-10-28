# Extracción de Datos de Bluesky y Análisis con Gemini API

Este proyecto extrae datos no estructurados (publicaciones y biografía) de un perfil de Bluesky mediante su SDK oficial, los almacena en una base de datos MongoDB local y realiza un análisis temático y de sentimiento utilizando la API de Google Gemini.

## Características Principales
- Autenticación segura mediante variables de entorno (`.env`).
- Extracción de publicaciones y biografía de perfiles de Bluesky con `atproto`.
- Almacenamiento inicial y actualizado de documentos no estructurados en MongoDB.
- Análisis del contenido recopilado mediante modelos de lenguaje (Google Gemini).
- Exportación automática del análisis a un archivo `.txt` y del documento completo a un archivo `.json`.

## Tecnologías Utilizadas
- **Lenguaje:** Python 3.12+
- **Gestor de entorno y paquetes:** `uv`
- **Librerías principales:**
  - `atproto`: SDK oficial de Bluesky.
  - `google-genai`: SDK de Google Gemini.
  - `pymongo`: Conector para MongoDB.
  - `python-dotenv`: Gestión de variables de entorno.

## Requisitos Previos
- Python instalado en el sistema.
- Gestor de paquetes `uv` instalado.
- Instancia activa de MongoDB ejecutándose en local (`localhost:27017`).
- Cuenta en Bluesky y contraseña de aplicación generada.
- API Key activa de Google Gemini Studio.

## Instalación y Configuración

1. **Clonar el repositorio:**
   ```bash
   git clone <URL_DE_TU_REPOSITYORIO>
   cd <NOMBRE_DE_LA_CARPETA>
