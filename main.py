from scraper import scrape_latest_news
from ai_processor import enrich_news
from image_handler import get_fallback_image, download_image
from linkedin_publisher import publish_to_make_webhook
import time
import schedule

def run_bot():
    print("Iniciando Bot de LinkedIn para Noticias Petroleras...\n")
    
    # 1. Scrapear la noticia
    news_data = scrape_latest_news()
    if not news_data:
        print("No se pudo obtener la noticia. Abortando.")
        return
        
    print(f"\nNoticia obtenida: {news_data['title']}\n")
    
    # 2. Procesar con IA
    enriched_post = enrich_news(news_data['text'])
    if not enriched_post:
        print("No se pudo generar el texto con IA. Abortando.")
        return
        
    # 3. Manejar la Imagen (solo necesitamos la URL para Make, no descargarla, 
    # pero para mantener el código simple usaremos la URL original)
    image_url = news_data.get('image_url')
    if not image_url:
        image_url = "https://source.unsplash.com/800x600/?oil,rig,petroleum"
        
    # 4. Enviar a Make.com
    success = publish_to_make_webhook(enriched_post, image_url)
    
    if success:
        print("\n¡Bot terminó su ejecución con éxito!")
    else:
        print("\nEl bot falló en la etapa de envío al webhook.")

if __name__ == "__main__":
    print("Iniciando programador del Bot...")
    print("Esperando 10 minutos para realizar la primera publicación...")
    
    # Pausa de 10 minutos (600 segundos) antes de arrancar por primera vez
    time.sleep(600)
    
    # Ejecutamos la primera publicación
    run_bot()
    
    # Programamos la tarea para que se repita cada 8 horas a partir de este momento
    schedule.every(8).hours.do(run_bot)
    
    print("Programación automática establecida: Publicando cada 8 horas.")
    
    # Bucle infinito para mantener el script ejecutándose en el servidor
    while True:
        schedule.run_pending()
        time.sleep(60) # Revisamos cada 60 segundos si es momento de publicar
