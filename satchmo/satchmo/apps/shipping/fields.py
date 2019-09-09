from livesettings.functions import config_choice_values
from livesettings.models import SettingNotSet

def shipping_choices():
    try:
        return config_choice_values('SHIPPING','MODULES')
    except SettingNotSet:
        return ()
