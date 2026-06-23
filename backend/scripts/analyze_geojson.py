import json
import sys
from pathlib import Path
from collections import Counter

sys.path.append(str(Path(__file__).parent.parent))

def analyze_geojson():
    """Анализирует структуру GeoJSON файла"""
    
    geo_path = Path(__file__).parent.parent / "data" / "russia_boundaries.geojson"
    
    if not geo_path.exists():
        print(f"❌ Файл {geo_path} не найден!")
        return
    
    print(f"📂 Анализ файла: {geo_path}\n")
    
    with open(geo_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    features = data.get('features', [])
    print(f"📊 Всего регионов: {len(features)}")
    
    if not features:
        print("❌ Нет данных в файле!")
        return
    
    # Анализируем свойства первого региона
    sample_props = features[0].get('properties', {})
    print(f"\n🔍 Свойства первого региона:")
    for key, value in sample_props.items():
        print(f"  - {key}: {value}")
    
    # Собираем все ключи из всех регионов
    all_keys = Counter()
    name_keys = []
    
    for feature in features:
        props = feature.get('properties', {})
        all_keys.update(props.keys())
        
        # Проверяем, какие ключи могут содержать названия
        for key in ['region', 'name', 'NAME', 'name_ru', 'NAME_RU', 'oblast', 'admin', 'admin_name']:
            if key in props and props[key]:
                name_keys.append(key)
    
    print(f"\n📋 Все уникальные ключи в свойствах:")
    for key, count in all_keys.most_common(10):
        print(f"  - {key}: встречается {count} раз")
    
    if name_keys:
        print(f"\n🔑 Ключи, используемые для названий:")
        for key in set(name_keys):
            count = name_keys.count(key)
            print(f"  - {key}: {count} раз")
    
    # Показываем примеры названий
    print(f"\n📋 Примеры названий регионов:")
    for i, feature in enumerate(features[:5]):
        props = feature.get('properties', {})
        name = (
            props.get('region') or 
            props.get('name') or 
            props.get('NAME') or 
            props.get('name_ru') or 
            'Неизвестно'
        )
        print(f"  {i+1}. {name}")
    
    print(f"\n💡 Рекомендация:")
    if 'region' in all_keys:
        print("  ✅ Используйте ключ 'region' для названий")
    elif 'name' in all_keys:
        print("  ✅ Используйте ключ 'name' для названий")
    else:
        print("  ⚠️ Не найден стандартный ключ для названий")
        print(f"  Используйте один из: {list(all_keys.keys())[:5]}")

if __name__ == "__main__":
    analyze_geojson()