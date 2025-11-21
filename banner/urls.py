from django.urls import path
from .views import get_all_banners, get_all_active_banners, add_banner, update_banner, update_banner_publish_status, delete_banner

urlpatterns = [
    path("get_all_banners/", get_all_banners, name="get_all_banners"),
    path("get_all_active_banners/", get_all_active_banners, name="get_all_active_banners"),
    path("add_banner/", add_banner, name="add_a_banner"),
    path("update_banner/<int:pk>/", update_banner, name="update_banner"),
    path("update_banner_publish_status/<int:pk>/", update_banner_publish_status, name="update_banner_publish_status"),
    path("delete_banner/<int:pk>/", delete_banner, name="delete_banner"),
]

