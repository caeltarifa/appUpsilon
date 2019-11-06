from django.conf.urls import url

from apps.plan_vuelo.views import view_plan_vuelo, view_admin # view_form_plan_vuelo, post_new, post_detail

urlpatterns = [
    url(r'^$',view_plan_vuelo, name='index_plan'),
    # url(r'^nuevo$',view_form_plan_vuelo, name='form_plan_vuelo'),
    # url(r'^postnew/', post_new, name='post_new'),
    # url(r'^postdetail/<int:pk>/', post_detail , name='post_detail'),
    url(r'^admin$',view_admin, name='view_admin'),
]