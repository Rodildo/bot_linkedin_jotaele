import os
import random
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
# Modelo barato y con buena calidad de escritura en OpenRouter.
# Se puede cambiar por otro (ej: "anthropic/claude-3.5-haiku", "deepseek/deepseek-chat") sin tocar el resto del código.
MODEL_NAME = "openai/gpt-4o-mini"

_client = None


def _get_client():
    global _client
    if _client is None:
        _client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=OPENROUTER_API_KEY)
    return _client


def _ask_ai(prompt):
    response = _get_client().chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content.strip()

def load_persona():
    persona_path = os.path.join(os.path.dirname(__file__), 'persona.txt')
    try:
        with open(persona_path, 'r', encoding='utf-8') as f:
            return f.read().strip()
    except Exception:
        return "Eres un experto de la industria que comparte contenido analítico y profesional en LinkedIn."

# Distintas formas de arrancar un post. Se elige una al azar en cada generación
# para que no todos los posts tengan la misma forma (eso es lo que más delata a un bot).
APERTURAS = [
    "Arranca con una afirmación contundente y polémica en la primera línea, sin rodeos ni contexto previo.",
    "Arranca citando el dato o hecho más chocante de la noticia, en tono seco y directo.",
    "Arranca con una pregunta retórica corta que enganche, antes de dar cualquier contexto.",
    "Arranca como si se lo estuvieras contando a alguien en un bar un viernes: casual, sin formalismos de oficina.",
    "Arranca contrastando lo que 'todo el mundo repite' sobre este tema con lo que tú realmente piensas.",
    "Arranca mencionando directamente la noticia y su titular, sin darle más vueltas.",
]

# Cierres que sí terminan en pregunta (para invitar al debate).
CIERRES_CON_PREGUNTA = [
    "Cierra con una pregunta abierta e inteligente que invite a debatir en los comentarios.",
    "Cierra retando directamente al lector a que te contradiga en los comentarios si no está de acuerdo.",
    "Cierra con una pregunta corta y filosa, del estilo '¿o me equivoco?'.",
]

# Cierres que NO terminan en pregunta (no todo post humano termina preguntando algo).
CIERRES_SIN_PREGUNTA = [
    "Cierra con una frase contundente tipo mic-drop, sin hacer ninguna pregunta.",
    "Cierra con una predicción sarcástica sobre hacia dónde va esto.",
    "Cierra con una ironía seca que resuma tu punto, sin necesidad de preguntar nada.",
]


def _elegir_apertura():
    return random.choice(APERTURAS)


def _elegir_cierre(prob_pregunta=0.6):
    pool = CIERRES_CON_PREGUNTA if random.random() < prob_pregunta else CIERRES_SIN_PREGUNTA
    return random.choice(pool)

def select_most_engaging_news(news_items):
    """
    De una lista de noticias candidatas (título y resumen), utiliza Gemini
    para elegir la que tenga mayor tensión, curiosidad, debate o potencial viral,
    descartando notas de prensa aburridas o institucionales.
    """
    if not news_items:
        return None
    if len(news_items) == 1:
        return news_items[0]
        
    if not OPENROUTER_API_KEY:
        print("Aviso: No hay OPENROUTER_API_KEY, seleccionando la primera noticia por defecto.")
        return news_items[0]
        
    print(f"\n[IA] Evaluando {len(news_items)} noticias candidatas con IA para elegir la más emocionante...")
    
    candidates_text = ""
    for idx, item in enumerate(news_items):
        title = item.get('title', 'Sin título')
        snippet = item.get('text', '')[:160].replace('\n', ' ')
        candidates_text += f"[{idx}] Titular: {title}\n    Resumen: {snippet}\n\n"
        
    prompt = f"""
    Eres un editor jefe especializado en publicaciones de alto impacto y debate para LinkedIn.
    
    Evalúa estas {len(news_items)} noticias candidatas:
    {candidates_text}
    
    CRITERIOS DE SELECCIÓN:
    1. Elige la noticia que tenga mayor tensión, curiosidad, sorpresa, dilema ético, fracaso/éxito inesperado o contradicción evidente.
    2. DESCARTA notas de prensa corporativas aburridas, acuerdos comerciales rutinarios o anuncios institucionales vacíos.
    3. Debe enganchar la atención de un profesional en LinkedIn.
    
    RESPONDE ÚNICAMENTE con el número del índice (ejemplo: 0, 1, 2, etc.) de la mejor opción. No agregues texto adicional.
    """
    
    try:
        text_resp = _ask_ai(prompt)
        import re
        match = re.search(r'\d+', text_resp)
        if match:
            idx = int(match.group())
            if 0 <= idx < len(news_items):
                print(f"[IA] Noticia seleccionada como mas impactante [{idx}]: {news_items[idx].get('title')}")
                return news_items[idx]
        print("No se pudo parsear el índice de la respuesta, usando la primera noticia.")
    except Exception as e:
        print(f"Error al evaluar noticias con IA: {e}")
        
    return news_items[0]

def generate_post(news_text, post_type="opinion"):
    """
    Toma el texto de una noticia y utiliza Gemini para generar un post.
    post_type puede ser: "curiosidad", "opinion", o "pregunta".
    """
    if not OPENROUTER_API_KEY:
        print("Error: No se encontró OPENROUTER_API_KEY en las variables de entorno.")
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
    apertura = _elegir_apertura()

    if post_type == "curiosidad":
        cierre = _elegir_cierre(prob_pregunta=0.7)
        prompt = f"""
        PERSONALIDAD DEL BOT:
        {persona}

        A continuación te paso una noticia reciente.
        Tu tarea es escribir el "Dato Curioso del Día" sobre el tema de la noticia.
        Extrae un dato curioso, histórico o estadístico.

        REGLAS:
        1. INICIA EL POST con algo como "El Dato Curioso del Día:" o similar, y luego {apertura[0].lower()}{apertura[1:]}
        2. EL TONO debe seguir estrictamente la PERSONALIDAD DEL BOT definida arriba.
        3. ESTÁ ESTRICTAMENTE PROHIBIDO HABLAR DE POLÍTICA.
        4. LONGITUD REQUERIDA: El post debe ser {chosen_length}
        5. {cierre}

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
        1. Analiza las noticias proporcionadas. Antes de llegar a la pregunta, {apertura[0].lower()}{apertura[1:]}
        2. Formula una pregunta que invite al debate profundo en los comentarios.
        3. EL TONO debe seguir estrictamente la PERSONALIDAD DEL BOT definida arriba.
        4. ESTÁ ESTRICTAMENTE PROHIBIDO HABLAR DE POLÍTICA. Enfócate en economía, mercado, innovación o negocios.
        5. LONGITUD REQUERIDA: El post debe ser breve, directo, máximo 2 párrafos antes de lanzar la gran pregunta.

        TEXTO DE LAS NOTICIAS:
        {news_text}

        POST DE LINKEDIN:
        """
    elif post_type == "normal":
        cierre = _elegir_cierre(prob_pregunta=0.5)
        prompt = f"""
        PERSONALIDAD DEL BOT:
        {persona}

        A continuación te paso una noticia reciente.
        Tu tarea es escribir un post de LinkedIn comentando la noticia de forma natural e interesante.

        REGLAS:
        1. {apertura}
        2. EL TONO debe seguir estrictamente la PERSONALIDAD DEL BOT definida arriba.
        3. ESTÁ ESTRICTAMENTE PROHIBIDO HABLAR DE POLÍTICA.
        4. LONGITUD REQUERIDA: El post debe ser {chosen_length}
        5. {cierre}

        TEXTO DE LA NOTICIA:
        {news_text}

        POST DE LINKEDIN:
        """
    else: # opinion
        cierre = _elegir_cierre(prob_pregunta=0.6)
        prompt = f"""
        PERSONALIDAD DEL BOT:
        {persona}

        A continuación te paso una noticia reciente de la industria.
        Tu tarea es escribir la "Opinión del Día", un post de LinkedIn que parta directamente analizando esta noticia, y luego des tu opinión experta al respecto.

        REGLAS:
        1. INICIA EL POST mencionando de forma clara la noticia (que sea la base objetiva de tu opinión), y hazlo así: {apertura[0].lower()}{apertura[1:]}
        2. EL TONO debe seguir estrictamente la PERSONALIDAD DEL BOT definida arriba.
        3. MANTÉN EL TOQUE POLÉMICO/DEBATE: Cuestiona de forma inteligente las decisiones o el rumbo de la industria, pero siempre con altura.
        4. ESTÁ ESTRICTAMENTE PROHIBIDO HABLAR DE POLÍTICA. Cero menciones a gobiernos, políticos o regulaciones estatales.
        5. LONGITUD REQUERIDA: El post debe ser {chosen_length}
        6. {cierre}

        TEXTO DE LA NOTICIA:
        {news_text}

        POST DE LINKEDIN:
        """
        
    try:
        return _ask_ai(prompt)
    except Exception as e:
        print(f"Error al generar contenido con IA: {e}")
        return None

if __name__ == "__main__":
    # Test
    sample_news = "Un estudio reciente muestra que el 80% de los trabajadores remotos están trabajando más horas que cuando iban a la oficina, sufriendo de agotamiento silencioso porque las empresas miden la productividad por el tiempo de conexión constante y no por los objetivos cumplidos."
    post = generate_post(sample_news, "normal")
    print("\n--- POST GENERADO ---")
    print(post)
