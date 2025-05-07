import streamlit as st
import requests
import time
import uuid
from typing import Dict, List
import os
from dotenv import load_dotenv
from PIL import Image # Import Pillow para manejo de imágenes

# Load environment variables
load_dotenv()

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000") # Get API_BASE_URL from env, default to localhost

# Configurar la página
st.set_page_config(
    page_title="Asistente Turístico Pai (Prueba)",
    page_icon="assets/pai_logo_blue.png" if os.path.exists("assets/pai_logo_blue.png") else "🅿️", 
    layout="wide"
)

# ---- Colores de Pai (Adaptados para Tema Oscuro) ----
PAI_BLUE = "#0052FF" 
PAI_DARK_BG_ACCENT = "#1C2A3F" # Un azul muy oscuro para fondos de mensajes de asistente
PAI_TEXT_ON_DARK_BG = "#E1E8F0" # Texto claro para fondos oscuros
USER_MESSAGE_BG_DARK = "#2D2D2D" # Un gris oscuro para mensajes de usuario
TEXT_GENERAL_DARK_THEME = "#FAFAFA" # Texto general brillante para tema oscuro
DISCLAIMER_BG_DARK = "#282828" # Fondo oscuro sutil para disclaimer
DISCLAIMER_TEXT_DARK = "#A0A0A0" # Texto gris medio para disclaimer

# Estilos personalizados
st.markdown(f"""
    <style>
    /* Ajustes generales para asegurar legibilidad en tema oscuro */
    body {{
        color: {TEXT_GENERAL_DARK_THEME};
    }}
    .stApp {{
        /* background-color: #0F172A; */ /* Opcional: si quieres un fondo aún más oscuro y uniforme */
    }}
    .main .block-container {{ 
        padding-top: 1rem;
    }}
    .logo-container {{
        display: flex;
        justify-content: center;
        margin-bottom: 1rem;
    }}
    .logo-container img {{
        max-width: 120px; /* Reducir un poco el logo */
        height: auto;
    }}
    h1 {{
        color: {PAI_BLUE};
        text-align: center;
        margin-top: 0.25rem;
        margin-bottom: 0.75rem; /* Menos espacio después del título */
        font-size: 2.2em; /* Ligeramente más pequeño */
    }}
    /* Disclaimer de prueba */
    .test-disclaimer {{
        text-align: center;
        padding: 0.5rem 1rem;
        background-color: {DISCLAIMER_BG_DARK};
        color: {DISCLAIMER_TEXT_DARK};
        border-radius: 8px;
        margin: 0.5rem auto 1.5rem auto; /* Centrado y con margen */
        border: 1px solid {PAI_BLUE};
        font-size: 0.9em;
        max-width: 80%;
    }}
    /* Lista de capacidades del asistente */
    .capabilities-list ul {{
        list-style-position: inside; 
        padding-left: 0;
    }}
    .capabilities-list li {{
        color: {TEXT_GENERAL_DARK_THEME}; /* Asegurar que el texto de la lista sea visible */
        margin-bottom: 0.3rem;
    }}
    /* Mensajes del Chat */
    .stChatMessage {{
        padding: 0.8rem 1rem;
        border-radius: 8px; /* Bordes más suaves */
        margin-bottom: 1rem;
        border: none; /* Quitar borde genérico si los fondos ya contrastan */
        box-shadow: 0 1px 3px rgba(0,0,0,0.2); /* Sombra sutil */
    }}
    .user-message {{
        background-color: {USER_MESSAGE_BG_DARK};
        color: {TEXT_GENERAL_DARK_THEME};
    }}
    .assistant-message {{
        background-color: {PAI_DARK_BG_ACCENT};
        color: {PAI_TEXT_ON_DARK_BG};
        border-left: 4px solid {PAI_BLUE};
    }}
    /* Paquetes de Viaje (como tarjetas) */
    .travel-package {{
        background-color: {USER_MESSAGE_BG_DARK}; /* Fondo más oscuro para la tarjeta */
        color: {TEXT_GENERAL_DARK_THEME};
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        border: 1px solid {PAI_BLUE}; /* Borde azul Pai */
        box-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }}
    .travel-package h3, .travel-package strong {{
        color: {PAI_BLUE}; /* Acentos azules Pai dentro del paquete */
    }}
    /* Botones de Viaje */
    .travel-button {{
        display: inline-block;
        padding: 0.6rem 1.2rem;
        margin: 0.8rem 0.3rem 0.5rem 0;
        border-radius: 6px;
        background-color: {PAI_BLUE};
        color: white;
        text-align: center;
        text-decoration: none;
        font-size: 0.95em;
        font-weight: bold;
        cursor: pointer;
        border: none;
        transition: background-color 0.2s ease, transform 0.1s ease;
    }}
    .travel-button:hover {{
        background-color: #0045CC; /* Azul más oscuro */
        transform: translateY(-1px);
    }}
    .travel-button-small {{
        display: inline-block;
        padding: 0.4rem 0.8rem;
        margin: 0.4rem 0.3rem 0.3rem 0;
        border-radius: 5px;
        background-color: #4A5568; /* Un gris azulado más oscuro */
        color: white;
        text-align: center;
        text-decoration: none;
        font-size: 0.85em;
        cursor: pointer;
        border: none;
        transition: background-color 0.2s ease, transform 0.1s ease;
    }}
    .travel-button-small:hover {{
        background-color: #3A4352;
        transform: translateY(-1px);
    }}
    </style>
""", unsafe_allow_html=True)

# Mostrar Logo 
logo_path = "assets/pai_logo_blue.png"
if not os.path.exists("assets"):
    os.makedirs("assets")

if os.path.exists(logo_path):
    st.image(logo_path, width=120)
else:
    # Si el logo no está, el título PAI toma más relevancia
    st.markdown(f"<h1 style='text-align:left; font-size: 2.5em; color:{PAI_BLUE};'>Pai</h1>", unsafe_allow_html=True)
    st.warning(f"Advertencia: No se encontró el logo en {logo_path}. Por favor, descarga el logo azul de Pai y guárdalo en la carpeta 'assets' de tu proyecto.")

# Título de la App y Disclaimer
st.title("Asistente Turístico Interactivo") 
st.markdown("<div class='test-disclaimer'>🧪 **Entorno de Prueba**: Este es un chat de demostración para probar casos de uso de agentes IA.</div>", unsafe_allow_html=True)

# Lista de Capacidades (mejorada visualmente)
st.markdown("""
<div class="capabilities-list">

**¡Pregúntame cualquier cosa sobre destinos turísticos! Puedo ayudarte con:**

*   Encontrar lugares turísticos específicos
*   Obtener información detallada sobre destinos
*   Calcular distancias entre lugares
*   Obtener direcciones y rutas
*   Encontrar atracciones cercanas
*   Información sobre el clima y la mejor época para visitar
*   Recomendaciones de hoteles y restaurantes
*   Información sobre actividades y tours disponibles
*   ¡Y ayudarte a reservar tu próxima aventura!

</div>
""", unsafe_allow_html=True)

# Inicializar el historial del chat y el ID de conversación
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": f"¡Hola! Soy tu Asistente Turístico Pai 🅿️. ¿Cómo puedo ayudarte a planificar tu próximo viaje o aventura? 🌍"
        }
    ]
if "conversation_id" not in st.session_state:
    st.session_state.conversation_id = str(uuid.uuid4())

# Mostrar el historial del chat
for message in st.session_state.messages:
    avatar_icon = "🧑‍💻" if message["role"] == "user" else "assets/pai_logo_blue.png" if os.path.exists("assets/pai_logo_blue.png") else "🅿️"
    with st.chat_message(message["role"], avatar=avatar_icon):
        if message["role"] == "assistant":
            st.markdown(message["content"], unsafe_allow_html=True)
        else:
            st.markdown(message["content"])

# Función para obtener respuesta de la API
def get_assistant_response(user_input: str) -> Dict:
    try:
        # Preparar el historial de mensajes para la API
        history = [
            {"role": msg["role"], "content": msg["content"]}
            for msg in st.session_state.messages
        ]
        
        api_url = f"{API_BASE_URL}/query" # Construct the full API URL
        
        response = requests.post(
            api_url,
            json={
                "query": user_input,
                "history": history,
                "conversation_id": st.session_state.conversation_id
            }
        )
        if response.status_code == 200:
            return response.json()
        else:
            return {"response": f"Error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"response": f"Error connecting to the API: {str(e)}"}

# Input del usuario
if prompt := st.chat_input("¿Qué te gustaría saber?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="🧑‍💻"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar=avatar_icon): # Reutilizar avatar_icon definido antes
        message_placeholder = st.empty()
        api_response = get_assistant_response(prompt)
        assistant_response = api_response["response"]
        
        # Simulación de streaming visual para la respuesta completa
        displayed_response = ""
        response_words = assistant_response.split(' ')
        
        for i, word in enumerate(response_words):
            displayed_response += word + " "
            time.sleep(0.03)  # Ajusta la velocidad del "tecleo"
            # Añadir cursor parpadeante solo si no es la última palabra para evitar que quede al final
            cursor = "▌" if i < len(response_words) - 1 else ""
            message_placeholder.markdown(displayed_response + cursor, unsafe_allow_html=True)
        
        # Render final sin cursor
        message_placeholder.markdown(assistant_response, unsafe_allow_html=True)
        
        st.session_state.messages.append({"role": "assistant", "content": assistant_response})
    
    if "conversation_id" in api_response and api_response["conversation_id"]:
        st.session_state.conversation_id = api_response["conversation_id"] 