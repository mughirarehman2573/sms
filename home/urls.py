from django.urls import path, include

urlpatterns = [
    path('api/v1/', include('home.api.v1.urls'))
]


