import json
import logging
from pathlib import Path
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import JSONResponse
from typing import Annotated
from sqlalchemy.orm import Session
from functools import lru_cache
from datetime import datetime, timedelta
import hashlib

from app.database import get_db
from app.core.deps import get_current_admin
from app.models import Region
from app.schemas.region import RegionCreate, RegionUpdate, RegionOut

logger = logging.getLogger(__name__)

# ВАЖНО: redirect_slashes=False отключает автоматическое перенаправление
router = APIRouter(prefix="/regions", tags=["regions"], redirect_slashes=False)

NOT_FOUND = "Регион не найден"
GEOJSON_EMPTY = {"type": "FeatureCollection", "features": []}

# Список возможных ключей для названия региона в GeoJSON
REGION_NAME_KEYS = [
    'region',      # Ваш основной ключ
    'name', 
    'NAME', 
    'name_ru', 
    'NAME_RU',
    'oblast',
    'admin',
    'admin_name',
    'title'
]

# Кэш для GeoJSON
_geojson_cache = {
    "data": None,
    "timestamp": None,
    "file_hash": None,
    "cache_duration": 3600  # 1 час в секундах
}

def get_geojson_file_hash() -> str:
    """Получает хеш файла GeoJSON для проверки изменений"""
    geo_paths = [
        Path("/app/data/russia_boundaries.geojson"),
        Path("/app/data/russia_regions.geojson"),
    ]
    
    for path in geo_paths:
        if path.exists():
            with open(path, 'rb') as f:
                return hashlib.md5(f.read()).hexdigest()
    return None

def load_geojson_file() -> dict:
    """Загружает GeoJSON файл с кэшированием"""
    global _geojson_cache
    
    current_hash = get_geojson_file_hash()
    
    # Проверяем кэш
    if _geojson_cache["data"] is not None and _geojson_cache["file_hash"] == current_hash:
        # Проверяем время жизни кэша
        if _geojson_cache["timestamp"] is not None:
            elapsed = (datetime.now() - _geojson_cache["timestamp"]).total_seconds()
            if elapsed < _geojson_cache["cache_duration"]:
                logger.debug("✅ GeoJSON загружен из кэша")
                return _geojson_cache["data"]
    
    # Если кэш устарел или данных нет - загружаем
    logger.info("🔄 Загрузка GeoJSON из файла...")
    
    geojson_paths = [
        Path("/app/data/russia_boundaries.geojson"),
        Path("/app/data/russia_regions.geojson"),
    ]
    
    for path in geojson_paths:
        if path.exists():
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if content.strip():
                        data = json.loads(content)
                        if isinstance(data, dict) and "features" in data:
                            # Обновляем кэш
                            _geojson_cache["data"] = data
                            _geojson_cache["timestamp"] = datetime.now()
                            _geojson_cache["file_hash"] = current_hash
                            logger.info(f"✅ GeoJSON загружен из файла: {path}")
                            return data
            except Exception as e:
                logger.warning(f"⚠️ Ошибка загрузки {path}: {e}")
                continue
    
    return None

def clear_geojson_cache():
    """Очищает кэш GeoJSON (для принудительного обновления)"""
    global _geojson_cache
    _geojson_cache["data"] = None
    _geojson_cache["timestamp"] = None
    _geojson_cache["file_hash"] = None
    logger.info("🗑️ Кэш GeoJSON очищен")

# ============================================================
# СПЕЦИФИЧНЫЕ РОУТЫ (ДОЛЖНЫ БЫТЬ ПЕРВЫМИ)
# ============================================================

@router.get("/geojson")
def get_regions_geojson(db: Session = Depends(get_db)):
    """Возвращает GeoJSON с границами регионов и данными из БД."""
    
    # Загружаем GeoJSON из кэша или файла
    geojson_data = load_geojson_file()
    
    if geojson_data is None:
        logger.warning("❌ GeoJSON файл не найден или пуст")
        return GEOJSON_EMPTY
    
    if not isinstance(geojson_data.get("features"), list):
        return GEOJSON_EMPTY
    
    # Получаем все регионы из БД
    regions_db = db.query(Region).all()
    
    # Создаем словари для быстрого поиска
    regions_dict = {region.title.lower(): region for region in regions_db}
    
    # Создаем маппинг для частичного совпадения
    region_mapping = {}
    for region in regions_db:
        title_lower = region.title.lower()
        # Добавляем варианты без "область", "край", "республика" и т.д.
        simple_name = title_lower.replace(' область', '').replace(' край', '').replace(' республика', '').replace(' автономный округ', '').replace(' автономная область', '').strip()
        if simple_name != title_lower:
            region_mapping[simple_name] = region
        region_mapping[title_lower] = region
    
    updated_count = 0
    total_features = len(geojson_data.get("features", []))
    
    for feature in geojson_data.get("features", []):
        if not isinstance(feature, dict):
            continue
        
        props = feature.get("properties", {})
        if not isinstance(props, dict):
            continue
        
        # Ищем название региона по всем возможным ключам
        region_name = None
        for key in REGION_NAME_KEYS:
            if key in props and props[key]:
                region_name = props[key]
                break
        
        if not region_name:
            continue
        
        region_name_lower = region_name.lower()
        matched_region = None
        
        # 1. Прямое совпадение
        if region_name_lower in regions_dict:
            matched_region = regions_dict[region_name_lower]
        # 2. Совпадение по маппингу (упрощенные названия)
        elif region_name_lower in region_mapping:
            matched_region = region_mapping[region_name_lower]
        # 3. Частичное совпадение
        else:
            for title_lower, region in regions_dict.items():
                if title_lower in region_name_lower or region_name_lower in title_lower:
                    matched_region = region
                    break
        
        if matched_region:
            # Обновляем свойства в GeoJSON
            props["db_id"] = matched_region.id
            props["name"] = matched_region.title
            props["region_name"] = matched_region.title
            props["capital"] = matched_region.capital
            props["short_description"] = matched_region.short_description
            props["full_description"] = matched_region.full_description
            props["image_url"] = matched_region.image_url
            props["federal_district"] = matched_region.federal_district
            props["facts"] = matched_region.facts
            props["culture"] = matched_region.culture
            props["achievements"] = matched_region.achievements
            updated_count += 1
    
    logger.info(f"✅ Обновлено {updated_count} регионов в GeoJSON из {total_features}")
    
    # Добавляем заголовки кэширования 
    response = JSONResponse(content=geojson_data)
    response.headers["Cache-Control"] = "public, max-age=3600, stale-while-revalidate=86400"
    response.headers["Vary"] = "Accept-Encoding"
    
    return response


@router.post("/geojson/clear-cache")
def clear_cache():
    """Очищает кэш GeoJSON (для админов)"""
    clear_geojson_cache()
    return {"status": "ok", "message": "Кэш GeoJSON очищен"}


# ============================================================
# КОРНЕВОЙ РОУТ (ДОЛЖЕН БЫТЬ ПЕРЕД ДИНАМИЧЕСКИМИ)
# ============================================================

# Роут СЛЕШОМ
@router.get("/")
def list_regions(
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=200)] = 100,
    db: Session = Depends(get_db),
):
    """Получить список всех регионов"""
    response = db.query(Region).offset(skip).limit(limit).all()
    return response

# Роут БЕЗ СЛЕША (для запросов /regions?limit=5)
@router.get("")
def list_regions_no_slash(
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=200)] = 100,
    db: Session = Depends(get_db),
):
    """Получить список всех регионов (без слеша)"""
    return db.query(Region).offset(skip).limit(limit).all()


@router.post("/", response_model=RegionOut, status_code=201, dependencies=[Depends(get_current_admin)])
def create_region(payload: RegionCreate, db: Session = Depends(get_db)):
    """Создать новый регион (только для админа)"""
    region = Region(**payload.model_dump())
    db.add(region)
    db.commit()
    db.refresh(region)
    # После создания региона очищаем кэш
    clear_geojson_cache()
    return region


@router.get("/all", response_model=list[RegionOut])
def get_all_regions(db: Session = Depends(get_db)):
    """Получить все регионы без пагинации"""
    return db.query(Region).all()


# ============================================================
# ДИНАМИЧЕСКИЕ РОУТЫ (С ID) - ДОЛЖНЫ БЫТЬ ПОСЛЕДНИМИ
# ============================================================

@router.get("/{region_id}")
def get_region(region_id: int, db: Session = Depends(get_db)):
    """Получить регион по ID"""
    region = db.query(Region).get(region_id)
    if not region:
        raise HTTPException(status_code=404, detail=NOT_FOUND)
    return region


@router.get("/{region_id}/info")
def get_region_info(region_id: int, db: Session = Depends(get_db)):
    """Получить полную информацию о регионе для попапа"""
    region = db.query(Region).get(region_id)
    if not region:
        raise HTTPException(status_code=404, detail=NOT_FOUND)
    
    return {
        "id": region.id,
        "title": region.title,
        "federal_district": region.federal_district,
        "capital": region.capital,
        "short_description": region.short_description,
        "full_description": region.full_description,
        "facts": region.facts,
        "culture": region.culture,
        "achievements": region.achievements,
        "image_url": region.image_url
    }


@router.put("/{region_id}", response_model=RegionOut, dependencies=[Depends(get_current_admin)])
def update_region(region_id: int, payload: RegionUpdate, db: Session = Depends(get_db)):
    """Обновить регион (только для админа)"""
    region = db.query(Region).get(region_id)
    if not region:
        raise HTTPException(status_code=404, detail=NOT_FOUND)
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(region, field, value)
    db.commit()
    db.refresh(region)
    # После обновления региона очищаем кэш
    clear_geojson_cache()
    return region


@router.delete("/{region_id}", status_code=204, dependencies=[Depends(get_current_admin)])
def delete_region(region_id: int, db: Session = Depends(get_db)):
    """Удалить регион (только для админа)"""
    region = db.query(Region).get(region_id)
    if not region:
        raise HTTPException(status_code=404, detail=NOT_FOUND)
    db.delete(region)
    db.commit()
    # После удаления региона очищаем кэш
    clear_geojson_cache()