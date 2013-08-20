from django.conf import settings
from storages.backends.s3boto import S3BotoStorage


StaticStorage = lambda: S3BotoStorage(location='static',
                                      custom_domain=settings.MEDIA_DOMAIN)

MediaStorage = lambda: S3BotoStorage(location='media',
                                     custom_domain=settings.MEDIA_DOMAIN)
