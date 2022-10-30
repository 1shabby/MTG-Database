from django.urls import path, include
from . import views

router = routers.DefaultRouter()
router.register(r'legends', views.LegendView, 'legend')

urlpatterns = [
    path('', views.index, name='index'),
]