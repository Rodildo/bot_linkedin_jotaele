from scraper import scrape_latest_news
from ai_processor import generate_post
from image_handler import get_fallback_image, download_image
from linkedin_publisher import publish_to_make_webhook
import time
import schedule

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

def run_dato_curioso():
    base_run(topic="petroleo venezuela", count=1, post_type="curiosidad", image_keyword="oil,history")

def run_opinion():
    base_run(topic="petroleo venezuela", count=1, post_type="opinion", image_keyword="oil,rig,petroleum")

def run_pregunta():
    base_run(topic="economia venezuela", count=3, post_type="pregunta", image_keyword="venezuela,economy,caracas")

if __name__ == "__main__":
    print("Iniciando programador del Bot...")
    
    # Programamos la tarea para que se repita todos los días a horas específicas
    schedule.every().day.at("09:00").do(run_dato_curioso)
    schedule.every().day.at("14:00").do(run_opinion)
    schedule.every().day.at("19:00").do(run_pregunta)
    
    print("Programación automática establecida:")
    print("- 09:00 -> Dato Curioso")
    print("- 14:00 -> Opinión")
    print("- 19:00 -> Pregunta del Día")
    
    # Bucle infinito para mantener el script ejecutándose en el servidor
    while True:
        schedule.run_pending()
        time.sleep(60) # Revisamos cada 60 segundos si es momento de publicar
