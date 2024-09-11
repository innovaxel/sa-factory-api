"""
Django admin configuration for managing the Chip model.
"""
from __future__ import annotations

from django.contrib import admin

from jobs.models import Chip
from jobs.models import Customer
from jobs.models import Error
from jobs.models import ErrorCategory
from jobs.models import ErrorSubCategory
from jobs.models import Job
from jobs.models import JobAddress
from jobs.models import JobLog
from jobs.models import JobSubmission
from jobs.models import Location
from jobs.models import Media
from jobs.models import TeamMember
from jobs.models import Timesheet
from jobs.models import WorkList


class ChipAdmin(admin.ModelAdmin):
    """
    Custom admin configuration for the Chip model.

    This class defines how the Chip model is displayed and managed in
    the Django admin interface,
    including the fields to be displayed, searchable, and filterable.
    """
    list_display = ('id', 'color', 'text', 'icon')
    search_fields = ('color', 'text', 'id')
    list_filter = ('color',)
    ordering = ('color',)
    readonly_fields = ('id',)

    def get_readonly_fields(self, request, obj=None):
        """
        Return a list of fields that are read-only in the admin interface.

        For the Chip model, the ID field is always read-only.
        """
        return self.readonly_fields


class CustomerAdmin(admin.ModelAdmin):
    """
    Custom admin configuration for the Customer model.

    This class defines how the Customer model is
    displayed and managed in the Django admin interface,
    including the fields to be displayed, searchable, and filterable.
    """
    list_display = ('id', 'name')
    search_fields = ('name', 'id')
    ordering = ('name',)
    readonly_fields = ('id',)

    def get_readonly_fields(self, request, obj=None):
        """
        Return a list of fields that are read-only in the admin interface.

        For the Customer model, the ID field is always read-only.
        """
        return self.readonly_fields


class ErrorCategoryAdmin(admin.ModelAdmin):
    """
    Custom admin configuration for the ErrorCategory model.

    This class defines how the ErrorCategory model is displayed
    and managed in the Django admin interface,
    including the fields to be displayed, searchable, and filterable.
    """
    list_display = ('id', 'name', 'code')
    search_fields = ('name', 'code', 'id')
    ordering = ('name',)
    readonly_fields = ('id',)

    def get_readonly_fields(self, request, obj=None):
        """
        Return a list of fields that are read-only in the admin interface.

        For the ErrorCategory model, the ID field is always read-only.
        """
        return self.readonly_fields


class ErrorSubCategoryAdmin(admin.ModelAdmin):
    """
    Custom admin configuration for the ErrorSubCategory model.

    This class defines how the ErrorSubCategory model is
    displayed and managed in the Django admin interface,
    including the fields to be displayed, searchable, and filterable.
    """
    list_display = ('id', 'name', 'code', 'error_category')
    search_fields = ('name', 'code', 'id', 'error_category__name')
    list_filter = ('error_category',)
    ordering = ('name',)
    readonly_fields = ('id',)

    def get_readonly_fields(self, request, obj=None):
        """
        Return a list of fields that are read-only in the admin interface.

        For the ErrorSubCategory model, the ID field is always read-only.
        """
        return self.readonly_fields


class ErrorAdmin(admin.ModelAdmin):
    """
    Custom admin configuration for the Error model.

    This class defines how the Error model is displayed and managed
    in the Django admin interface,
    including the fields to be displayed, searchable, and filterable.
    """
    list_display = ('id', 'errorsubcategory', 'comment', 'user', 'job')
    search_fields = (
        'comment', 'user__username',
        'job__id', 'errorsubcategory__name',
    )
    list_filter = ('errorsubcategory', 'user', 'job')
    ordering = ('-id',)
    readonly_fields = ('id',)

    def get_readonly_fields(self, request, obj=None):
        """
        Return a list of fields that are read-only in the admin interface.

        For the Error model, the ID field is always read-only.
        """
        return self.readonly_fields


class JobAddressAdmin(admin.ModelAdmin):
    """
    Custom admin configuration for the JobAddress model.

    This class defines how the JobAddress model is displayed
    and managed in the Django admin interface,
    including the fields to be displayed, searchable, and filterable.
    """
    list_display = ('id', 'address', 'latitude', 'longitude')
    search_fields = ('address', 'id')
    ordering = ('address',)
    readonly_fields = ('id',)

    def get_readonly_fields(self, request, obj=None):
        """
        Return a list of fields that are read-only in the admin interface.

        For the JobAddress model, the ID field is always read-only.
        """
        return self.readonly_fields


class JobLogAdmin(admin.ModelAdmin):
    """
    Custom admin configuration for the JobLog model.

    This class defines how the JobLog model is displayed and managed
    in the Django admin interface,
    including the fields to be displayed, searchable, and filterable.
    """
    list_display = ('id', 'user', 'job', 'created_at')
    search_fields = ('user__username', 'job__id', 'created_at')
    list_filter = ('created_at',)
    ordering = ('-created_at',)
    readonly_fields = ('id', 'created_at')

    def get_readonly_fields(self, request, obj=None):
        """
        Return a list of fields that are read-only in the admin interface.

        For the JobLog model, the ID and created_at fields are always read-only.
        """
        return self.readonly_fields


class JobSubmissionAdmin(admin.ModelAdmin):
    """
    Custom admin configuration for the JobSubmission model.

    This class defines how the JobSubmission model is displayed
    and managed in the Django admin interface,
    including the fields to be displayed, searchable, and filterable.
    """
    list_display = ('id', 'comment', 'user', 'job')
    search_fields = ('comment', 'user__username', 'job__id', 'id')
    list_filter = ('user', 'job')
    ordering = ('-id',)
    readonly_fields = ('id',)

    def get_readonly_fields(self, request, obj=None):
        """
        Return a list of fields that are read-only in the admin interface.

        For the JobSubmission model, the ID field is always read-only.
        """
        return self.readonly_fields


class JobAdmin(admin.ModelAdmin):
    """
    Custom admin configuration for the Job model.

    This class defines how the Job model is displayed and managed
    in the Django admin interface,
    including the fields to be displayed, searchable, and filterable.
    """
    list_display = (
        'id', 'name', 'number', 'customerid',
        'worklistid', 'chip', 'address_id',
    )
    search_fields = (
        'name', 'number', 'customerid__name',
        'worklistid__name', 'chip__text', 'address_id__address',
    )
    list_filter = ('customerid', 'worklistid', 'chip', 'address_id')
    ordering = ('-number',)
    readonly_fields = ('id',)

    def get_readonly_fields(self, request, obj=None):
        """
        Return a list of fields that are read-only in the admin interface.

        For the Job model, the ID field is always read-only.
        """
        return self.readonly_fields


class LocationAdmin(admin.ModelAdmin):
    """
    Custom admin configuration for the Location model.

    This class defines how the Location model is displayed
    and managed in the Django admin interface,
    including the fields to be displayed, searchable, and filterable.
    """
    list_display = ('id', 'name')
    search_fields = ('name', 'id')
    ordering = ('name',)
    readonly_fields = ('id',)

    def get_readonly_fields(self, request, obj=None):
        """
        Return a list of fields that are read-only in the admin interface.

        For the Location model, the ID field is always read-only.
        """
        return self.readonly_fields


class MediaAdmin(admin.ModelAdmin):
    """
    Custom admin configuration for the Media model.

    This class defines how the Media model is displayed and managed
    in the Django admin interface,
    including the fields to be displayed, searchable, and filterable.
    """
    list_display = ('id', 'resource_id', 'image')
    search_fields = ('resource_id', 'id')
    readonly_fields = ('id',)
    ordering = ('-id',)

    def get_readonly_fields(self, request, obj=None):
        """
        Return a list of fields that are read-only in the admin interface.

        For the Media model, the ID field is always read-only.
        """
        return self.readonly_fields


class TeamMemberAdmin(admin.ModelAdmin):
    """
    Custom admin configuration for the TeamMember model.

    This class defines how the TeamMember model is displayed and managed 
    in the Django admin interface,
    including the fields to be displayed, searchable, and filterable.
    """
    list_display = ('id', 'user', 'worklist')
    search_fields = ('user__username', 'worklist__name', 'id')
    list_filter = ('user', 'worklist')
    ordering = ('-id',)
    readonly_fields = ('id',)

    def get_readonly_fields(self, request, obj=None):
        """
        Return a list of fields that are read-only in the admin interface.

        For the TeamMember model, the ID field is always read-only.
        """
        return self.readonly_fields


class TimesheetAdmin(admin.ModelAdmin):
    """
    Custom admin configuration for the Timesheet model.

    This class defines how the Timesheet model is displayed and managed
    in the Django admin interface,
    including the fields to be displayed, searchable, and filterable.
    """
    list_display = ('id', 'user', 'action', 'timestamp')
    search_fields = ('user__username', 'action', 'id')
    list_filter = ('action', 'user')
    ordering = ('-timestamp',)
    readonly_fields = ('id', 'timestamp')

    def get_readonly_fields(self, request, obj=None):
        """
        Return a list of fields that are read-only in the admin interface.

        For the Timesheet model, the ID and timestamp fields are always read-only.
        """
        return self.readonly_fields


class WorkListAdmin(admin.ModelAdmin):
    """
    Custom admin configuration for the WorkList model.

    This class defines how the WorkList model is displayed
    and managed in the Django admin interface,
    including the fields to be displayed, searchable, and filterable.
    """
    list_display = ('id', 'title', 'location')
    search_fields = ('title', 'id', 'location__name')
    list_filter = ('location',)
    ordering = ('-title',)
    readonly_fields = ('id',)

    def get_readonly_fields(self, request, obj=None):
        """
        Return a list of fields that are read-only in the admin interface.

        For the WorkList model, the ID field is always read-only.
        """
        return self.readonly_fields


admin.site.register(WorkList, WorkListAdmin)
admin.site.register(Timesheet, TimesheetAdmin)
admin.site.register(TeamMember, TeamMemberAdmin)
admin.site.register(Media, MediaAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Job, JobAdmin)
admin.site.register(JobSubmission, JobSubmissionAdmin)
admin.site.register(JobLog, JobLogAdmin)
admin.site.register(JobAddress, JobAddressAdmin)
admin.site.register(Error, ErrorAdmin)
admin.site.register(ErrorSubCategory, ErrorSubCategoryAdmin)
admin.site.register(ErrorCategory, ErrorCategoryAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Chip, ChipAdmin)
