# ZooML

В этом репозитории содержится инструмент для классификации животных с фотоловушек.

## Список животных 
- барсук 
- птица 
- кабан 
- бурый медведь 
- олень 
- лиса 
- заяц 
- гималайский медведь
- рысь
- манул
- сурок
- енотовидная собака
- снежный леопард
- белка
- ласка
- волк
- росомаха

## Установка

Примечание: выполняйте все скрипты в директории ZooML

1. склонируйте репозиторий:
   ```
   git clone https://github.com/Ivsoffy/ZooML.git
   ```
2. установите зависимости:
   Во время установки, укажите такой путь, чтобы директория находилась рядом с директорией ZooML
   ```
   bash install_dependencies.sh
   ```
## Запуск
Перед запуском основного скрипта, создайте переменную окружения
   ```
   export ZOOPATH='path_to_dir_ZooML'
   ```
Где path_to_dir_ZooML это абсолютный путь до директории ZooML.

для проверки, что все установилось правильно, можно запустить демо. изначально скрипт настроен на демо. Запускаем скрипт в папке ZooML.

   ```
   bash detect_and_classifier.sh
   ```
Для запуска модели на своих данных необходимо запустить скрипт с двумя параметрами
   ```
   bash detect_and_classifier.sh path_to_input_dir path_to_output_dir
   ```
где
- path_to_input_dir - путь до папки с фотографиями, которые нужно обработать
- path_to_output_dir - путь до папки, в которую будут сохраняться фотографии с классифицированными животными

## Разделение классифицированных файлов по папкам
в репозитории присутствует скрипт для разделения классифицированных фотографий по папкам.
```
python split_by_directories.py path_to_images path_to_classifier_json_file path_to_folder_with_classes
```
где:
- path_to_images - путь до директории с классифицированными фотографиями
- path_to_classifier_json_file - путь до json файла с классификацией фотографий
- path_to_folder_with_classes - путь до директории, где будут находиться классы
### Запуск демо
```
python split_by_directories.py ./dataset/output_images ./dataset/annotations/raw_images_classifier.json ./dataset/classes
```
## Пример работы
![Classifier image](https://github.com/Ivsoffy/ZooML/blob/main/dataset/repos_img/demo.jpg)
