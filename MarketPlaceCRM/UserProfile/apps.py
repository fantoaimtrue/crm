from django.apps import AppConfig

class UserProfileConfig(AppConfig):
    name = 'UserProfile'

    def ready(self):
        import UserProfile.signals
