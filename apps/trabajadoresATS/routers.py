class MirrhhRouter(object):
    """
    A router to control all database operations on models in the historic application.
    """
    def db_for_read(self, model, **hints):
        """
        Attempts to read historic models go to historical.
        """
        if model._meta.app_label == 'trabajadoresATS':
            return 'aasana_bd'
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write historic models go to historical.
        """
        if model._meta.app_label == 'trabajadoresATS':
            return 'aasana_bd'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the historic app is involved.
        """
        if obj1._meta.app_label == 'plan_vuelo' or \
            obj2._meta.app_label == 'trabajadoresATS':
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the historic app only appears in the 'historical' database.
        """
        if app_label == 'trabajadoresATS':
            return db == 'aasana_bd'
        return None

