from django.urls import include, path
from rest_framework import routers
from crusine import views

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

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/',
         include('rest_framework.urls', namespace='rest_framework'))
]
