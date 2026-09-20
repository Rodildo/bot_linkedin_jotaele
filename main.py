import random

from config import TOPICOS_TENDENCIA
from poster import create_and_publish_post
from scheduler import run_forever


def run_normal_post():
    topic = random.choice(TOPICOS_TENDENCIA)
    create_and_publish_post(topic=topic, count=5, post_type="normal")


if __name__ == "__main__":
    print("Iniciando el bot de LinkedIn...")
    print("El horario de publicación se recalcula cada día con variación aleatoria.\n")
    run_forever(run_normal_post)
