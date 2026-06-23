import json
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from app.database import SessionLocal
from app.models import Region

def load_regions_from_geojson():
    """Загружает регионы из GeoJSON файла"""
    
    db = SessionLocal()
    
    geo_path = Path(__file__).parent.parent / "data" / "russia_boundaries.geojson"
    
    if not geo_path.exists():
        print(f"❌ Файл {geo_path} не найден!")
        return False
    
    print(f"📂 Загрузка из файла: {geo_path}")
    
    try:
        with open(geo_path, 'r', encoding='utf-8') as f:
            geojson_data = json.load(f)
    except Exception as e:
        print(f"❌ Ошибка чтения файла: {e}")
        return False
    
    features = geojson_data.get('features', [])
    print(f"📊 Найдено {len(features)} регионов в GeoJSON")
    
    # Показываем пример структуры для отладки
    if features:
        sample_props = features[0].get('properties', {})
        print(f"\n🔍 Пример свойств региона:")
        for key, value in list(sample_props.items())[:5]:
            print(f"  - {key}: {value}")
        print()
    
    created = 0
    skipped = 0
    unknown = 0
    
    for feature in features:
        props = feature.get('properties', {})
        
        # Ищем название региона по всем возможным ключам
        name = (
            props.get('region') or           # Ваш ключ!
            props.get('name') or 
            props.get('NAME') or 
            props.get('name_ru') or 
            props.get('NAME_RU') or
            props.get('oblast') or
            props.get('admin') or
            props.get('admin_name') or
            None
        )
        
        # Если название не найдено, пропускаем
        if not name:
            unknown += 1
            print(f"⚠️ Пропущен регион без названия (свойства: {list(props.keys())})")
            continue
        
        # Извлекаем федеральный округ
        federal_district = (
            props.get('federal_district') or
            props.get('federalDistrict') or
            props.get('FEDERAL_DISTRICT') or
            props.get('district') or
            props.get('DISTRICT') or
            None
        )
        
        # Проверяем, существует ли уже регион с таким названием
        existing = db.query(Region).filter(Region.title == name).first()
        
        if existing:
            skipped += 1
            continue
        
        # Создаем новый регион
        region = Region(
            title=name,
            federal_district=federal_district,
            capital=None,
            short_description=f"Регион {name}",
            full_description=None,
            facts=None,
            culture=None,
            achievements=None,
            image_url=None
        )
        
        db.add(region)
        created += 1
        
        if created % 10 == 0:
            print(f"  Загружено {created} регионов...")
    
    # Сохраняем изменения
    db.commit()
    db.close()
    
    print(f"\n🎉 Готово!")
    print(f"✅ Создано новых регионов: {created}")
    print(f"⏭️ Пропущено (уже существовали): {skipped}")
    print(f"⚠️ Пропущено (без названия): {unknown}")
    
    if created > 0:
        # Показываем примеры загруженных регионов
        db = SessionLocal()
        regions = db.query(Region).limit(5).all()
        print(f"\n📋 Примеры загруженных регионов:")
        for r in regions:
            print(f"  - {r.title} (Округ: {r.federal_district or 'не указан'})")
        db.close()
    
    return True

if __name__ == "__main__":
    load_regions_from_geojson()