#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import requests
import re
from bs4 import BeautifulSoup
import time
import random
from urllib.parse import quote_plus
import os
import pandas as pd
import sys

# Константы
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'
SEARCH_URL = 'https://prom.ua/ua/search?search_term={}'
OUTPUT_FILE = 'results.json'
MAX_IMAGES = 10  # Максимальное количество изображений для каждого товара

def load_targets(filename='targets.json', excel_file=None):
    """Загрузка списка целевых товаров из JSON файла или Excel-файла
    
    Args:
        filename (str): Путь к JSON-файлу (по умолчанию 'targets.json')
        excel_file (str): Путь к Excel-файлу (по умолчанию None)
        
    Returns:
        list: Список словарей с данными о товарах
    """
    # Если указан Excel-файл, загружаем данные из него
    if excel_file and os.path.exists(excel_file):
        return load_targets_from_excel(excel_file)
    
    # Иначе загружаем из JSON-файла
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Ошибка при загрузке файла {filename}: {e}")
        return []
        
def load_targets_from_excel(excel_file):
    """Загрузка списка целевых товаров из Excel-файла
    
    Args:
        excel_file (str): Путь к Excel-файлу
        
    Returns:
        list: Список словарей с данными о товарах
    """
    try:
        # Чтение Excel-файла
        df = pd.read_excel(excel_file)
        
        # Проверка и переименование столбцов, если необходимо
        # Предполагаем, что столбцы в Excel называются "Артикул" и "Повна назва"
        if "Артикул" in df.columns and "Повна назва" in df.columns:
            df = df.rename(columns={"Артикул": "article", "Повна назва": "name"})
        
        # Конвертация DataFrame в список словарей
        targets = []
        for _, row in df.iterrows():
            # Проверка на наличие обязательных полей
            if 'article' in row and 'name' in row:
                # Преобразование значений в строки и удаление начальных и конечных пробелов
                article = str(row['article']).strip()
                name = str(row['name']).strip()
                
                # Добавление только непустых записей
                if article and name:
                    targets.append({
                        'article': article,
                        'name': name
                    })
        
        print(f"Загружено {len(targets)} товаров из Excel-файла {excel_file}")
        return targets
    except Exception as e:
        print(f"Ошибка при загрузке Excel-файла {excel_file}: {e}")
        return []

def get_html(query):
    """Получение HTML-страницы результатов поиска
    
    Args:
        query (str): Поисковый запрос
        
    Returns:
        str: HTML-контент страницы или None в случае ошибки
    """
    encoded_query = quote_plus(query)
    url = SEARCH_URL.format(encoded_query)
    
    headers = {
        'User-Agent': USER_AGENT,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
        'Referer': 'https://prom.ua/',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе к {url}: {e}")
        return None

def extract_images(html):
    """Извлечение URL изображений из HTML-страницы
    
    Args:
        html (str): HTML-контент страницы
        
    Returns:
        list: Список URL изображений
    """
    if not html:
        return []
    
    soup = BeautifulSoup(html, 'html.parser')
    images = []
    
    # Поиск тегов picture с атрибутом data-qaid
    picture_tags = soup.find_all('picture', attrs={'data-qaid': True})
    
    for picture in picture_tags:
        # Поиск вложенного тега img с атрибутом src
        img_tag = picture.find('img', attrs={'src': True})
        if img_tag and 'src' in img_tag.attrs:
            images.append(img_tag['src'])
            
            # Ограничение количества изображений
            if len(images) >= MAX_IMAGES:
                break
    
    return images

def process_targets(targets):
    """Обработка списка целевых товаров
    
    Args:
        targets (list): Список словарей с данными о товарах
        
    Returns:
        list: Список словарей с результатами поиска
    """
    results = []
    
    for i, target in enumerate(targets):
        article = target['article']
        name = target['name']
        
        print(f"[{i+1}/{len(targets)}] Обработка: [{article}] {name}")
        
        # Пауза между запросами, чтобы избежать блокировки
        time.sleep(random.uniform(1.5, 3.0))
        
        html = get_html(name)
        images = extract_images(html)
        
        result = {
            'article': article,
            'name': name,
            'images': images
        }
        
        results.append(result)
        
        # Печать прогресса
        print(f"  Найдено изображений: {len(images)}")
    
    return results

def save_results(results, filename=OUTPUT_FILE):
    """Сохранение результатов в JSON файл
    
    Args:
        results (list): Список словарей с результатами поиска
        filename (str): Имя выходного файла
    """
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print(f"Результаты сохранены в файл: {filename}")
    except Exception as e:
        print(f"Ошибка при сохранении результатов в {filename}: {e}")

def main():
    print("Начало работы скрипта парсинга изображений с prom.ua")
    
    # Проверка наличия Excel-файла
    excel_file = 'targets.xlsx'
    json_file = 'targets.json'
    
    # Определяем источник данных в зависимости от наличия файлов
    if os.path.exists(excel_file):
        print(f"Найден Excel-файл {excel_file}, загрузка данных из него...")
        targets = load_targets(excel_file=excel_file)
    elif os.path.exists(json_file):
        print(f"Найден JSON-файл {json_file}, загрузка данных из него...")
        targets = load_targets(filename=json_file)
    else:
        print("Не найдены файлы с данными. Необходим targets.xlsx или targets.json.")
        return
    
    if not targets:
        print("Список товаров пуст или произошла ошибка при загрузке. Завершение работы.")
        return
    
    print(f"Загружено товаров: {len(targets)}")
    
    # Обработка товаров
    results = process_targets(targets)
    
    # Сохранение результатов
    save_results(results)
    
    print("Работа скрипта завершена")

if __name__ == "__main__":
    main()