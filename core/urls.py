from django.conf.urls import patterns, include, url
from django.conf import settings
from django.views.generic import TemplateView


# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()


urlpatterns = []
if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT
        })
    )


urlpatterns += patterns('',
    url(r'^$', TemplateView.as_view(template_name='index.html'),
        name='home'),

    url(r'^accounts/', include('registration.backends.simple.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),

    url(r'^robots\.txt$', TemplateView.as_view(template_name='robots.txt',
                                               content_type='text/plain')),

    # Uncomment & change CODE to verify site with Google
    # url(r'^googleCODE\.txt$',
    #     TemplateView.as_view(template_name='google-verify.html',
    #                          content_type="text/plain"))
)
