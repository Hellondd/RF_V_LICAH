import os
from pathlib import Path

def cleanup_images():
    """Удаляет лишние файлы изображений"""
    
    # ПРАВИЛЬНЫЙ ПУТЬ
    images_dir = Path("/app/frontend/images")
    
    if not images_dir.exists():
        print(f"❌ Папка не найдена: {images_dir}")
        print("📂 Проверяем доступные папки...")
        for p in Path("/app").iterdir():
            if p.is_dir():
                print(f"  - /app/{p.name}")
        return
    
    print(f"✅ Найдена папка: {images_dir}")
    print()
    
    # Список файлов, которые увеличились в WebP (удаляем WebP, оставляем JPG)
    bad_webp_files = [
        'bryansk.webp',
        'dagestan.webp',
        'ivanovo.webp',
        'kalmykia.webp',
        'khakasia.webp',
        'moscow_region.webp',
        'primorsky.webp',
        'pskov.webp',
        'rostov.webp',
        'ryazan.webp',
        'sevastopol.webp',
        'smolensk.webp',
        'tula.webp',
        'voronezh.webp',
        'yaroslavl.webp',
    ]
    
    # Находим все WebP
    all_webp = list(images_dir.glob("*.webp"))
    good_webp = [f for f in all_webp if f.name not in bad_webp_files]
    bad_webp = [f for f in all_webp if f.name in bad_webp_files]
    
    deleted_jpg = 0
    deleted_webp = 0
    total_saved = 0
    
    print(f"📊 Найдено WebP файлов: {len(all_webp)}")
    print(f"📊 Хороших WebP (оставляем): {len(good_webp)}")
    print(f"📊 Плохих WebP (удаляем): {len(bad_webp)}")
    print()
    
    # 1. Удаляем JPG для хороших WebP
    for webp_file in good_webp:
        jpg_path = webp_file.with_suffix('.jpg')
        if jpg_path.exists():
            size = jpg_path.stat().st_size / 1024
            jpg_path.unlink()
            deleted_jpg += 1
            total_saved += size
            print(f"🗑️ Удален JPG: {jpg_path.name} ({size:.1f}KB) — заменен на WebP")
    
    # 2. Удаляем плохие WebP (оставляем JPG)
    for webp_file in bad_webp:
        if webp_file.exists():
            size = webp_file.stat().st_size / 1024
            webp_file.unlink()
            deleted_webp += 1
            total_saved += size
            print(f"🗑️ Удален WebP: {webp_file.name} ({size:.1f}KB) — возвращаем JPG")
    
    print()
    print("🎉 Готово!")
    print(f"✅ Удалено JPG файлов: {deleted_jpg}")
    print(f"✅ Удалено WebP файлов: {deleted_webp}")
    print(f"💾 Освобождено места: {total_saved:.1f}KB ({total_saved/1024:.2f}MB)")

if __name__ == "__main__":
    cleanup_images()