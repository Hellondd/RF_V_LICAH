import json
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from app.database import SessionLocal
from app.models import Region

def seed_regions():
    db = SessionLocal()
    
    # Путь к файлу с данными
    data_path = Path(__file__).parent.parent / "data" / "regions_data.json"
    
    if not data_path.exists():
        print(f"❌ Файл {data_path} не найден!")
        print("💡 Положите regions_data.json в папку backend/data/")
        db.close()
        return
    
    with open(data_path, 'r', encoding='utf-8') as f:
        regions = json.load(f)
    
    created = 0
    updated = 0
    
    for region_data in regions:
        # Проверяем, существует ли уже регион
        existing = db.query(Region).filter(Region.title == region_data['title']).first()
        
        if existing:
            # Обновляем существующий
            for key, value in region_data.items():
                setattr(existing, key, value)
            updated += 1
            print(f"🔄 Обновлен: {region_data['title']}")
        else:
            # Создаем новый
            region = Region(**region_data)
            db.add(region)
            created += 1
            print(f"✅ Добавлен: {region_data['title']}")
    
    db.commit()
    db.close()
    
    print(f"\n🎉 Готово!")
    print(f"   ✅ Создано: {created}")
    print(f"   🔄 Обновлено: {updated}")
    print(f"   📊 Всего в БД: {db.query(Region).count()}")

if __name__ == "__main__":
    seed_regions()