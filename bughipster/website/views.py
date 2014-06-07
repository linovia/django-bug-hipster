"""
bughipster.website.views
~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2014 by Xavier Ordoquy, see AUTHORS for more details.
:license: BSD, see LICENSE for more details.
"""

from django import http
from django.views import generic
from django.core.urlresolvers import reverse

from bughipster.project import models, filters


class ToDo(generic.TemplateView):
    template_name = 'todo.html'


class Error(generic.TemplateView):
    template_name = 'error.html'
    message = None

    def get_context_data(self, **kwargs):
        result = super(Error, self).get_context_data(**kwargs)
        result['message'] = self.message
        return result


class Home(generic.TemplateView):
    template_name = 'home.html'

    def get(self, request, *args, **kwargs):
        if 'logout' in self.request.GET:
            return http.HttpResponseRedirect(reverse('logout'))
        if self.request.GET:
            raise ValueError(self.request.GET)
        return super(Home, self).get(request, *args, **kwargs)


class UnconfiguredHome(generic.TemplateView):
    template_name = 'unconfigured.html'


class CreateAccount(generic.TemplateView):
    template_name = 'create_account.html'


class SimpleQuery(generic.TemplateView):
    template_name = 'simple_search.html'

    def get_context_data(self, **kwargs):
        result = super(SimpleQuery, self).get_context_data(**kwargs)
        # f = ProductFilter(request.GET, queryset=Product.objects.all())
        result['form'] = filters.SimpleQuery({}, queryset=models.Bug.objects.all()).form
        return result


#
# Complex query page helpers
#

SUMMARY_TYPE = (
    ("allwordssubstr", "contains all of the strings"), 
    ("anywordssubstr", "contains any of the strings"), 
    ("substring",      "contains the string"), 
    ("casesubstring",  "contains the string (exact case)"), 
    ("allwords",       "contains all of the words"), 
    ("anywords",       "contains any of the words"), 
    ("regexp",         "matches regular expression"), 
    ("notregexp",      "does not match regular expression"), 
)


BUG_INCLUSION_TYPE = (
    ("anyexact", "only included in"),
    ("nowords", "excluded from"),
)


EMAIL_TYPE = (
    ("substring", "contains"),
    ("notsubstring", "doesn't contain"),
    ("exact", "is"),
    ("notequals", "is not"),
    ("regexp", "matches regexp"),
    ("notregexp", "doesn't match regexp"),
)


BUG_TYPE = (
    ("noop", "---"),
    ("equals", "is equal to"),
    ("notequals", "is not equal to"),
    ("anyexact", "is equal to any of the strings"),
    ("substring", "contains the string"),
    ("casesubstring", "contains the string (exact case)"),
    ("notsubstring", "does not contain the string"),
    ("anywordssubstr", "contains any of the strings"),
    ("allwordssubstr", "contains all of the strings"),
    ("nowordssubstr", "contains none of the strings"),
    ("regexp", "matches regular expression"),
    ("notregexp", "does not match regular expression"),
    ("lessthan", "is less than"),
    ("lessthaneq", "is less than or equal to"),
    ("greaterthan", "is greater than"),
    ("greaterthaneq", "is greater than or equal to"),
    ("anywords", "contains any of the words"),
    ("allwords", "contains all of the words"),
    ("nowords", "contains none of the words"),
    ("changedbefore", "changed before"),
    ("changedafter", "changed after"),
    ("changedfrom", "changed from"),
    ("changedto", "changed to"),
    ("changedby", "changed by"),
    ("matches", "matches"),
    ("notmatches", "does not match"),
)

CUSTOM_SEARCH = (
    ("noop", "---"),
    ("alias", "Alias"),
    ("assigned_to", "Assignee"),
    ("attachments.submitter", "Attachment creator"),
    ("attach_data.thedata", "Attachment data"),
    ("attachments.description", "Attachment description"),
    ("attachments.filename", "Attachment filename"),
    ("attachments.isobsolete", "Attachment is obsolete"),
    ("attachments.ispatch", "Attachment is patch"),
    ("attachments.isprivate", "Attachment is private"),
    ("attachments.mimetype", "Attachment mime type"),
    ("blocked", "Blocks"),
    ("bug_id", "Bug ID"),
    ("cc", "CC"),
    ("cclist_accessible", "CC list accessible"),
    ("classification", "Classification"),
    ("longdesc", "Comment"),
    ("longdescs.isprivate", "Comment is private"),
    ("commenter", "Commenter"),
    ("component", "Component"),
    ("content", "Content"),
    ("creation_ts", "Creation date"),
    ("days_elapsed", "Days since bug changed"),
    ("dependson", "Depends on"),
    ("everconfirmed", "Ever confirmed"),
    ("requestees.login_name", "Flag Requestee"),
    ("setters.login_name", "Flag Setter"),
    ("flagtypes.name", "Flags"),
    ("bug_group", "Group"),
    ("keywords", "Keywords"),
    ("delta_ts", "Changed"),
    ("longdescs.count", "Number of Comments"),
    ("op_sys", "OS"),
    ("rep_platform", "Hardware"),
    ("priority", "Priority"),
    ("product", "Product"),
    ("qa_contact", "QA Contact"),
    ("reporter", "Reporter"),
    ("reporter_accessible", "Reporter accessible"),
    ("resolution", "Resolution"),
    ("see_also", "See Also"),
    ("bug_severity", "Severity"),
    ("bug_status", "Status"),
    ("status_whiteboard", "Whiteboard"),
    ("short_desc", "Summary"),
    ("tag", "Tags"),
    ("target_milestone", "Target Milestone"),
    ("owner_idle_time", "Time Since Assignee Touched"),
    ("bug_file_loc", "URL"),
    ("version", "Version"),
)


def item_per_project(items):
    """
    Create a dictionary of {project_id: [item_ids]} which allows the page
    to show/hide items according to the project id.

    - items is a list of item
    - item must have an id
    - item must have an associated project
    """
    result = {}
    for item in items:
        result.setdefault(item.product_id, []).append(item.id)
    return result


def remove_duplicates(items):
    """
    Remove duplicated names from the available choices.
    Returns the cleaned list and the duplicates dictionary
    """
    items_map = {}
    duplicates = {}
    duplicates_count = {}

    for item in items:
        items_map.setdefault(item.value, []).append(item.id)

    for grouped_items in items_map.values():
        if len(grouped_items) > 1:
            reference = grouped_items.pop()
            local_dict = dict((item, reference) for item in grouped_items)
            duplicates.update(local_dict)
            duplicates_count[reference] = len(local_dict)
    return {
        'duplicates': duplicates,
        'count': duplicates_count,
    }


class ComplexQuery(generic.TemplateView):
    template_name = 'complex_search.html'

    def get_context_data(self, **kwargs):
        result = super(ComplexQuery, self).get_context_data(**kwargs)

        # Generic data
        result['statuses'] = list(models.Status.objects.all().order_by('sortkey', 'value'))
        result['resolutions'] = list(models.Resolution.objects.all().order_by('sortkey', 'value').distinct())
        result['severities'] = list(models.Severity.objects.all().order_by('sortkey', 'value'))
        result['priorities'] = list(models.Priority.objects.all().order_by('sortkey', 'value'))
        result['hardwares'] = list(models.Hardware.objects.all().order_by('sortkey', 'value'))
        result['osses'] = list(models.OS.objects.all().order_by('sortkey', 'value'))

        # TODO: Check project's permission.
        result['projects'] = list(models.Product.objects.all().order_by('name'))
        result['components'] = list(models.Component.objects.all().order_by('product__id', 'name').distinct())
        result['versions'] = list(models.Version.objects.all().order_by('id').distinct())
        result['milestones'] = list(models.Milestone.objects.all().order_by('sortkey', 'value').distinct())

        # Sort the components/version/other per project
        result['per_project'] = {}
        result['duplicates'] = {}
        for key in ['components', 'versions', 'milestones']:
            duplicates = remove_duplicates(result[key])
            result['per_project'][key] = item_per_project(result[key])
            result['duplicates'][key] = duplicates
            result[key] = [v for v in result[key] if v.id not in duplicates['duplicates']]

        result['SUMMARY_TYPE'] = SUMMARY_TYPE
        result['BUG_TYPE'] = BUG_TYPE
        result['EMAIL_TYPE'] = EMAIL_TYPE
        result['BUG_INCLUSION_TYPE'] = BUG_INCLUSION_TYPE
        result['CUSTOM_SEARCH'] = CUSTOM_SEARCH

        # Filter the various values based on authorized projects.
        return result


def query(request, *args, **kwargs):
    view_type = request.GET.get('format', 'specific')
    if view_type == 'specific':
        return SimpleQuery.as_view()(request, *args, **kwargs)
    elif view_type == 'advanced':
        return ComplexQuery.as_view()(request, *args, **kwargs)

    error_message =  """The requested format <em>%s</em> does not exist with
    a content type of <em>html</em>.""" % (view_type,)

    return Error.as_view(message=error_message)(request, *args, **kwargs)
