"""
This module defines the URL configuration for the app.

Currently, there are no URL patterns defined for this app.
"""
from __future__ import annotations

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from jobs.views import (
    ChipViewSet,
    CustomerViewSet,
    ErrorCategoryViewSet,
    ErrorSubCategoryViewSet,
    JobAddressViewSet,
    JobViewSet,
    LocationViewSet,
    WorkListViewSet,
)

router = DefaultRouter()
router.register(r'locations', LocationViewSet, basename='location')
router.register(r'worklists', WorkListViewSet, basename='worklist')
router.register(r'jobaddresses', JobAddressViewSet, basename='jobaddress')
router.register(r'customers', CustomerViewSet, basename='customer')
router.register(r'jobs', JobViewSet, basename='job')
router.register(r'chips', ChipViewSet, basename='chip')
router.register(
    r'error-categories', ErrorCategoryViewSet,
    basename='error-category',
)
router.register(
    r'error-subcategories', ErrorSubCategoryViewSet,
    basename='error-subcategory',
)

urlpatterns = [
    path('', include(router.urls)),
]
