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

# Константы
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'
SEARCH_URL = 'https://depositphotos.com/ru/stock-photos/{}.html'
OUTPUT_FILE = 'results.json'

def load_targets(filename='targets.json'):
    """Загрузка списка целевых товаров из JSON файла"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Ошибка при загрузке файла {filename}: {e}")
        return []

def get_html(query):
    """Получение HTML-страницы результатов поиска"""
    encoded_query = quote_plus(query)
    url = SEARCH_URL.format(encoded_query)
    
    headers = {
        'User-Agent': USER_AGENT,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
        'Referer': 'https://depositphotos.com/',
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

def extract_srcsets(html):
    """Извлечение всех значений srcset из тегов source"""
    if not html:
        return []
    
    soup = BeautifulSoup(html, 'html.parser')
    source_tags = soup.find_all('source')
    
    srcsets = []
    for source in source_tags:
        if source.has_attr('srcset'):
            # Извлекаем все URL из атрибута srcset
            urls = re.findall(r'(https://[^\s]+)', source['srcset'])
            
            # Фильтруем URLs, убираем ссылки с запятой на конце
            filtered_urls = []
            for url in urls:
                # Если URL заканчивается запятой, убираем ее
                if url.endswith(','):
                    url = url[:-1]  # Удаляем последний символ (запятую)
                
                # Проверяем, что URL не заканчивается запятой
                if not url.endswith(','):
                    filtered_urls.append(url)
            
            srcsets.extend(filtered_urls)
    
    return srcsets

def process_targets(targets):
    """Обработка списка целевых товаров"""
    results = []
    
    for target in targets:
        article = target['article']
        name = target['name']
        
        print(f"Обработка: [{article}] {name}")
        
        # Пауза между запросами, чтобы избежать блокировки
        time.sleep(random.uniform(1.5, 3.0))
        
        html = get_html(name)
        srcsets = extract_srcsets(html)
        
        result = {
            'article': article,
            'name': name,
            'images': srcsets
        }
        
        results.append(result)
        
        # Печать прогресса
        print(f"  Найдено изображений: {len(srcsets)}")
    
    return results

def save_results(results, filename=OUTPUT_FILE):
    """Сохранение результатов в JSON файл"""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print(f"Результаты сохранены в файл: {filename}")
    except Exception as e:
        print(f"Ошибка при сохранении результатов в {filename}: {e}")

def main():
    print("Начало работы скрипта парсинга depositphotos.com")
    
    # Загрузка целевых товаров
    targets = load_targets()
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