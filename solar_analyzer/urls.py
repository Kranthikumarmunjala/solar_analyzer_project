"""
URL configuration for solar_analyzer project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
# from django.contrib import admin
# from django.urls import path
# from analysis.views import SiteAnalysisView

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('api/sites/', SiteAnalysisView.as_view(), name='site-analysis'),
# ]


from django.contrib import admin
from django.urls import path
from analysis.views import SiteAnalysisView, StatisticsView

urlpatterns = [
    path('admin/', admin.site.urls),
    # Handles list and post
    path('api/sites/', SiteAnalysisView.as_view(), name='site-list'),
    # Handles single site details (Requirement: GET /api/sites/{id})
    path('api/sites/<int:pk>/', SiteAnalysisView.as_view(), name='site-detail'),
    # Handles statistics (Requirement: GET /api/statistics)
    path('api/statistics/', StatisticsView.as_view(), name='site-stats'),
]