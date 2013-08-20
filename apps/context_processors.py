from django.contrib.sites.models import Site

def sites(request):
    site = Site.objects.get_current()
    return {
        'SITE_ID': site.id,
        'SITE_DOMAIN': site.domain,
        'SITE_NAME': site.name,
    }
