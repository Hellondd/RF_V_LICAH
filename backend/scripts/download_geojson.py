import os
import requests
import json
from pathlib import Path

def download_geojson():
    """Скачивает GeoJSON файл с регионами России"""
    
    # URL с данными
    url = "https://code.highcharts.com/mapdata/countries/ru/ru-all.geo.json"
    # Путь для сохранения
    data_dir = Path(__file__).parent.parent / "data"
    data_dir.mkdir(exist_ok=True)
    
    file_path = data_dir / "russia_regions.geojson"
    
    print(f"📥 Скачивание GeoJSON с регионами России...")
    print(f"📁 Сохранение в: {file_path}")
    
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        # Проверяем, что это валидный JSON
        data = response.json()
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        # Считаем количество регионов
        features_count = len(data.get('features', []))
        print(f"✅ Успешно! Скачано {features_count} регионов.")
        print(f"📂 Файл сохранен: {file_path}")
        
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Ошибка при скачивании: {e}")
        return False
    except json.JSONDecodeError as e:
        print(f"❌ Ошибка: получен невалидный JSON: {e}")
        return False

if __name__ == "__main__":
    download_geojson()