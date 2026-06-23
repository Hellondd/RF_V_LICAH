import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from app.database import SessionLocal
from app.models import Region

def reset_regions():
    """Очищает таблицу регионов и перезагружает из GeoJSON"""
    
    db = SessionLocal()
    
    # Удаляем все регионы
    print("🗑️ Очистка таблицы регионов...")
    deleted = db.query(Region).delete()
    db.commit()
    print(f"✅ Удалено {deleted} регионов")
    
    db.close()
    
    # Загружаем заново
    print("\n📥 Перезагрузка регионов...")
    from scripts.load_regions_from_geojson import load_regions_from_geojson
    load_regions_from_geojson()

if __name__ == "__main__":
    reset_regions()