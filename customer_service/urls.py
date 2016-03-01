from django.conf.urls import include, url
from django.contrib import admin

from customer_service.twitter_api.views import TwitterApiHomeView

admin.autodiscover()

urlpatterns = [
    # Examples:
    # url(r'^$', 'customer_service.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', TwitterApiHomeView.as_view(), name='home'),
]
