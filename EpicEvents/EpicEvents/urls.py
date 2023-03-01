"""EpicEvents URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_nested import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from api.views import ClientViewset, ContratViewset, EvenementViewset, \
    ContratFiltreViewset

client_router = routers.SimpleRouter()
client_router.register("client", ClientViewset, basename="client")

contrat_router = routers.NestedSimpleRouter(client_router, "client", lookup="client")
contrat_router.register("contrat", ContratViewset, basename="contrat")

evenement_router = routers.NestedSimpleRouter(contrat_router, "contrat", lookup="contrat")
evenement_router.register("evenement", EvenementViewset, basename="evenement")

router = routers.SimpleRouter()
router.register("contrat", ContratFiltreViewset, basename="contrat_filtre")

urlpatterns = [
    path('admin/', admin.site.urls),
    path("login/", TokenObtainPairView.as_view()),
    path("login/refresh/", TokenRefreshView.as_view()),
    path("", include(client_router.urls)),
    path("", include(contrat_router.urls)),
    path("", include(evenement_router.urls)),
    path("", include(router.urls)),
]
