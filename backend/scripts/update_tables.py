import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from app.database import engine
from app.database import Base
from app.models import *

def update_tables():
    """Создает или обновляет структуру таблиц"""
    
    print("📊 Обновление структуры таблиц...")
    
    try:
        # Создает только новые таблицы, существующие не трогает
        Base.metadata.create_all(bind=engine)
        print("✅ Структура таблиц обновлена!")
        
        # Проверяем созданные таблицы
        from sqlalchemy import inspect
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        print(f"\n📋 Таблицы в БД ({len(tables)}):")
        for table in sorted(tables):
            print(f"  - {table}")
        
        # Показываем структуру ключевых таблиц
        if 'postcard_templates' in tables:
            print("\n✅ Таблица postcard_templates создана!")
        if 'quiz_results' in tables:
            print("✅ Таблица quiz_results обновлена (добавлена связь с вопросами)!")
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    update_tables()