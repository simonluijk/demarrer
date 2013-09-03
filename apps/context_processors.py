from django.contrib.sites.models import Site
from crispy_forms.helper import FormHelper


def sites(request):
    site = Site.objects.get_current()
    return {
        'SITE_ID': site.id,
        'SITE_DOMAIN': site.domain,
        'SITE_NAME': site.name,
    }


def bootstrap3(request):
    helper = FormHelper()
    helper.form_class = 'form-horizontal'
    helper.label_class = 'col-lg-4'
    helper.field_class = 'col-lg-8'
    helper.disable_csrf = True
    helper.form_tag = False
    helper.html5_required = True

    return {
        'crispy_horizontal': helper
    }
