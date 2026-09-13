import os
import random
from google import genai
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

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
        "muy breve y directo (máximo 1 o 2 párrafos).",
        "de longitud media (unos 3 párrafos).",
        "un poco más largo y analítico (4 o 5 párrafos)."
    ]
    chosen_length = random.choice(lengths)
    
    if post_type == "curiosidad":
        prompt = f"""
        Eres un experto de la industria petrolera que comparte contenido interesante en LinkedIn.
        A continuación te paso una noticia reciente.
        
        Tu tarea es escribir el "Dato Curioso del Día".
        Extrae un dato curioso, histórico o estadístico relacionado con el tema de la noticia.
        
        REGLAS:
        1. INICIA EL POST con algo como "El Dato Curioso del Día:" o similar.
        2. EL TONO debe ser humano, muy simple de entender, y buscando crear un poco de polémica o debate.
        3. ESTÁ ESTRICTAMENTE PROHIBIDO HABLAR DE POLÍTICA.
        4. LONGITUD REQUERIDA: El post debe ser {chosen_length}
        5. Termina con una reflexión o pregunta abierta para generar polémica sana en los comentarios.
        
        TEXTO DE LA NOTICIA:
        {news_text}
        
        POST DE LINKEDIN:
        """
    elif post_type == "pregunta":
        prompt = f"""
        Eres un analista provocador en LinkedIn. A continuación te paso un resumen de varias noticias sobre la economía de Venezuela.
        
        Tu tarea es lanzar la "Pregunta del Día".
        
        REGLAS:
        1. Analiza las noticias proporcionadas.
        2. Formula una pregunta altamente polémica y muy actual que invite al debate profundo en los comentarios.
        3. EL TONO debe ser directo, en vogue y retador, pero humano.
        4. ESTÁ ESTRICTAMENTE PROHIBIDO HABLAR DE POLÍTICA. Enfócate en economía, mercado, innovación o negocios.
        5. LONGITUD REQUERIDA: El post debe ser breve, directo, máximo 2 párrafos antes de lanzar la gran pregunta.
        
        TEXTO DE LAS NOTICIAS:
        {news_text}
        
        POST DE LINKEDIN:
        """
    else: # opinion
        prompt = f"""
        Eres un analista experto de la industria petrolera que comparte análisis en LinkedIn.
        A continuación te paso una noticia reciente del sector petrolero.
        
        Tu tarea es escribir la "Opinión del Día", un post de LinkedIn que parta directamente analizando esta noticia, y luego des tu opinión experta al respecto.
        
        REGLAS:
        1. INICIA EL POST mencionando de forma clara la noticia. Que la noticia sea la base objetiva de tu opinión.
        2. EL TONO debe ser FORMAL y PROFESIONAL, pero con un LENGUAJE SIMPLE Y DIRECTO. No uses palabras rebuscadas, raras o demasiado complejas. Escribe de manera que cualquier persona pueda entender tu punto fácilmente.
        3. MANTÉN EL TOQUE POLÉMICO: Cuestiona de forma inteligente las decisiones de las empresas o el rumbo de la industria, pero siempre con altura.
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
    sample_news = "La empresa XYZ anuncia que reducirá su producción de barriles diarios en un 10% debido a problemas de logística interna y falta de inversión en innovación, enfocándose en mantener márgenes de ganancia a corto plazo en lugar de crecimiento a largo plazo."
    post = generate_post(sample_news, "opinion")
    print("\n--- POST GENERADO ---")
    print(post)
