from django.urls import path
from users.views import UploadUserView

urlpatterns = [
    path('upload-users/', UploadUserView.as_view(),name='upload-users'),
]