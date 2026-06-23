import json
import logging
from pathlib import Path
from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Annotated
from sqlalchemy.orm import Session

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


# ============================================================
# СПЕЦИФИЧНЫЕ РОУТЫ (ДОЛЖНЫ БЫТЬ ПЕРВЫМИ)
# ============================================================

@router.get("/geojson")
def get_regions_geojson(db: Session = Depends(get_db)):
    """Возвращает GeoJSON с границами регионов и данными из БД."""
    
    # Пробуем загрузить из разных возможных файлов
    geojson_paths = [
        Path("/app/data/russia_boundaries.geojson"),
        Path("/app/data/russia_regions.geojson"),
    ]
    
    geojson_data = None
    loaded_path = None
    
    for path in geojson_paths:
        if path.exists():
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if content.strip():
                        geojson_data = json.loads(content)
                        if isinstance(geojson_data, dict) and "features" in geojson_data:
                            loaded_path = path
                            logger.info(f"✅ Загружен GeoJSON: {path}")
                            break
            except Exception as e:
                logger.warning(f"⚠️ Ошибка загрузки {path}: {e}")
                continue
    
    if geojson_data is None:
        logger.warning("❌ GeoJSON файл не найден или пуст")
        return GEOJSON_EMPTY
    
    if not isinstance(geojson_data.get("features"), list):
        return GEOJSON_EMPTY
    
    # Получаем все регионы из БД
    regions_db = db.query(Region).all()
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
            # Если название не найдено, пропускаем
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
            props["name"] = matched_region.title  # Используем название из БД
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
    
    logger.info(f"✅ Обновлено {updated_count} регионов в GeoJSON из {len(geojson_data.get('features', []))}")
    
    return geojson_data


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
    return db.query(Region).offset(skip).limit(limit).all()

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
    return region


@router.delete("/{region_id}", status_code=204, dependencies=[Depends(get_current_admin)])
def delete_region(region_id: int, db: Session = Depends(get_db)):
    """Удалить регион (только для админа)"""
    region = db.query(Region).get(region_id)
    if not region:
        raise HTTPException(status_code=404, detail=NOT_FOUND)
    db.delete(region)
    db.commit()