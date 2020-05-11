from django.apps import AppConfig


class CoreFinanceAppConfig(AppConfig):
    name = 'core_finance_app'

    def ready(self):
        import core_finance_app.signals
        # Below is a dummy do nothing line to prevent unused import error
        str(vars(core_finance_app.signals))
