from django.urls import path
from core import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("api/features", views.features_api, name="features-api"),
    path("api/features/<int:feature_id>", views.feature_api, name="feature-api"),
    path("api/results", views.results_api, name="results-api"),
]
