import os
import random
from google import genai
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def load_persona():
    persona_path = os.path.join(os.path.dirname(__file__), 'persona.txt')
    try:
        with open(persona_path, 'r', encoding='utf-8') as f:
            return f.read().strip()
    except Exception:
        return "Eres un experto de la industria que comparte contenido analítico y profesional en LinkedIn."

def generate_post(news_text, post_type="opinion"):
    """
    Toma el texto de una noticia y utiliza Gemini para generar un post.
    post_type puede ser: "curiosidad", "opinion", o "pregunta".
    """
    if not GEMINI_API_KEY:
        print("Error: No se encontró GEMINI_API_KEY en las variables de entorno.")
        return None
        
    print(f"Generando contenido enriquecido con IA para el tipo: {post_type}...")
    
    # Elegir una longitud aleatoria para darle variedad
    lengths = [
        "extremadamente breve y como un dardo (máximo 1 párrafo de 3 o 4 líneas).",
        "muy directo y al grano (máximo 2 párrafos muy cortos).",
        "como un pensamiento rápido (1 párrafo de impacto y 1 reflexión final)."
    ]
    chosen_length = random.choice(lengths)
    
    persona = load_persona()

    if post_type == "curiosidad":
        prompt = f"""
        PERSONALIDAD DEL BOT:
        {persona}
        
        A continuación te paso una noticia reciente.
        Tu tarea es escribir el "Dato Curioso del Día" sobre el tema de la noticia.
        Extrae un dato curioso, histórico o estadístico.
        
        REGLAS:
        1. INICIA EL POST con algo como "El Dato Curioso del Día:" o similar.
        2. EL TONO debe seguir estrictamente la PERSONALIDAD DEL BOT definida arriba.
        3. ESTÁ ESTRICTAMENTE PROHIBIDO HABLAR DE POLÍTICA.
        4. LONGITUD REQUERIDA: El post debe ser {chosen_length}
        5. Termina con una reflexión o pregunta abierta para generar debate sano en los comentarios.
        
        TEXTO DE LA NOTICIA:
        {news_text}
        
        POST DE LINKEDIN:
        """
    elif post_type == "pregunta":
        prompt = f"""
        PERSONALIDAD DEL BOT:
        {persona}
        
        A continuación te paso un resumen de varias noticias actuales.
        Tu tarea es lanzar la "Pregunta del Día".
        
        REGLAS:
        1. Analiza las noticias proporcionadas.
        2. Formula una pregunta que invite al debate profundo en los comentarios.
        3. EL TONO debe seguir estrictamente la PERSONALIDAD DEL BOT definida arriba.
        4. ESTÁ ESTRICTAMENTE PROHIBIDO HABLAR DE POLÍTICA. Enfócate en economía, mercado, innovación o negocios.
        5. LONGITUD REQUERIDA: El post debe ser breve, directo, máximo 2 párrafos antes de lanzar la gran pregunta.
        
        TEXTO DE LAS NOTICIAS:
        {news_text}
        
        POST DE LINKEDIN:
        """
    elif post_type == "normal":
        prompt = f"""
        PERSONALIDAD DEL BOT:
        {persona}
        
        A continuación te paso una noticia reciente.
        Tu tarea es escribir un post de LinkedIn comentando la noticia de forma natural e interesante.
        
        REGLAS:
        1. INICIA EL POST con un gancho atractivo sobre el tema.
        2. EL TONO debe seguir estrictamente la PERSONALIDAD DEL BOT definida arriba.
        3. ESTÁ ESTRICTAMENTE PROHIBIDO HABLAR DE POLÍTICA.
        4. LONGITUD REQUERIDA: El post debe ser {chosen_length}
        5. Cierra el post de manera concisa.
        
        TEXTO DE LA NOTICIA:
        {news_text}
        
        POST DE LINKEDIN:
        """
    else: # opinion
        prompt = f"""
        PERSONALIDAD DEL BOT:
        {persona}
        
        A continuación te paso una noticia reciente de la industria.
        Tu tarea es escribir la "Opinión del Día", un post de LinkedIn que parta directamente analizando esta noticia, y luego des tu opinión experta al respecto.
        
        REGLAS:
        1. INICIA EL POST mencionando de forma clara la noticia. Que la noticia sea la base objetiva de tu opinión.
        2. EL TONO debe seguir estrictamente la PERSONALIDAD DEL BOT definida arriba.
        3. MANTÉN EL TOQUE POLÉMICO/DEBATE: Cuestiona de forma inteligente las decisiones o el rumbo de la industria, pero siempre con altura.
        4. ESTÁ ESTRICTAMENTE PROHIBIDO HABLAR DE POLÍTICA. Cero menciones a gobiernos, políticos o regulaciones estatales.
        5. LONGITUD REQUERIDA: El post debe ser {chosen_length}
        6. Termina SIEMPRE con una pregunta abierta e inteligente que invite a debatir en los comentarios.
        
        TEXTO DE LA NOTICIA:
        {news_text}
        
        POST DE LINKEDIN:
        """
        
    try:
        client = genai.Client(api_key=GEMINI_API_KEY)
        response = client.models.generate_content(
            model='gemini-3.6-flash',
            contents=prompt,
        )
        return response.text.strip()
    except Exception as e:
        print(f"Error al generar contenido con IA: {e}")
        return None

if __name__ == "__main__":
    # Test
    sample_news = "Un estudio reciente muestra que el 80% de los trabajadores remotos están trabajando más horas que cuando iban a la oficina, sufriendo de agotamiento silencioso porque las empresas miden la productividad por el tiempo de conexión constante y no por los objetivos cumplidos."
    post = generate_post(sample_news, "normal")
    print("\n--- POST GENERADO ---")
    print(post)
