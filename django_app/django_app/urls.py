from django.urls import include, path
from rest_framework import routers
from rest_framework.authtoken import views as token_views
from rawfood import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'ingredients', views.IngredientViewSet)
router.register(r'units', views.UnitViewSet)
router.register(r'utensils', views.UtensilViewSet)
router.register(r'receipes', views.ReceipeViewSet)
router.register(r'receipe_entries', views.ReceipeEntryViewSet)
router.register(r'receipe_steps', views.ReceipeStepViewSet)
router.register(r'receipe_step_entries', views.ReceipeStepEntryViewSet)
router.register(r'meals', views.MealViewSet)
router.register(r'meal_steps', views.MealStepViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    
    # POST with {"username": "xx", "password": "xx"}
    # Ensuite, ajouter le header suivant
    # Authorization: Token [TOEKN_ID]
    path('api-token-auth/', token_views.obtain_auth_token)
]
