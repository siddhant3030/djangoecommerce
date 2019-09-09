def active_gateways():
    """Get a list of activated payment gateways, in the form of
    [(module, config module name),...]
    """
    try:
        from django.apps import apps
        app_list = [app_config.models_module for app_config in apps.get_app_configs() if app_config.models_module is not None]
    except ImportError:
        from django.db import models
        app_list = models.get_apps()
              
    gateways = []
    for app in app_list:
        if hasattr(app, 'PAYMENT_PROCESSOR'):
            parts = app.__name__.split('.')[:-1]
            module = ".".join(parts)
            group = 'PAYMENT_%s' % parts[-1].upper()
            gateways.append((module, group))
    return gateways
