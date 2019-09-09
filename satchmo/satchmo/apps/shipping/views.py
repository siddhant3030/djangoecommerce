 # pylint: disable=W0613,W0231
import os
import sys
import logging
import threading
import subprocess
from tempfile import mkstemp
try:
    import trml2pdf
    HAS_TRML = True
except ImportError:
    trml2pdf = object()
    HAS_TRML = False
from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import get_object_or_404
from django.utils.encoding import smart_str
import six
try: 
    from importlib import import_module
except ImportError:
    from django.utils.importlib import import_module    
from django.views.decorators.cache import never_cache
from satchmo_store.shop.models import Order
from satchmo_store.shop.models import Config
from livesettings.functions import config_value


class ConverterError(Exception):
    """An error occurred while setting up the converter
    """


class DocumentBase(object):
    """The base document converter class.

    Any custom-defined converter must subclass this one as the first class.
    """

    def get_context(self, request, order_id, doc):
        return {
            'order' : get_object_or_404(Order, pk=order_id),
            'doc': doc,
            'iconURI' : config_value('SHOP', 'LOGO_URI'),
            'shopDetails' : Config.objects.get_current(),
            'default_view_tax': config_value('TAX','DEFAULT_VIEW_TAX')
        }

    def __call__(self, request, order_id, doc):
        return self.render(request, self.get_context(request, order_id, doc))


class FileTemplateMixin(object):
    """The file template mixin.

    Subclass from this mixin to load file templates.
    """

    def get_template(self, request, context):
        template_name = "%s.%s" % (context['doc'], self.template_ext)
        template_path = os.path.join(self.template_dir, template_name)
        return loader.get_template(template_path)


class BaseRenderer(object):
    """The base class for rendering the document (usually in an intermediate
    format).
    """

    def get_content(self, request, context):
        template = self.get_template(request, context)
        return template.render(context)


class HTMLRenderMixin(BaseRenderer):
    """The HTML (normal page) template mixin.

    Subclass from this mixin if you want to render directly within the
    browser.
    """

    def render(self, request, context):
        return HttpResponse(self.get_content(request, context))


class FileRenderMixin(BaseRenderer):
    """The file render mixin.

    Renders as a downloadable file (attachment). Subclass from this mixin if
    you are not rendering to a format understood by the browser natively.
    """

    def get_filename(self, request, context):
        return '%s-%s-%d.%s' % (
            context['shopDetails'].site.domain,
            context['doc'],
            context['order'].pk,
            self.output_ext
        )

    def render(self, request, context):
        filename = self.get_filename(request, context)
        content = self.convert(self.get_content(request, context))
        response = HttpResponse(content_type=self.mimetype)
        if config_value('SHIPPING','DOWNLOAD_PDFS'):
            content_disposition = 'attachment; filename=%s' % filename
            response['Content-Disposition'] = content_disposition
        response.write(content)
        return response


class HTMLDocument(DocumentBase, FileTemplateMixin, HTMLRenderMixin):
    """The default document class, rendering every document as HTML
    """
    template_ext = 'html'
    template_dir = 'shop/docs/html'


class TRMLDocument(DocumentBase, FileTemplateMixin, FileRenderMixin):
    """The RML PDF document generator.

    Available only if trml2pdf is installed.
    """

    mimetype = "application/pdf"
    template_ext = 'rml'
    template_dir = 'shop/docs/rml'
    output_ext = 'pdf'

    def __init__(self):
        if not HAS_TRML:
            raise ConverterError(
                "'trml2pdf' must be installed on your system "
                "for the TRMLDocument converter to work properly. "
                "Please make sure "
                "that the 'trml2pdf' egg is within your PYTHONPATH, "
                "and install it via 'pip install trml2pdf' otherwise."
            )

    def convert(self, data):
        return trml2pdf.parseString(smart_str(data))


class WKHTMLDocument(DocumentBase, FileTemplateMixin, FileRenderMixin):
    """The "webkit to html" PDF generator.

    Available only if the static binary of
    http://code.google.com/p/wkhtmltopdf/ has been downloaded and extracted
    somewhere and its path provided via 'settings.py', as follows:

    SATCHMO_SETTINGS = {
        ...
        'WKHTML2PDF_BINARIES': {
            ...
            'linux2': '/path/to/wkhtmltopdf'
        }
    }

    It is to be noted that every key value pair within 'WKHTML2PDF_BINARIES'
    associates a different executable to every platform as named by
    'sys.platform'. You can have many or just one, depending if you reuse your
    'settings.py' between development and production (and whether you use Mac
    OS X for development).
    """

    mimetype = "application/pdf"
    template_ext = 'html'
    template_dir = 'shop/docs/html'
    output_ext = 'pdf'

    def __init__(self):
        satchmo_settings = getattr(settings, 'SATCHMO_SETTINGS', {})
        wkhtml2pdf_binaries = satchmo_settings.get(
            'WKHTML2PDF_BINARIES',
            {}
        )
        self.wkhtml2pdf = wkhtml2pdf_binaries.get(sys.platform, None)
        if self.wkhtml2pdf is None:
            raise ConverterError(
                ("WKHTMLDocument can't find the 'wkhtmltopdf' binary "
                 "for your platform. "
                 "Please make sure "
                 "that SATCHMO_SETTINGS['WKHTML2PDF_BINARIES']['%s'] exists "
                 "within your 'settings.py' "
                 "and that it contains the absolute path to the binary.") % (
                    sys.platform,
                )
            )

    def convert(self, data):
        logger = logging.getLogger('wkhtml2pdf')
        fd, input_file = mkstemp(suffix='input.'+self.template_ext,
                                 prefix='satchmo-wkhtml')
        os.close(fd)
        fd, output_file = mkstemp(suffix='output.'+self.output_ext,
                                  prefix='satchmo-wkhtml')
        os.close(fd)
        errors_fd, errors_file = mkstemp(
            suffix='errors',
            prefix='satchmo-wkhtml'
        )
        try:
            if isinstance(data, six.text_type):
                data = data.encode("utf-8")
            with open(input_file, 'wb') as input:
                input.write(data)
            args = (self.wkhtml2pdf, "-q",
                    input_file, "--encoding", "utf-8", "--print-media-type",
                    output_file)
            logger.debug("Calling %s" % " ".join(args))
            returncode = subprocess.call(args, stderr=errors_fd)
            if returncode != 0:
                with open(errors_file, 'rb') as errors:
                    logger.error(
                        "wkhtmltopdf failed (%d): %s" % (
                            returncode,
                            errors.read()
                        )
                    )
            with open(output_file, 'rb') as output:
                return output.read()
        finally:
            os.close(errors_fd)
            os.remove(input_file)
            os.remove(output_file)
            os.remove(errors_file)


class ConverterFactory(object):
    """A thread-safe document converter factory.

    Tries to load the converted specified in the
    SATCHMO_SETTINGS['DOCUMENT_CONVERTER'] setting (as the full dotted name of
    the class).

    If this setting is absent, defaults to using HTMLDocument.
    """

    def __init__(self):
        self.Converter = None
        self.lock = threading.Lock()

    def __call__(self, *args, **kwargs):
        if self.Converter is None:
            self.lock.acquire()
            classpath = getattr(settings, 'SATCHMO_SETTINGS', {}).get(
                'DOCUMENT_CONVERTER', None)
            if classpath is None:
                self.Converter = TRMLDocument
            else:
                module_name, class_name = classpath.rsplit('.', 1)
                module = import_module(module_name)
                self.Converter = getattr(module, class_name)
            self.lock.release()
        return self.Converter(*args, **kwargs)


converter_factory = ConverterFactory()


@staff_member_required
@never_cache
def displayDoc(request, id, doc):
    """Displays the document using the specified converter in 'settings.py'.
    """
    converter = converter_factory()
    return converter(request, id, doc)
