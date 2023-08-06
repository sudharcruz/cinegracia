from django.apps import AppConfig


class RegisterConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'register'


    def ready(self):
        # Import and register the custom tag library
        from django.template import Engine
        Engine.get_default().libraries['future'] = 'myapp.future_tags'