import requests
import json
import os

def publish_to_make_webhook(text, image_url=None):
    """
    Envía el texto y la URL de la imagen a un webhook de Make.com.
    Make se encargará de publicar en LinkedIn.
    Requiere MAKE_WEBHOOK_URL en el .env.
    """
    webhook_url = os.getenv("MAKE_WEBHOOK_URL")
    
    if not webhook_url:
        print("Falta MAKE_WEBHOOK_URL en el archivo .env.")
        return False
        
    print("Enviando datos a Make.com...")
    
    payload = {
        "text": text,
        "image_url": image_url
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(webhook_url, headers=headers, json=payload)
        response.raise_for_status()
        print("¡Datos enviados a Make exitosamente!")
        return True
    except Exception as e:
        print(f"Error al enviar al webhook: {e}")
        return False

if __name__ == "__main__":
    # Test
    publish_to_make_webhook("Este es un post de prueba generado automáticamente.", "https://ejemplo.com/imagen.jpg")
