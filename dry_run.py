import os
import random
from scraper import scrape_latest_news
from ai_processor import generate_post
from image_handler import get_fallback_image, download_image
from dotenv import load_dotenv

load_dotenv()

TOPICOS_TENDENCIA = [
    "ultimos avances tecnologicos y su impacto",
    "descubrimientos cientificos recientes y sorprendentes",
    "tecnologia de consumo y redes sociales",
    "innovacion y ciencia aplicada a la vida diaria",
    "inteligencia artificial y el futuro del trabajo",
    "curiosidades cientificas virales"
]

def run_dry_post():
    topic = random.choice(TOPICOS_TENDENCIA)
    count = 1
    post_type = "broma"
    image_keyword = "news,trend,innovation"

    print(f"--- INICIANDO DRY RUN PARA {post_type.upper()} ---")
    print(f"Tema: {topic}")
    
    # 1. Scrapear la noticia
    print("\n1. Scrapeando noticias...")
    news_data = scrape_latest_news(topic=topic, count=count)
    if not news_data:
        print("No se pudo obtener la noticia. Abortando.")
        return
        
    combined_text = f"Título: {news_data['title']}\nTexto: {news_data['text']}"
    image_url = news_data.get('image_url')
    print(f"Noticia obtenida: {news_data['title']}")
    
    # 2. Procesar con IA
    print("\n2. Generando post con IA (Gemini)...")
    enriched_post = generate_post(combined_text, post_type=post_type)
    if not enriched_post:
        print("No se pudo generar el texto con IA. Abortando.")
        return
        
    # 3. Manejar la Imagen
    if not image_url:
        image_url = f"https://source.unsplash.com/800x600/?{image_keyword}"

    print("\n--- RESULTADO FINAL (OFFLINE) ---")
    print(f"URL de imagen a usar: {image_url}\n")
    print("Contenido del Post:")
    print("--------------------------------------------------")
    print(enriched_post)
    print("--------------------------------------------------")

if __name__ == "__main__":
    run_dry_post()
