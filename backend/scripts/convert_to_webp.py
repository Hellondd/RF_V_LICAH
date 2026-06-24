import os
from pathlib import Path
from PIL import Image
import sys

def convert_images_to_webp():
    """Конвертирует все JPG/PNG изображения в WebP"""
    
    # Путь к папке с изображениями
    images_dir = Path(__file__).parent.parent.parent / "frontend" / "images"
    
    if not images_dir.exists():
        print(f"❌ Папка {images_dir} не найдена")
        return
    
    print(f"📂 Обработка папки: {images_dir}")
    
    # Поддерживаемые форматы
    extensions = ['.jpg', '.jpeg', '.png']
    
    converted = 0
    failed = 0
    skipped = 0
    
    for file_path in images_dir.iterdir():
        if file_path.suffix.lower() not in extensions:
            continue
        
        # Пропускаем если уже есть WebP версия
        webp_path = file_path.with_suffix('.webp')
        if webp_path.exists():
            print(f"⏭️ WebP уже существует: {webp_path.name}")
            skipped += 1
            continue
        
        try:
            print(f"🔄 Конвертация: {file_path.name} -> {webp_path.name}")
            
            # Открываем изображение
            img = Image.open(file_path)
            
            # Конвертируем в RGB если нужно (для PNG с альфа-каналом)
            if img.mode in ('RGBA', 'LA', 'P'):
                img = img.convert('RGB')
            
            # Сохраняем в WebP с качеством 85%
            img.save(webp_path, 'WEBP', quality=85, optimize=True)
            
            # Получаем размеры
            original_size = file_path.stat().st_size / 1024
            webp_size = webp_path.stat().st_size / 1024
            reduction = (1 - webp_size / original_size) * 100
            
            print(f"   ✅ {original_size:.1f}KB -> {webp_size:.1f}KB (сжатие {reduction:.1f}%)")
            converted += 1
            
        except Exception as e:
            print(f"   ❌ Ошибка конвертации {file_path.name}: {e}")
            failed += 1
    
    print(f"\n🎉 Готово!")
    print(f"✅ Сконвертировано: {converted}")
    print(f"⏭️ Пропущено (уже есть WebP): {skipped}")
    print(f"❌ Ошибок: {failed}")

if __name__ == "__main__":
    convert_images_to_webp()