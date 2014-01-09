from datetime import timedelta
from django.core.cache import cache
from django.core.urlresolvers import reverse
from django.http import Http404
from django.shortcuts import redirect
from django.utils import timezone
from misago.apps.profiles.decorators import profile_view
from misago.apps.profiles.template import RequestContext
from misago.apps.profiles.warnings.warningstracker import WarningsTracker
from misago.shortcuts import render_to_response
from misago.utils.pagination import make_pagination

@profile_view('user_warnings')
def warnings(request, user, page=0):
    request.acl.warnings.allow_member_warns_view(request.user, user)

    queryset = user.warning_set
    count = queryset.count()
    try:
        pagination = make_pagination(page, count, 12)
    except Http404:
        return redirect(reverse('user_warnings', kwargs={'user': user.id, 'username': user.username_slug}))

    return render_to_response('profiles/warnings.html',
                              context_instance=RequestContext(request, {
                                  'profile': user,
                                  'tab': 'warnings',
                                  'items_total': count,
                                  'warning_level': user.get_current_warning_level(),
                                  'warnings_tracker': WarningsTracker(user.warning_level - pagination['start']),
                                  'items': queryset.order_by('-id')[pagination['start']:pagination['stop']],
                                  'pagination': pagination,
                                  }));