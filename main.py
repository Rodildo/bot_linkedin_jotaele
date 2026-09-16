from scraper import scrape_latest_news
from ai_processor import generate_post
from image_handler import get_fallback_image, download_image
from linkedin_publisher import publish_to_make_webhook
import time
import schedule
import random

TOPICOS_TENDENCIA = [
    "ultimos avances tecnologicos y su impacto",
    "descubrimientos cientificos recientes y sorprendentes",
    "tecnologia de consumo y redes sociales",
    "innovacion y ciencia aplicada a la vida diaria",
    "inteligencia artificial y el futuro del trabajo",
    "curiosidades cientificas virales"
]

def base_run(topic, count, post_type, image_keyword):
    print(f"Iniciando Bot de LinkedIn para: {post_type.upper()}...\n")
    
    # 1. Scrapear la noticia
    news_data = scrape_latest_news(topic=topic, count=count)
    if not news_data:
        print("No se pudo obtener la noticia. Abortando.")
        return
        
    # Manejar caso de múltiples noticias (para pregunta)
    if isinstance(news_data, list):
        combined_text = "\n---\n".join([f"Título: {item['title']}\nTexto: {item['text']}" for item in news_data])
        # Usar la imagen de la primera noticia
        image_url = news_data[0].get('image_url') if len(news_data) > 0 else None
        print(f"\n{len(news_data)} noticias obtenidas para procesar.\n")
    else:
        combined_text = f"Título: {news_data['title']}\nTexto: {news_data['text']}"
        image_url = news_data.get('image_url')
        print(f"\nNoticia obtenida: {news_data['title']}\n")
    
    # 2. Procesar con IA
    enriched_post = generate_post(combined_text, post_type=post_type)
    if not enriched_post:
        print("No se pudo generar el texto con IA. Abortando.")
        return
        
    # 3. Manejar la Imagen
    if not image_url:
        image_url = f"https://source.unsplash.com/800x600/?{image_keyword}"
        
    # 4. Enviar a Make.com
    success = publish_to_make_webhook(enriched_post, image_url)
    
    if success:
        print(f"\n¡Bot terminó su ejecución de {post_type} con éxito!")
    else:
        print(f"\nEl bot falló en la etapa de envío al webhook para {post_type}.")

def run_normal_post():
    topic = random.choice(TOPICOS_TENDENCIA)
    base_run(topic=topic, count=1, post_type="normal", image_keyword="news,trend,innovation")

if __name__ == "__main__":
    print("Iniciando programador del Bot...")
    
    # Programamos la tarea para que se repita dos veces al día con 12 horas de diferencia
    schedule.every().day.at("10:00").do(run_normal_post)
    schedule.every().day.at("22:00").do(run_normal_post)
    
    print("Programación automática establecida:")
    print("- 10:00 -> Post Normal")
    print("- 22:00 -> Post Normal")
    
    # Bucle infinito para mantener el script ejecutándose en el servidor
    while True:
        schedule.run_pending()
        time.sleep(60) # Revisamos cada 60 segundos si es momento de publicar
