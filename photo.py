import os
from PIL import Image
from transliterate import translit
from datetime import datetime

# Функция изменения размеров изображения
def resize_image(image_path, max_size=None, width=None, height=None):
    try:
        # Открываем изображение с помощью Pillow
        with Image.open(image_path) as img:
            orig_width, orig_height = img.size  # Получаем текущие размеры изображения
            new_width, new_height = orig_width, orig_height  # Изначально размеры остаются такими же

            # Определяем масштабирование в зависимости от входных параметров
            if width:
                scaling_factor = width / float(orig_width)
                new_width = width
                new_height = int(orig_height * scaling_factor)
            elif height:
                scaling_factor = height / float(orig_height)
                new_width = int(orig_width * scaling_factor)
                new_height = height
            elif max_size:
                if orig_width > orig_height:
                    scaling_factor = max_size / float(orig_width)
                else:
                    scaling_factor = max_size / float(orig_height)
                new_width = int(orig_width * scaling_factor)
                new_height = int(orig_height * scaling_factor)

            # Проверяем, нужно ли изменять размер изображения
            if (new_width, new_height) != (orig_width, orig_height):
                img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                img.save(image_path)
                print(f"Изображение {image_path} изменено до размеров {new_width}x{new_height}")
            else:
                print(f"Изображение {image_path} не требует изменения размера")
    except Exception as e:
        print(f"Ошибка при обработке изображения {image_path}:\n {e}")

# Функция транслитерации имени файла с добавлением даты
def transliterate_filename(filename, date_suffix):
    name, ext = os.path.splitext(filename)   # Разделяем имя файла и расширение
    transliterated_name = translit(name, 'ru', reversed=True)   # Транслитерация
    new_name = f"{transliterated_name}_{date_suffix}{ext}"
    return new_name

# Функция изменения всех изображений в папке
def resize_images_in_folder(folder_path, max_size=None, width=None, height=None, date_suffix=''):
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

            resize_image(image_path, max_size=max_size, width=width, height=height)

if __name__ == "__main__":
    # Запрашиваем путь к папке с фотографиями
    folder_path = input("Введите путь к папке с изображениями: ").strip()

    # Запрашиваем параметры масштабирования
    scaling_choice = input("Выберите способ масштабирования (по умолчанию 400 для большей стороны, введите 'w' или 'h'): ").strip().lower()
    if scaling_choice == 'w':
        width = int(input("Введите ширину для масштабирования: ").strip())
        height = None
        max_size = None
    elif scaling_choice == 'h':
        height = int(input("Введите высоту для масштабирования: ").strip())
        width = None
        max_size = None
    else:
        width = None
        height = None
        max_size = 400

    # Запрашиваем дату для добавления к названию файлов (по умолчанию текущая дата)
    date_input = input("Введите дату: ").strip()
    if not date_input:
        date_suffix = datetime.now().strftime('%d.%m.%Y')
    else:
        try:
            date_suffix = datetime.strptime(date_input, '%d.%m.%Y').strftime('%d.%м.%Y')
        except ValueError:
            print("Неправильный формат даты. Используется текущая дата.")
            date_suffix = datetime.now().strftime('%d.%m.%Y')

    if os.path.isdir(folder_path):
        resize_images_in_folder(folder_path, max_size=max_size, width=width, height=height, date_suffix=date_suffix)
    else:
        print("Указанный путь не является папкой.")

input("Нажмите Enter для выхода")