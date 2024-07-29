import cv2
import json
import os

def draw_labels(image_path, info_animals, output_path, labels, filename, width, height):
    image = cv2.imread(image_path)
    
    for info in info_animals:
        label = labels[str(info['category'])]
        conf = info['conf']
        draw_label(image, f'{label} {conf}', info['bbox'], width, height)
        
    cv2.imwrite(os.path.join(output_path, filename), image)
        


def draw_label(image, category, coordinates, width, height):

    # Загружаем изображение
    #image = cv2.imread(image_path)
    
    # Декодируем координаты рамки
    coord = tuple(coordinates)
    x1, y1, x2, y2 = coord
    x1 *= width
    x2 *= width
    y1 *= height
    y2 *= height
    
    # Рисуем рамку
    color = (255, 0, 0)  # Зеленый цвет
    thickness = 1  # Толщина линии
    cv2.rectangle(image, (int(x1), int(y1)), (int(x1) + int(x2), int(y1) + int(y2)), color, thickness)
    
    # Настройки текста
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.5
    font_thickness = 1
    text_size, _ = cv2.getTextSize(category, font, font_scale, font_thickness)
    
    # Позиция текста (над рамкой)
    text_x = x1
    text_y = y1 - 10  # Чуть выше верхней границы рамки
    
    # Если текст выходит за границы изображения, корректируем его позицию
    text_y = max(text_y, text_size[1])
    
    # Рисуем фон для текста (чтобы текст был читаемым)
    cv2.rectangle(image, (int(text_x), int(text_y) - text_size[1]), 
                  (int(text_x) + text_size[0], int(text_y) + text_size[1] - 10), 
                  color, cv2.FILLED)
    
    # Рисуем текст
    cv2.putText(image, category, (int(text_x), int(text_y)), font, font_scale, (255, 255, 255), font_thickness)