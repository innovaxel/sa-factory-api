# """
# This module defines the URL configuration for the app.

# Currently, there are no URL patterns defined for this app.
# """

# from __future__ import annotations

# from django.urls import include, path
# from rest_framework.routers import DefaultRouter

# from jobs.views import (
#     ChipViewSet,
#     CustomerViewSet,
#     ErrorCategoryViewSet,
#     ErrorSubCategoryViewSet,
#     JobAddressViewSet,
#     JobViewSet,
#     LocationViewSet,
#     WorkListViewSet,
#     JobByWorkListView,
#     JobLogView,
#     UserJobsView,
#     TimesheetViewSet,
#     UserWorkTimeView,
#     JobSubmissionViewSet,
#     ErrorViewSet,
#     JobDetailView,
# )

# router = DefaultRouter()
# router.register(r"locations", LocationViewSet, basename="location")
# router.register(r"worklists", WorkListViewSet, basename="worklist")
# router.register(r"jobaddresses", JobAddressViewSet, basename="jobaddress")
# router.register(r"customers", CustomerViewSet, basename="customer")
# router.register(r"jobs", JobViewSet, basename="job")
# router.register(r"chips", ChipViewSet, basename="chip")
# router.register(r"timesheets", TimesheetViewSet, basename="timesheet")
# router.register(
#     r"error-categories",
#     ErrorCategoryViewSet,
#     basename="error-category",
# )
# router.register(
#     r"error-subcategories",
#     ErrorSubCategoryViewSet,
#     basename="error-subcategory",
# )
# router.register(
#     r"job-submissions", JobSubmissionViewSet, basename="job-submission"
# )
# router.register(r"errors", ErrorViewSet, basename="error")

# urlpatterns = [
#     path("", include(router.urls)),
#     path("jobs/<uuid:job_id>/users/", JobLogView.as_view(), name="job-users"),
#     path("users/jobs/", UserJobsView.as_view(), name="user-jobs"),
# path(
#     "worklist/<uuid:worklist_id>/jobs/",
#     JobByWorkListView.as_view(),
#     name="jobs-by-worklist",
# ),
#     path("user-work-time/", UserWorkTimeView.as_view(), name="user-work-time"),
#     path(
#         "job-detail/<uuid:job_id>/", JobDetailView.as_view(), name="job-detail"
#     ),
# ]


# jobs/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ResourceGroupViewSet,
    BranchListView,
    ResourceGroupListView,
    AsanaTaskListView,
    AsanaTaskByWorklistView,
    JobTrackingView,
)

router = DefaultRouter()
router.register(r"resource-groups", ResourceGroupViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path(
        "resource-groups/",
        ResourceGroupListView.as_view(),
        name="resource-group-list",
    ),
    path(
        "worklist/<int:worklist_id>/jobs/",
        AsanaTaskByWorklistView.as_view(),
        name="asana-task-by-worklist",
    ),
    path("branches/", BranchListView.as_view(), name="branch-list"),
    path("asana-tasks/", AsanaTaskListView.as_view(), name="asana-task-list"),
    path("timesheets/", JobTrackingView.as_view(), name="timesheets"),
]
