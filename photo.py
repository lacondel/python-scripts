import os
from PIL import Image

# Функция изменения размеров изображения
def resize_image(image_path, max_size=600):
    try:
        # Открываем изображение с помощью Pillow
        with Image.open(image_path) as img:
            width, height = img.size # Получаем текущие размеры изображения
            # Проверяем стороны, больше ли они max_size
            if width > max_size or height > max_size:
                # Определяем коэффициент масштабирования
                if width > height:
                    scaling_factor = max_size / float(width)
                else:
                    scaling_factor = max_size / float(height)

                # Вычисляем новые размеры изображения
                new_width = int(width * scaling_factor)
                new_height = int(height * scaling_factor)

                # Изменяем размеры изображения
                img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

                # Сохраняем изображение, заменяя оригинал
                img.save(image_path)
                print("Размеры изменены")
    except Exception as e:
        print(f"Ошибка при обработке изображения {image_path}:\n {e}")

# Функция изменения всех изображений в папке
def resize_images_in_folder(folder_path, max_size=600):
    # Перебираем все файлы в указанной папке
    for filename in os.listdir(folder_path):
        # Проверяем, является ли файл изображением
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(folder_path, filename)
            resize_image(image_path, max_size)

if __name__ == "__main__":
    # Запрашиваем путь к папке с фотографиями
    folder_path = input("Введите путь к папке с изображениями: ").strip()

    if os.path.isdir(folder_path):
        resize_images_in_folder(folder_path)
    else:
        print("Указанный путь не является папкой.")