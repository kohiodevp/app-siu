"""
Optimisations de performance pour l'application
"""
from functools import lru_cache
from typing import Dict, Any
import time

class PerformanceMonitor:
    """Moniteur de performance pour les requêtes"""
    
    def __init__(self):
        self.query_times: Dict[str, list] = {}
    
    def record_query_time(self, query_name: str, duration: float):
        """Enregistre le temps d'une requête"""
        if query_name not in self.query_times:
            self.query_times[query_name] = []
        self.query_times[query_name].append(duration)
    
    def get_stats(self) -> Dict[str, Any]:
        """Retourne les statistiques de performance"""
        stats = {}
        for query_name, times in self.query_times.items():
            if times:
                stats[query_name] = {
                    'count': len(times),
                    'avg': sum(times) / len(times),
                    'min': min(times),
                    'max': max(times)
                }
        return stats

# Instance globale
performance_monitor = PerformanceMonitor()

def time_query(func):
    """Décorateur pour mesurer le temps d'exécution"""
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        duration = time.time() - start
        performance_monitor.record_query_time(func.__name__, duration)
        return result
    return wrapper

@lru_cache(maxsize=128)
def cached_zone_stats(zone: str) -> Dict[str, Any]:
    """Cache les statistiques par zone"""
    # Les résultats sont mis en cache automatiquement
    return {}

