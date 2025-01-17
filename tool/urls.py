from django.urls import path
from . import views

urlpatterns = [
    path('login', views.login_view, name="login"),
    path('logout', views.logout_view, name="logout"),
    path('', views.index, name="index"),
    # path('report', views.report_view, name="report"),
    path('git_process', views.git_process, name="git_process"),
    path('zip_process', views.zip_process, name="zip_process"),
    path('download-zip/<path:name>/', views.download_zip, name='download_zip'),
    path('edit_keywords/', views.edit_key_view, name='edit_keywords_dictionary'),
]
