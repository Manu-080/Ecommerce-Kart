from django.apps import AppConfig


class ProductsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'products'

# To conect signals to apps.py.
    def ready(self): 
        import products.signals # Import signals when the app is ready