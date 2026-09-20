from scraper import scrape_latest_news
from ai_processor import generate_post
from config import FALLBACK_IMAGE_URL


def build_post(topic, count, post_type):
    """
    Busca noticias y redacta el post con IA, pero no lo publica.
    Devuelve (texto, image_url) o (None, None) si algo falla en el camino.
    """
    print(f"Buscando noticias para un post de tipo '{post_type}'...\n")

    select_best = post_type != "pregunta"
    news_data = scrape_latest_news(topic=topic, count=count, select_best=select_best)
    if not news_data:
        print("No se pudo obtener la noticia.")
        return None, None

    if isinstance(news_data, list):
        combined_text = "\n---\n".join(
            f"Título: {item['title']}\nTexto: {item['text']}" for item in news_data
        )
        image_url = news_data[0].get("image_url") if news_data else None
        print(f"\n{len(news_data)} noticias obtenidas para procesar.\n")
    else:
        combined_text = f"Título: {news_data['title']}\nTexto: {news_data['text']}"
        image_url = news_data.get("image_url")
        print(f"\nNoticia seleccionada: {news_data['title']}\n")

    enriched_post = generate_post(combined_text, post_type=post_type)
    if not enriched_post:
        print("No se pudo generar el texto con IA.")
        return None, None

    return enriched_post, image_url or FALLBACK_IMAGE_URL


def create_and_publish_post(topic, count, post_type):
    """Arma el post con build_post() y lo envía al webhook de Make."""
    from linkedin_publisher import publish_to_make_webhook

    text, image_url = build_post(topic, count, post_type)
    if not text:
        print("Abortando: no se generó contenido para publicar.")
        return False

    success = publish_to_make_webhook(text, image_url)
    if success:
        print(f"\n¡Post de tipo '{post_type}' publicado con éxito!")
    else:
        print(f"\nFalló el envío al webhook para el post de tipo '{post_type}'.")
    return success
