import json
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from app.database import SessionLocal
from app.models import Region

def map_regions_to_geojson():
    """Создает файл соответствия между БД и GeoJSON"""
    
    db = SessionLocal()
    
    # Загружаем GeoJSON
    geo_path = Path(__file__).parent.parent / "data" / "russia_boundaries.geojson"
    
    if not geo_path.exists():
        print(f"❌ Файл {geo_path} не найден!")
        return
    
    print(f"📂 Загрузка GeoJSON: {geo_path}")
    
    with open(geo_path, 'r', encoding='utf-8') as f:
        geojson = json.load(f)
    
    # Получаем все регионы из БД
    regions = db.query(Region).all()
    print(f"📊 Регионов в БД: {len(regions)}")
    print(f"📊 Регионов в GeoJSON: {len(geojson.get('features', []))}")
    
    # Создаем маппинг
    mapping = {}
    not_found = []
    
    # Для каждого региона из БД ищем соответствие в GeoJSON
    for region in regions:
        found = False
        region_name = region.title.lower()
        
        for feature in geojson.get('features', []):
            props = feature.get('properties', {})
            geo_name = (
                props.get('region') or 
                props.get('name') or 
                props.get('NAME') or 
                ''
            ).lower()
            
            # Проверяем соответствие (учитываем разные варианты написания)
            if (region_name == geo_name or 
                region_name in geo_name or 
                geo_name in region_name or
                region_name.replace(' область', '') in geo_name or
                geo_name.replace(' область', '') in region_name):
                
                mapping[region.id] = {
                    'region_id': region.id,
                    'title': region.title,
                    'geojson_title': props.get('region') or props.get('name'),
                    'feature_index': geojson.get('features', []).index(feature)
                }
                found = True
                break
        
        if not found:
            not_found.append(region.title)
    
    # Сохраняем маппинг
    mapping_path = Path(__file__).parent.parent / "data" / "region_mapping.json"
    with open(mapping_path, 'w', encoding='utf-8') as f:
        json.dump(mapping, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ Найдено соответствий: {len(mapping)}")
    print(f"❌ Не найдено: {len(not_found)}")
    
    if not_found:
        print("\n⚠️ Регионы без соответствия в GeoJSON:")
        for name in not_found[:10]:
            print(f"  - {name}")
    
    db.close()

if __name__ == "__main__":
    map_regions_to_geojson()