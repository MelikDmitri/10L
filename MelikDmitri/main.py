# ГЛАВНЫЙ КОНТРОЛЛЕР (насос + спринклер)

from machine import Pin          # 1. Управление проводами (GPIO)
import time                      # 2. Таймеры и паузы
from neopixel import NeoPixel    # 3. Цветной светодиод статус

print("СИСТЕМА ПОЖАРОТУШЕНИЯ СТАРТОВАЛА")  # 4. Приветствие

# ПОДКЛЮЧЕНИЕ ОБОРУДОВАНИЯ

pump = Pin(13, Pin.OUT)           # 5. GPIO13 = насос (10 литров в минуту)
sprinkler = Pin(14, Pin.OUT)      # 6. GPIO14 = поворотный спринклер
status_led = NeoPixel(Pin(16), 1) # 7. GPIO16 = большой цветной LED

# Состояние системы
system_active = False             # 8. Работает ли сейчас тушение?
start_time = 0                    # 9. Когда началось тушение
sprinkler_time = 12000            # 10. Тушим 12 секунд

# Стартовая настройка
status_led[0] = (0, 255, 0)      # 11. Зелёный = система готова
status_led.write()                # 12. Включаем LED
print("ОЖИДАЮ ПОЖАР...")       # 13. Готовность

# ОСНОВНОЙ ЦИКЛ РАБОТЫ

while True:                       # 14. Никогда не останавливаемся
    try:
        # Читаем сигнал от камеры (Serial)
        command = input().strip()  # 15. Ждём сообщение типа "S1_FIRE_0.82"
        
        if "S1_FIRE" in command:   # 16. Камера увидела пожар
            fire_level = float(command.split('_')[2])  # 17. Извлекаем число 0.82
            print(f"ПОЖАР! Уверенность ИИ: {fire_level:.1%}")
            
            if fire_level > 0.65 and not system_active:  # 18. Проверяем порог
                # АКТИВАЦИЯ ТУШЕНИЯ
                system_active = True     # 19. Запускаем
                start_time = time.ticks_ms()  # 20. Фиксируем время
                
                pump.on()                # 21. НАСОС ВКЛ
                sprinkler.on()           # 22. СПРИНКЛЕР ОТКРЫТ (вода льётся)
                
                status_led[0] = (255, 0, 0)  # 23. Красный = тушение
                status_led.write()
                
                print("НАСОС ЗАПУЩЕН")     # 24. Лог
                print("СПРИНКЛЕР ВРАЩАЕТСЯ") # 25. Лог
                print("Тушение: 12 секунд...")
                
    except:
        pass  # 26. Если нет команды — продолжаем ждать

    # АВТОМАТИЧЕСКАЯ ОСТАНОВКА
    if system_active and time.ticks_diff(time.ticks_ms(), start_time) > sprinkler_time:
        pump.off()                   # 27. Насос остановить
        sprinkler.off()              # 28. Спринклер закрыть
        system_active = False        # 29. Система свободна
        
        status_led[0] = (0, 255, 0)  # 30. Зелёный = готово
        status_led.write()
        
        print("ТУШЕНИЕ ЗАВЕРШЕНО")   # 31. Успех
        print("СИСТЕМА ГОТОВА К НОВОМУ ПОЖАРУ")
    
    time.sleep_ms(100)               # 32. Не нагружаем процессор
