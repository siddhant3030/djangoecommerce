from django import forms
from django.utils.translation import ugettext as _
from django.utils.safestring import mark_safe
from livesettings.functions import config_value
from sorl.thumbnail.admin import AdminImageMixin
from sorl.thumbnail import get_thumbnail

class AdminImageWithThumbnailWidget(AdminImageMixin, forms.FileInput):
    """
    A FileField Widget that shows its current image as a thumbnail if it has one.
    """
    def __init__(self, attrs={}):
        super(AdminImageWithThumbnailWidget, self).__init__(attrs)

    def render(self, name, value, **kwargs):
        output = []
        if value and hasattr(value, "path"):
            # Generate 120px wide thumbnail for the admin interface
            # TODO: replace manual thumbnail generation with a template tag
            thumb = get_thumbnail(value.path, '120',
                    quality=config_value('THUMBNAIL', 'IMAGE_QUALITY'))
            output.append('<img src="%s" /><br/>%s<br/> %s ' % \
                (thumb.url, value.url, _('Change:')))
        output.append(super(AdminImageWithThumbnailWidget, self).render(name, value, **kwargs))
        return mark_safe(''.join(output))
