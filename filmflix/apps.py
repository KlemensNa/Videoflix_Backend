from django.apps import AppConfig


class FilmflixConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'filmflix'
    
    # Methode ready wird gestartet, wenn Anwendung fertig geladen ist
    # None --> zeigt das Methode kein Rückgabewert hat
    def ready(self) -> None:
        import filmflix.signals
