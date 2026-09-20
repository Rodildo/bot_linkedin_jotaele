# Temas sobre los que el bot busca noticias para comentar.
TOPICOS_TENDENCIA = [
    "vigilancia trabajo remoto",
    "despidos inteligencia artificial",
    "quiebra startups tecnologia",
    "adiccion redes sociales",
    "burnout empleados empresas",
    "estafa cripto tecnologia",
    "descubrimiento cientifico insolito",
]

# Imagen genérica si la noticia no trae ninguna.
FALLBACK_IMAGE_URL = "https://images.unsplash.com/photo-1518770660439-4636190af475?w=800&auto=format&fit=crop&q=60"

# Ventanas horarias "humanas" en las que puede salir cada publicación del día.
# (hora, minuto) de inicio y fin de cada ventana.
MORNING_WINDOW = ((9, 15), (11, 30))
EVENING_WINDOW = ((19, 30), (22, 45))

# Probabilidad de saltarse una ventana ese día (nadie publica 100% de los días a la misma cadencia).
SKIP_PROBABILITY = 0.12
