"""
Migration pour créer la table des mutations de parcelles
"""
import sqlite3
from pathlib import Path

def create_mutations_table(db_path: str = "backend.db"):
    """Crée la table parcel_mutations dans la base de données"""
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Créer la table parcel_mutations
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS parcel_mutations (
                id TEXT PRIMARY KEY,
                parcel_id TEXT NOT NULL,
                mutation_type TEXT NOT NULL CHECK(mutation_type IN ('sale', 'donation', 'inheritance', 'exchange', 'expropriation', 'subdivision', 'merge', 'other')),
                from_owner_id INTEGER,
                to_owner_id INTEGER,
                initiated_by_user_id TEXT NOT NULL,
                price REAL,
                notes TEXT,
                status TEXT NOT NULL DEFAULT 'pending' CHECK(status IN ('pending', 'approved', 'rejected', 'completed', 'cancelled')),
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                approved_at TEXT,
                approved_by_user_id TEXT,
                completed_at TEXT,
                rejection_reason TEXT,
                FOREIGN KEY (parcel_id) REFERENCES parcels(id) ON DELETE CASCADE,
                FOREIGN KEY (from_owner_id) REFERENCES owners(id) ON DELETE SET NULL,
                FOREIGN KEY (to_owner_id) REFERENCES owners(id) ON DELETE SET NULL,
                FOREIGN KEY (initiated_by_user_id) REFERENCES users(id) ON DELETE RESTRICT,
                FOREIGN KEY (approved_by_user_id) REFERENCES users(id) ON DELETE SET NULL
            )
        """)
        
        # Créer des index pour améliorer les performances
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_mutations_parcel_id 
            ON parcel_mutations(parcel_id)
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_mutations_status 
            ON parcel_mutations(status)
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_mutations_created_at 
            ON parcel_mutations(created_at DESC)
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_mutations_from_owner 
            ON parcel_mutations(from_owner_id)
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_mutations_to_owner 
            ON parcel_mutations(to_owner_id)
        """)
        
        conn.commit()
        print("✅ Table parcel_mutations créée avec succès")
        
    except sqlite3.Error as e:
        print(f"❌ Erreur lors de la création de la table: {e}")
        conn.rollback()
        raise
    finally:
        conn.close()

if __name__ == "__main__":
    create_mutations_table()
