from app.infrastructure.db.base import Base
from app.infrastructure.db.database import engine
from app.infrastructure.db import models


def reset_database():
    """Elimina y recrea todas las tablas"""
    print("⚠️  ELIMINANDO todas las tablas...")
    Base.metadata.drop_all(bind=engine)
    
    print("✅ Creando tablas nuevamente...")
    Base.metadata.create_all(bind=engine)
    
    print("✅ Base de datos reseteada exitosamente")


if __name__ == "__main__":
    import sys
    response = input("¿Estás seguro de resetear la base de datos? (escriba 'SI' para confirmar): ")
    if response == "SI":
        reset_database()
    else:
        print("Operación cancelada")
        sys.exit(0)