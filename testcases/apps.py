from django.apps import AppConfig


class TestcasesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'testcases'
    verbose_name = "Summary"

    def ready(self):
        import testcases.signals    