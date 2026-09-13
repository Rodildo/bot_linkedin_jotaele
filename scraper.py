import requests
from bs4 import BeautifulSoup
import warnings
from bs4 import XMLParsedAsHTMLWarning
import urllib.parse
import re

warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)

def scrape_latest_news(topic="petroleo venezuela"):
    """
    Busca la última noticia sobre un tema específico usando Google News RSS.
    Luego intenta extraer el texto del artículo real.
    """
    query = urllib.parse.quote(topic)
    rss_url = f"https://news.google.com/rss/search?q={query}&hl=es-419&gl=US&ceid=US:es-419"
    
    print(f"Buscando noticias sobre '{topic}' en Google News...")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        response = requests.get(rss_url, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        items = soup.find_all('item')
        
        if not items:
            print("No se encontraron noticias en el RSS.")
            return None
            
        # Tomar la primera noticia
        item = items[0]
        title = item.title.text if item.title else "Sin Título"
        link = item.link.next_sibling.text if item.link and item.link.next_sibling else (item.link.text if item.link else "")
        description = item.description.text if item.description else ""
        
        print(f"\nNoticia encontrada: {title}")
        print(f"Enlace: {link}")
        
        # Limpiar el HTML de la descripción para tener texto puro como fallback
        clean_desc = BeautifulSoup(description, "html.parser").get_text()
        article_text = clean_desc
        image_url = "https://source.unsplash.com/800x600/?oil,venezuela,petroleum"
        
        # Intentar scrapear el artículo completo desde el enlace
        try:
            print("Intentando extraer el texto completo del artículo...")
            article_res = requests.get(link, headers=headers, timeout=10)
            if article_res.status_code == 200:
                article_soup = BeautifulSoup(article_res.content, 'html.parser')
                
                # Buscar imagen (og:image)
                image_meta = article_soup.find('meta', property='og:image')
                if image_meta and image_meta.get('content'):
                    image_url = image_meta['content']
                
                # Extraer texto de párrafos
                paragraphs = article_soup.find_all('p')
                extracted_text = " ".join([p.text for p in paragraphs if len(p.text) > 40])
                
                if len(extracted_text) > 200:
                    article_text = extracted_text
                    print("Texto completo extraído exitosamente.")
                else:
                    print("Texto demasiado corto, usando resumen del RSS.")
            else:
                print(f"No se pudo acceder al artículo (Status {article_res.status_code}). Usando resumen del RSS.")
        except Exception as e:
            print(f"No se pudo scrapear el artículo completo ({e}). Usando resumen del RSS.")
        
        return {
            "title": title,
            "url": link,
            "text": article_text,
            "image_url": image_url
        }
            
    except Exception as e:
        print(f"Error general en el scraper: {e}")
        return None

if __name__ == "__main__":
    # Test
    news = scrape_latest_news()
    if news:
        print(f"\n--- TEST DEL SCRAPER ---")
        print(f"Título: {news['title']}")
        print(f"URL: {news['url']}")
        print(f"Texto (resumen): {news['text'][:300]}...")
        print(f"Imagen URL: {news['image_url']}")
