import csv
from django.http import HttpResponse
from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Portfolio, Candidate, Voter

def export_results(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="election_results.csv"'
    writer = csv.writer(response)
    writer.writerow(['Portfolio', 'Candidate', 'Votes'])

    for portfolio in Portfolio.objects.all():
        candidates = Candidate.objects.filter(portfolio=portfolio).order_by('-votes')
        for candidate in candidates:
            writer.writerow([portfolio.name, candidate.name, candidate.votes])

    return response

export_results.short_description = "Export Election Results to CSV"

class CandidateAdmin(admin.ModelAdmin):
    list_display = ('name', 'portfolio', 'votes', 'image_tag')
    readonly_fields = ('votes', 'image_tag')  # Make the votes field read-only
    actions = [export_results]  # Add the export action to the admin interface

    def image_tag(self, obj):
        return mark_safe(f'<img src="{obj.image.url}" width="50" height="50" />')
    image_tag.short_description = 'Image'

    # Allow adding and deleting candidates, but not modifying the votes
    def get_readonly_fields(self, request, obj=None):
        if obj:  # When editing an existing object
            return ['votes', 'image_tag']
        return []

admin.site.register(Portfolio)
admin.site.register(Candidate, CandidateAdmin)
admin.site.register(Voter)
