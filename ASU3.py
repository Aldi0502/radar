import numpy as np
import matplotlib.pyplot as plt
import random
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Button  # Импортируем класс кнопок

# НАЧАЛЬНЫЕ НАСТРОЙКИ
R = 10
alpha = 0
MAX_TAIL = 50  # Длина светящегося хвоста радара
is_paused = False  # Флаг паузы

# Создаем окно и оси
fig, ax = plt.subplots(figsize=(8, 8))
# Оставляем снизу место под кнопки (поднимаем график чуть выше)
plt.subplots_adjust(bottom=0.2)

ax.set_xlim(-15, 15)
ax.set_ylim(-15, 15)
ax.set_title("АСУ ТП: Сканирующий Радар Ротора")
ax.grid(True, color='gray', linestyle='--', alpha=0.5)

# Списки для хранения истории хвоста
x_history = []
y_history = []

# Создаем пустой скаттер-объект
radar_plot = ax.scatter([], [], c=[], cmap='cool', s=80) 

# Функция обновления кадра для анимации
def update(frame):
    global alpha, is_paused
    
    if is_paused:
        return radar_plot,  # Если пауза, ничего не меняем

    # Случайное приращение угла
    alpha += random.uniform(0.04, 0.12)
    
    # Считаем текущую позицию луча
    x_now = R * np.cos(alpha)
    y_now = R * np.sin(alpha)
    
    # Добавляем новые координаты
    x_history.append(x_now)
    y_history.append(y_now)
    
    # Ограничиваем длину хвоста
    if len(x_history) > MAX_TAIL:
        x_history.pop(0)
        y_history.pop(0)
        
    # Массив интенсивности
    intensity = np.linspace(0.1, 1.0, len(x_history))
    
    # Обновляем данные на графике
    radar_plot.set_offsets(np.c_[x_history, y_history])
    radar_plot.set_array(intensity)
    
    return radar_plot,

# --- ДОБАВЛЕНИЕ КНОПОК СНИЗУ ---

# Координаты для первой кнопки [left, bottom, width, height]
ax_pause = plt.axes([0.15, 0.05, 0.2, 0.05])
btn_pause = Button(ax_pause, 'Пауза / Старт', color='lightgray', hovercolor='tomato')

# Координаты для второй кнопки
ax_reset = plt.axes([0.40, 0.05, 0.2, 0.05])
btn_reset = Button(ax_reset, 'Сброс', color='lightgray', hovercolor='lightblue')

# ИСПРАВЛЕНИЕ: Идеальные координаты для третьей кнопки ENG
ax_eng = plt.axes([0.65, 0.05, 0.2, 0.05])
btn_eng = Button(ax_eng, 'ENG / RU', color='lightgray', hovercolor='purple')

# Логика для кнопки Пауза/Старт
def toggle_pause(event):
    global is_paused
    is_paused = not is_paused

# Логика для кнопки Сброс
def reset_radar(event):
    global x_history, y_history, alpha
    x_history.clear()
    y_history.clear()
    alpha = 0
    radar_plot.set_offsets(np.empty((0, 2)))
    radar_plot.set_array(np.empty(0))
    fig.canvas.draw_idle()

# логика для смены языка 
#def eng_but(event):
 #   global btn_eng , btn_reset ,btn_pause
  #  if btn_pause('Сброс')==


# Связываем кнопки с их функциями
btn_pause.on_clicked(toggle_pause)
btn_reset.on_clicked(reset_radar)
btn_eng.on_clicked(lambda event: print("eng clicked"))

# Запуск анимации
ani = FuncAnimation(fig, update, interval=20, blit=False, cache_frame_data=False)

plt.show()
