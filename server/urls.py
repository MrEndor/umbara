"""
Main URL mapping configuration file.

Include other URLConfs from external apps using method `include()`.

It is also a good practice to keep a single URL to the root index page.

This examples uses Django's default media
files serving technique in development.
"""

from django.conf import settings
from django.contrib import admin
from django.contrib.admindocs import urls as admindocs_urls
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path
from django.views.generic import TemplateView
from health_check import urls as health_urls

from server.apps.about import urls as about_urls
from server.apps.catalog import urls as catalog_urls
from server.apps.homepage import urls as homepage_urls
from server.endpoints import coffee

admin.autodiscover()

urlpatterns = [
    # Apps:
    path('', include(homepage_urls, namespace='homepage')),
    path('about/', include(about_urls, namespace='about')),
    path('catalog/', include(catalog_urls, namespace='catalog')),

    path('coffee/', coffee, name='coffee'),

    # Health checks:
    path('health/', include(health_urls)),

    # django-admin:
    path('admin/doc/', include(admindocs_urls)),
    path('admin/', admin.site.urls),

    # Text and xml static files:
    path('robots.txt', TemplateView.as_view(
        template_name='txt/robots.txt',
        content_type='text/plain',
    )),
    path('humans.txt', TemplateView.as_view(
        template_name='txt/humans.txt',
        content_type='text/plain',
    )),
]

if settings.DEBUG:  # pragma: no cover
    import debug_toolbar  # noqa: WPS433
    from django.conf.urls.static import static  # noqa: WPS433

    urlpatterns = [
        # URLs specific only to django-debug-toolbar:
        path('__debug__/', include(debug_toolbar.urls)),
        *urlpatterns,
        # Serving media files in development only:
        *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
        *staticfiles_urlpatterns(),
        path('ckeditor/', include('ckeditor_uploader.urls')),
    ]
