import requests
import os

def download_image(image_url, save_path="temp_image.jpg"):
    """
    Descarga la imagen de la URL proporcionada y la guarda localmente.
    """
    if not image_url:
        print("No hay URL de imagen para descargar.")
        return None
        
    print(f"Descargando imagen desde: {image_url}...")
    try:
        response = requests.get(image_url, stream=True)
        response.raise_for_status()
        
        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
                
        print(f"Imagen guardada en {save_path}")
        return save_path
    except Exception as e:
        print(f"Error al descargar la imagen: {e}")
        return None

def get_fallback_image(save_path="temp_image.jpg"):
    """
    Si la noticia no tiene imagen, podemos descargar una imagen genérica de petróleo de Unsplash.
    """
    print("Obteniendo imagen genérica de respaldo...")
    # Usando Unsplash Source API para una imagen aleatoria relacionada con "oil rig"
    url = "https://source.unsplash.com/800x600/?oil,rig,petroleum"
    return download_image(url, save_path)
