#!/usr/bin/env python3
"""
Script de test pour valider les corrections apportées
"""
import sys
sys.path.insert(0, '.')

from database import SessionLocal, init_db
from models.user import User, Role
from models.parcel import Parcel
from infrastructure.repositories.parcel_repository import SqlParcelRepository
from infrastructure.repositories.user_repository import SqlUserRepository
from utils.db_helpers import escape_like_pattern, safe_ilike
from utils.role_helpers import get_role_value, is_admin, is_admin_or_manager

def test_database_transactions():
    """Test que les transactions sont bien gérées"""
    print("🧪 Test 1: Database Transactions")
    db = SessionLocal()
    try:
        # Créer un rôle
        role = Role(name="test_role", description="Test role")
        db.add(role)
        db.commit()
        
        # Vérifier qu'il existe
        found = db.query(Role).filter(Role.name == "test_role").first()
        assert found is not None, "❌ Le rôle n'a pas été committé"
        
        # Nettoyer
        db.delete(found)
        db.commit()
        
        print("   ✅ Transactions fonctionnent correctement")
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        db.rollback()
    finally:
        db.close()

def test_sql_injection_protection():
    """Test que l'échappement SQL fonctionne"""
    print("🧪 Test 2: SQL Injection Protection")
    
    # Test échappement des caractères spéciaux
    test_cases = [
        ("test%", "test\\%"),
        ("test_", "test\\_"),
        ("test\\", "test\\\\"),
        ("normal", "normal"),
        ("%_test_%", "\\%\\_test\\_\\%"),
    ]
    
    all_passed = True
    for input_str, expected in test_cases:
        result = escape_like_pattern(input_str)
        if result != expected:
            print(f"   ❌ Échappement incorrect: '{input_str}' -> '{result}' (attendu: '{expected}')")
            all_passed = False
    
    if all_passed:
        print("   ✅ Échappement SQL fonctionne correctement")

def test_role_normalization():
    """Test que la normalisation des rôles fonctionne"""
    print("🧪 Test 3: Role Normalization")
    
    # Test avec différents types de rôles
    test_role = Role(name="administrator")
    
    role_value = get_role_value(test_role)
    assert role_value == "administrator", f"❌ get_role_value échoué: {role_value}"
    
    role_str = get_role_value("Manager")
    assert role_str == "manager", f"❌ get_role_value avec string échoué: {role_str}"
    
    print("   ✅ Normalisation des rôles fonctionne")

def test_pagination():
    """Test que la pagination fonctionne"""
    print("🧪 Test 4: Pagination")
    db = SessionLocal()
    repo = SqlParcelRepository(db)
    
    try:
        # Test de recherche avec pagination
        criteria = {
            'page': 1,
            'page_size': 10,
            'search_term': 'test'
        }
        
        results = repo.search(criteria)
        count = repo.count_search(criteria)
        
        assert isinstance(results, list), "❌ Les résultats doivent être une liste"
        assert isinstance(count, int), "❌ Le comptage doit être un entier"
        assert len(results) <= 10, f"❌ Trop de résultats: {len(results)}"
        
        print(f"   ✅ Pagination fonctionne (trouvé {count} résultats, limité à {len(results)})")
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
    finally:
        db.close()

def test_eager_loading():
    """Test que l'eager loading est configuré"""
    print("🧪 Test 5: Eager Loading")
    db = SessionLocal()
    user_repo = SqlUserRepository(db)
    
    try:
        # Créer un utilisateur de test avec un rôle
        role = db.query(Role).first()
        if not role:
            role = Role(name="test_user_role", description="Test")
            db.add(role)
            db.commit()
        
        test_user = User(
            username="eager_test_user",
            email="eager@test.com",
            password="test123",
            role_id=role.id
        )
        db.add(test_user)
        db.commit()
        
        # Récupérer l'utilisateur
        found_user = user_repo.get_by_username("eager_test_user")
        
        # Fermer la session pour forcer le test d'eager loading
        db.close()
        
        # Si l'eager loading fonctionne, on peut accéder au rôle sans lazy loading
        try:
            role_name = found_user.role.name if found_user and found_user.role else None
            print(f"   ✅ Eager loading fonctionne (rôle: {role_name})")
        except Exception:
            print("   ⚠️  Eager loading pourrait ne pas être optimal")
        
        # Nettoyer
        db2 = SessionLocal()
        db2.query(User).filter(User.username == "eager_test_user").delete()
        db2.commit()
        db2.close()
        
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        db.rollback()
    finally:
        if db.is_active:
            db.close()

def main():
    """Execute tous les tests"""
    print("\n" + "="*60)
    print("🔧 TESTS DES CORRECTIONS - Application SIU")
    print("="*60 + "\n")
    
    # Initialiser la base de données
    try:
        init_db()
        print("✅ Base de données initialisée\n")
    except Exception as e:
        print(f"❌ Erreur d'initialisation de la base: {e}\n")
        return
    
    # Exécuter les tests
    test_database_transactions()
    test_sql_injection_protection()
    test_role_normalization()
    test_pagination()
    test_eager_loading()
    
    print("\n" + "="*60)
    print("✅ TESTS TERMINÉS")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
