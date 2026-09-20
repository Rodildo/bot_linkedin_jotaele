import random

from dotenv import load_dotenv

from config import TOPICOS_TENDENCIA
from poster import build_post

load_dotenv()


def run_dry_post():
    topic = random.choice(TOPICOS_TENDENCIA)
    print(f"--- DRY RUN (no se publica nada) ---\nTema: {topic}\n")

    text, image_url = build_post(topic=topic, count=5, post_type="normal")
    if not text:
        return

    print("\n--- RESULTADO ---")
    print(f"Imagen: {image_url}\n")
    print("Contenido del post:")
    print("-" * 50)
    print(text)
    print("-" * 50)


if __name__ == "__main__":
    run_dry_post()
