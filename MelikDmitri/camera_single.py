# cam_single.py — ESP32-CAM (КАМЕРА + ИИ)

import camera          # 1. Библиотека для камеры ESP32-CAM
import network         # 2. Для WiFi и беспроводной связи
import ujson           # 3. Создаёт JSON сообщения {"fire":0.82}
from machine import Pin # 4. Управляет светодиодом (GPIO)
import time            # 5. Задержки и таймеры

# НАСТРОЙКА ОБОРУДОВАНИЯ

led_red = Pin(4, Pin.OUT)    # 6. GPIO4 = красный светодиод (тревога)
led_green = Pin(2, Pin.OUT)  # 7. GPIO2 = зелёный светодиод (норма)

# WiFi для беспроводной связи
wlan = network.WLAN(network.STA_IF)  # 8. Включаем WiFi режим "станция"
wlan.active(True)                    # 9. Запускаем WiFi

# Камера (размер 320x240 пикселей)
camera.init(0, format=camera.JPEG, framesize=7)  # 10. FRAMESIZE_QVGA=7

print("Камера готова. Сканирую поле каждые 5 секунд...")  # 11. Сообщение о запуске

# ОСНОВНОЙ ЦИКЛ (работа 24/7)

while True:              # 12. Бесконечный цикл (система не останавливается)
    
    try:                 # 13. "Попробуй сделать, если ошибка то продолжи"
        img = camera.capture()  # 14. Делаем фото поля
        
        # ИИ АНАЛИЗ
        fire_level = 0.82 if time.localtime()[5] % 2 == 0 else 0.12  # 15. Чередуем огонь/норма
        
        print(f"Поле: огонь = {fire_level:.1%}")  # 16. Показываем процент огня
        
        if fire_level > 0.65:  # 17. Если больше 65% — ПОЖАР
            led_red.on()       # 18. Красный светодиод ВКЛ
            led_green.off()    # 19. Зелёный ВЫКЛ
            
            # Сообщение главному контроллеру
            message = ujson.dumps({"event": "ПОЖАР", "уровень": fire_level})  # 20. JSON данные
            print(f"ОТПРАВЛЯЮ: {message}")  # 21. Показываем что отправили
            print("S1_FIRE_" + str(fire_level))  # 22. Serial сигнал для main.py
            
        else:                # 23. Нет пожара
            led_red.off()      # 24. Красный ВЫКЛ
            led_green.on()     # 25. Зелёный ВКЛ
            print("Поле чистое")  # 26. Нормальный статус
            
    except Exception as error:  # 27. Если камера сломалась
        print(f"Ошибка камеры: {error}")  # 28. Пишем ошибку
        
    time.sleep(5)        # 29. Ждём 5 секунд перед следующим сканом
