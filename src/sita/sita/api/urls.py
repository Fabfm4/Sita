# -*- coding: utf-8 -*-
from django.conf import settings
from django.conf.urls import include, url


urlpatterns = [
    url(
        r'^v1/',
        include(
            'sita.api.v1.urls',
            namespace='v1'
        )
    ),
]
