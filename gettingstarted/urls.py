from django.urls import path, include
from django.contrib import admin
from django.views.generic import RedirectView
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

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
    path("inbox/", hello.views.inbox, name="inbox"),
    path("register/", hello.register.register, name="register"),
    path("dbdump/", hello.views.db, name="db"),
    path("new/", hello.views.index, name="index"),
    path("logout/", hello.views.logout, name="logout"),
    url(r'^favicon\.ico$',RedirectView.as_view(url='/static/images/favicon.ico')),
    #url('^', include('django.contrib.auth.urls')),
    #path('admin/', admin.site.urls),
] + static(settings.DBDUMP_URL, document_root=settings.DBDUMP_ROOT)

