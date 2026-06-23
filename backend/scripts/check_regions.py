import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from app.database import SessionLocal
from app.models import Region

def check_regions():
    """Проверяет количество загруженных регионов"""
    
    db = SessionLocal()
    
    total = db.query(Region).count()
    print(f"📊 Всего регионов в БД: {total}")
    
    # Показываем первые 10 для проверки
    regions = db.query(Region).limit(10).all()
    print("\n📋 Примеры загруженных регионов:")
    for region in regions:
        print(f"  - {region.title} (Округ: {region.federal_district or 'не указан'})")
    
    db.close()
    
    return total

if __name__ == "__main__":
    check_regions()