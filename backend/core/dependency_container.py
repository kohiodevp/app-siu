"""
Conteneur d'injection de dépendances pour l'application
"""
from typing import Dict, Type, Any, Callable
from functools import wraps


class DependencyContainer:
    """
    Conteneur d'injection de dépendances simple pour l'application
    """
    def __init__(self):
        self._singletons: Dict[Type, Any] = {}
        self._factories: Dict[Type, Callable] = {}
        self._transients: Dict[Type, Type] = {}

    def register_singleton(self, interface: Type, implementation: Type):
        """
        Enregistre un singleton (instance unique partagée)
        """
        self._singletons[interface] = implementation

    def register_factory(self, interface: Type, factory: Callable):
        """
        Enregistre une fabrique (fonction qui crée une instance à chaque fois)
        """
        self._factories[interface] = factory

    def register_transient(self, interface: Type, implementation: Type):
        """
        Enregistre un transient (nouvelle instance à chaque demande)
        """
        self._transients[interface] = implementation

    def resolve(self, interface: Type) -> Any:
        """
        Résout une dépendance en retournant une instance appropriée
        """
        # Vérifier si c'est un singleton
        if interface in self._singletons:
            if isinstance(self._singletons[interface], interface):
                # Déjà instancié
                return self._singletons[interface]
            else:
                # Instancier et sauvegarder
                impl_class = self._singletons[interface]
                instance = self._create_instance(impl_class)
                self._singletons[interface] = instance
                return instance

        # Vérifier si c'est une fabrique
        if interface in self._factories:
            factory = self._factories[interface]
            return factory()

        # Vérifier si c'est un transient
        if interface in self._transients:
            impl_class = self._transients[interface]
            return self._create_instance(impl_class)

        # Si aucune correspondance, essayer d'instancier directement
        return self._create_instance(interface)

    def _create_instance(self, cls: Type) -> Any:
        """
        Crée une instance en résolvant récursivement les dépendances du constructeur
        """
        # Obtenir les annotations du constructeur
        import inspect
        sig = inspect.signature(cls.__init__)
        params = sig.parameters

        # Préparer les arguments
        args = {}
        for name, param in params.items():
            if name == 'self':
                continue
            if param.annotation != inspect.Parameter.empty:
                # Résoudre la dépendance
                dep_instance = self.resolve(param.annotation)
                args[name] = dep_instance

        # Créer l'instance
        return cls(**args)


# Instance globale du conteneur
container = DependencyContainer()


def inject(func):
    """
    Décorateur pour injecter automatiquement les dépendances dans une fonction
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Obtenir les annotations de la fonction
        import inspect
        sig = inspect.signature(func)
        params = sig.parameters

        # Résoudre les dépendances manquantes
        resolved_kwargs = {}
        for name, param in params.items():
            if name in kwargs:
                # Déjà fourni
                resolved_kwargs[name] = kwargs[name]
            elif param.annotation != inspect.Parameter.empty:
                # Résoudre via le conteneur
                resolved_kwargs[name] = container.resolve(param.annotation)

        return func(*args, **resolved_kwargs)

    return wrapper