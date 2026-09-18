import requests
from bs4 import BeautifulSoup
import warnings
from bs4 import XMLParsedAsHTMLWarning
import urllib.parse
import re

warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)

DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

def fetch_news_candidates(topic="tecnologia innovacion", count=5):
    """
    Obtiene rápidamente las noticias candidatas del RSS de Google News sin scrapear las páginas completas.
    Devuelve una lista de diccionarios con title, url y text (resumen del RSS).
    """
    query = urllib.parse.quote(topic)
    rss_url = f"https://news.google.com/rss/search?q={query}&hl=es-419&gl=US&ceid=US:es-419"
    
    print(f"Buscando {count} candidatos sobre '{topic}' en Google News RSS...")
    try:
        response = requests.get(rss_url, headers=DEFAULT_HEADERS, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        items = soup.find_all('item')
        
        if not items:
            print("No se encontraron noticias en el RSS.")
            return []
            
        candidates = []
        limit = min(count, len(items))
        
        for i in range(limit):
            item = items[i]
            title = item.title.text if item.title else "Sin Título"
            link = item.link.next_sibling.text if item.link and item.link.next_sibling else (item.link.text if item.link else "")
            description = item.description.text if item.description else ""
            clean_desc = BeautifulSoup(description, "html.parser").get_text()
            
            candidates.append({
                "title": title,
                "url": link,
                "text": clean_desc,
                "image_url": None
            })
            
        return candidates
    except Exception as e:
        print(f"Error al obtener candidatos RSS: {e}")
        return []

def enrich_article(news_item, default_keyword="tech"):
    """
    Toma una noticia seleccionada y extrae el contenido completo y la imagen og:image de su web original.
    """
    if not news_item:
        return None
        
    link = news_item.get("url", "")
    print(f"\nExtrayendo contenido completo e imagen de: {news_item.get('title')}")
    
    fallback_image = f"https://images.unsplash.com/photo-1518770660439-4636190af475?w=800&auto=format&fit=crop&q=60"
    image_url = fallback_image
    article_text = news_item.get("text", "")
    
    if link:
        try:
            article_res = requests.get(link, headers=DEFAULT_HEADERS, timeout=10)
            if article_res.status_code == 200:
                article_soup = BeautifulSoup(article_res.content, 'html.parser')
                
                image_meta = article_soup.find('meta', property='og:image')
                if image_meta and image_meta.get('content'):
                    image_url = image_meta['content']
                    
                paragraphs = article_soup.find_all('p')
                extracted_text = " ".join([p.text for p in paragraphs if len(p.text) > 40])
                if len(extracted_text) > 200:
                    article_text = extracted_text
                    print("Texto completo extraído exitosamente.")
                else:
                    print("Texto demasiado corto, conservando resumen del RSS.")
            else:
                print(f"No se pudo acceder al artículo (Status {article_res.status_code}). Usando resumen del RSS.")
        except Exception as e:
            print(f"No se pudo scrapear el artículo completo ({e}). Usando resumen del RSS.")
            
    news_item["text"] = article_text
    news_item["image_url"] = image_url
    return news_item

def scrape_latest_news(topic="tecnologia innovacion", count=1, select_best=True):
    """
    Busca noticias sobre un tema.
    Si select_best=True y count > 1, pide los candidatos al RSS y utiliza IA para seleccionar
    la noticia más impactante antes de descargar el artículo completo.
    """
    if select_best and count > 1:
        candidates = fetch_news_candidates(topic=topic, count=count)
        if not candidates:
            return None
        from ai_processor import select_most_engaging_news
        best_candidate = select_most_engaging_news(candidates)
        return enrich_article(best_candidate)
        
    candidates = fetch_news_candidates(topic=topic, count=count)
    if not candidates:
        return [] if count > 1 else None
        
    results = [enrich_article(item) for item in candidates]
    return results if count > 1 else results[0]

if __name__ == "__main__":
    # Test
    news = scrape_latest_news()
    if news:
        print(f"\n--- TEST DEL SCRAPER ---")
        print(f"Título: {news['title']}")
        print(f"URL: {news['url']}")
        print(f"Texto (resumen): {news['text'][:300]}...")
        print(f"Imagen URL: {news['image_url']}")
