from django.urls import include, path
from rest_framework import routers
from rest_framework.authtoken import views as token_views
from rest_framework.schemas import get_schema_view

from rawfood import views


# Simple routes
router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'units', views.UnitViewSet)
router.register(r'aliments', views.AlimentViewSet)
router.register(r'utensils', views.UtensilViewSet)
router.register(r'receipes', views.ReceipeViewSet)
router.register(r'receipe-step-receipes', views.ReceipeStepReceipeViewSet)
router.register(r'receipe-step-aliments', views.ReceipeStepAlimentViewSet)
router.register(r'receipe-steps', views.ReceipeStepViewSet)
router.register(r'meals', views.MealViewSet)
router.register(r'meal-receipes', views.MealReceipeViewSet)
router.register(r'meal-aliments', views.MealAlimentViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    
    # POST with {"username": "xx", "password": "xx"}
    # Ensuite, ajouter le header suivant
    # Authorization: Token [TOEKN_ID]
    path('api-token-auth/', token_views.obtain_auth_token),

    path('openapi', get_schema_view(
        title="Your Project",
        description="API for all things …"
    ), name='openapi-schema'),
]
