def active_product_types():
    """Get a list of activated product modules, in the form of
    [(module, config module name),...]
    """
    gateways = []
    try:
        from django.apps import apps
        app_list = [app_config.models_module for app_config in apps.get_app_configs() if app_config.models_module is not None]
    except ImportError:
        from django.db import models
        app_list = models.get_apps()
    for app in app_list:
        if hasattr(app, 'SATCHMO_PRODUCT'):
            parts = app.__name__.split('.')[:-1]
            module = ".".join(parts)
            if hasattr(app, 'get_product_types'):
                subtypes = app.get_product_types()
                for subtype in subtypes:
                    gateways.append((module, subtype))
            else:
                gateways.append((module, parts[-1].capitalize() + 'Product'))

    return gateways
