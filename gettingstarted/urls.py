from django.urls import path, include
from django.contrib import admin
from django.views.generic import RedirectView
from django.conf.urls import url

admin.autodiscover()

import hello.views
import hello.register

# To add a new path, first import the app:
# import blog
#
# Then add the new path:
# path('blog/', blog.urls, name="blog")
#
# Learn more here: https://docs.djangoproject.com/en/2.1/topics/http/urls/

urlpatterns = [
    path("", hello.views.index, name="index"),
    path("register/", hello.register.register, name="register"),
    path("db/", hello.views.db, name="db"),
    path("admin/", admin.site.urls),
    url(r'^favicon\.ico$',RedirectView.as_view(url='/static/images/favicon.ico')),
]
