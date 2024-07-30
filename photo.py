import os
from PIL import Image
from transliterate import translit
from datetime import datetime

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
    except Exception as e:
        print(f"Ошибка при обработке изображения {image_path}:\n {e}")

# Функция транслитерации имени файла с добавлением даты
def transliterate_filename(filename, date_suffix):
    name, ext = os.path.splitext(filename)   # Разделяем имя файла и расширение
    transliterated_name = translit(name, 'ru', reversed=True)   # Транслитерация
    new_name = f"{transliterated_name}_{date_suffix}{ext}"
    return new_name

# Функция изменения всех изображений в папке
def resize_images_in_folder(folder_path, max_size=600, date_suffix=''):
    # Перебираем все файлы в указанной папке
    for filename in os.listdir(folder_path):
        # Проверяем, является ли файл изображением
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(folder_path, filename)
            
            # Транслитерация имени файла и добавление даты
            new_filename = transliterate_filename(filename, date_suffix)
            new_image_path = os.path.join(folder_path, new_filename)

            # Переименование файла, если имя изменилось
            if image_path != new_image_path:
                os.rename(image_path, new_image_path)
                image_path = new_image_path   # Обновляем путь к файлу

            resize_image(image_path, max_size)

if __name__ == "__main__":
    # Запрашиваем путь к папке с фотографиями
    folder_path = input("Введите путь к папке с изображениями: ").strip()

    # Запрашиваем дату для добавления к названию  файлов (по умолчанию текущая дата)
    date_input = input("Введите дату: ").strip()
    if not date_input:
        date_suffix = datetime.now().strftime('%d.%m.%Y')
    else:
        try:
            date_suffix = datetime.strptime(date_input, '%d.%m.%Y').strftime('%d.%m.%Y')
        except ValueError:
            print("Неправильные формат даты. Используется текущая дата.")
            date_suffix = datetime.now().strftime('%d.%m.%Y')

    if os.path.isdir(folder_path):
        resize_images_in_folder(folder_path, date_suffix=date_suffix)
    else:
        print("Указанный путь не является папкой.")
