# ГЛАВНЫЙ КОНТРОЛЛЕР (насос + спринклер)

from machine import Pin          # 1. Управление проводами (GPIO)
import time                      # 2. Таймеры и паузы
from neopixel import NeoPixel    # 3. Цветной светодиод статус

print("СИСТЕМА ПОЖАРОТУШЕНИЯ СТАРТОВАЛА")  # 4. Приветствие
