"""
Tests pour le ParcelService
"""
import sys
sys.path.insert(0, '..')

from backend.models.parcel import Parcel, ParcelCategory

def test_parcel_statistics():
    """Test le calcul des statistiques"""
    from backend.services.parcel_service import ParcelService
    
    # Mock repository
    class MockParcelRepository:
        def get_all(self):
            return [
                type('obj', (object,), {
                    'id': '1',
                    'reference_cadastrale': 'REF001',
                    'area': 1000.0,
                    'category': 'Habitation',
                    'zone': 'Zone A',
                    'status': 'available'
                })(),
                type('obj', (object,), {
                    'id': '2',
                    'reference_cadastrale': 'REF002',
                    'area': 2000.0,
                    'category': 'Commercial',
                    'zone': 'Zone B',
                    'status': 'occupied'
                })()
            ]
    
    service = ParcelService(None, None, None, None)
    service.parcel_repository = MockParcelRepository()
    
    stats = service.get_parcel_statistics()
    
    assert stats['total'] == 2, f"Expected 2, got {stats['total']}"
    assert stats['total_area'] == 3000.0, f"Expected 3000.0, got {stats['total_area']}"
    assert stats['average_area'] == 1500.0, f"Expected 1500.0, got {stats['average_area']}"
    assert 'by_category' in stats
    assert 'by_status' in stats
    print("✅ test_parcel_statistics passed")

def test_escape_like_pattern():
    """Test l'échappement des caractères SQL"""
    from backend.utils.db_helpers import escape_like_pattern
    
    assert escape_like_pattern("test%") == "test\\%"
    assert escape_like_pattern("test_") == "test\\_"
    assert escape_like_pattern("test\\") == "test\\\\"
    assert escape_like_pattern("normal") == "normal"
    print("✅ test_escape_like_pattern passed")

if __name__ == '__main__':
    test_parcel_statistics()
    test_escape_like_pattern()
    print("\n✅ Tous les tests backend passés")
