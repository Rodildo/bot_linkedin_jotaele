import datetime
import random
import time

from config import MORNING_WINDOW, EVENING_WINDOW, SKIP_PROBABILITY


def _random_time_today(window):
    (start_h, start_m), (end_h, end_m) = window
    now = datetime.datetime.now()
    start = now.replace(hour=start_h, minute=start_m, second=0, microsecond=0)
    end = now.replace(hour=end_h, minute=end_m, second=0, microsecond=0)
    offset_seconds = random.uniform(0, (end - start).total_seconds())
    return start + datetime.timedelta(seconds=offset_seconds)


def plan_today():
    """
    Arma el horario de publicaciones de hoy: un momento aleatorio dentro de cada
    ventana, saltándose alguna con cierta probabilidad para no ser 100% predecible.
    """
    slots = []
    for window in (MORNING_WINDOW, EVENING_WINDOW):
        if random.random() > SKIP_PROBABILITY:
            slots.append(_random_time_today(window))
    slots.sort()
    return slots


def _sleep_until(target):
    remaining = (target - datetime.datetime.now()).total_seconds()
    while remaining > 0:
        time.sleep(min(remaining, 60))
        remaining = (target - datetime.datetime.now()).total_seconds()


def run_forever(job):
    """
    Bucle principal del bot: cada día arma un horario distinto (con variación
    aleatoria y algún salto ocasional) y espera a cada momento para ejecutar `job`.
    """
    while True:
        today = datetime.date.today()
        slots = plan_today()

        if slots:
            horarios = ", ".join(s.strftime("%H:%M") for s in slots)
            print(f"Horario de hoy ({today}): {horarios}")
        else:
            print(f"Hoy ({today}) no hay publicaciones programadas (variación humana).")

        for slot in slots:
            _sleep_until(slot)
            job()

        tomorrow_start = datetime.datetime.combine(
            today + datetime.timedelta(days=1), datetime.time(0, 5)
        )
        _sleep_until(tomorrow_start)
