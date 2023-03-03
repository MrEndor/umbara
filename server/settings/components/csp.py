"""
This file contains a definition for Content-Security-Policy headers.

Read more about it:
https://developer.mozilla.org/ru/docs/Web/HTTP/Headers/Content-Security-Policy

We are using `django-csp` to provide these headers.
Docs: https://github.com/mozilla/django-csp
"""

CSP_SCRIPT_SRC = (
    "'self'",
    "'unsafe-inline'",
    'cdn.ckeditor.com',
)
CSP_SCRIPT_SRC_ELEM = (
    "'self'",
    "'unsafe-inline'",
    'ajax.googleapis.com',
    'cdn.jsdelivr.net',
    'cdn.ckeditor.com',
)
CSP_IMG_SRC = ("'self'",)
CSP_FONT_SRC = ("'self'",)
CSP_STYLE_SRC = (
    "'self'",
    "'unsafe-inline'",
    'cdn.jsdelivr.net',
    'cdn.ckeditor.com',
)
CSP_DEFAULT_SRC = ("'none'",)
CSP_CONNECT_SRC = ("'self'", 'pdf-converter.cke-cs.com')
CSP_SCRIPT_SRC_ATTR = (
    "'self'",
    "'unsafe-inline'",
    'cdn.ckeditor.com',
)
