
from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.index),
    url(r'^main$', views.index),
    url(r'^dashboard$', views.dashboard),
    url(r'^dashboard/recent$', views.dashboard_recent),
    url(r'^posts/new$', views.new_post),
    url(r'^posts/create$', views.create_post),
    url(r'^posts/(?P<id>\d+)$', views.show_post),
    url(r'^posts/(?P<id>\d+)/edit$', views.edit_post),
    url(r'^posts/edit$', views.make_edit_post),
    url(r'^posts/(?P<id>\d+)/v/(?P<vid>\d+)$', views.show_post_version),
    url(r'^posts/(?P<id>\d+)/contribute$', views.contribute),
    url(r'^posts/v/approve$', views.approve_version),
    url(r'^posts/v/reject$', views.reject_version),
    url(r'^posts/star$', views.star_post),
    url(r'^posts/unstar$', views.unstar_post),
    url(r'^posts/comment$', views.comment_post),
    url(r'^users/(?P<id>\d+)$', views.show_user),
    url(r'^logout$', views.logout),
    url(r'^process$', views.process)
]