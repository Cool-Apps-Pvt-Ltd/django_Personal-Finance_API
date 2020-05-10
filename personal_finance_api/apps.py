from django.apps import AppConfig


class PersonalFinanceApiConfig(AppConfig):
    name = 'personal_finance_api'

    def ready(self):
        import personal_finance_api.signals
        # Below is a dummy do nothing line to prevent unused import error
        str(vars(personal_finance_api.signals))
