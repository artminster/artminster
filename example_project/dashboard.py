"""
This file was generated with the customdashboard management command and
contains the class for the main dashboard.

To activate your index dashboard add the following to your settings.py::
    GRAPPELLI_INDEX_DASHBOARD = 'djangogenericproject.dashboard.CustomIndexDashboard'
"""

from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from grappelli.dashboard import modules, Dashboard
from grappelli.dashboard.utils import get_admin_site_name


class CustomIndexDashboard(Dashboard):
    """
    Custom index dashboard for www.
    """
    
    def init_with_context(self, context):
        site_name = get_admin_site_name(context)
        
        # append an app list module for "Applications"
        self.children.append(modules.Group(
            _('projectname'),
            collapsible=True,
            column=1,
            children = [
                modules.ModelList(
                    _('App Name'),
                    css_classes=('collapse',),
                    models=('apps.appname.models.*',),
                ),
            ]
        ))
        
        self.children.append(modules.ModelList(
            _('Billing'),
            collapsible=True,
            column=1,
            models=('artminster.contrib.billing.models.*',),
        ))
        
        self.children.append(modules.Group(
            _('CMS & Site Content'),
            column=1,
            css_classes=('grp-open',),
            children = [
                modules.ModelList(
                    _('CMS'),
                    css_classes=('collapse',),
                    models=('cms.*',),
                ),
                modules.ModelList(
                    _('Content Blocks'),
                    css_classes=('collapse',),
                    models=('flatblocks.*',),
                ),
            ]
        ))
        
        self.children.append(modules.AppList(
            _('Social Signups and Authentication'),
            collapsible=True,
            column=1,
            css_classes=('grp-closed',),
            models=('allauth.*','emailconfirmation.*',),
        ))
        
        self.children.append(modules.AppList(
            _('Site Administration'),
            collapsible=True,
            column=1,
            css_classes=('grp-closed',),
            models=('django.contrib.*',),
        ))
        
        # append another link list module for "support".
        self.children.append(modules.LinkList(
            _('Media Management'),
            column=2,
            children=[
                {
                    'title': _('File Browser'),
                    'url': '/admin/filebrowser/browse/',
                    'external': False,
                },
            ]
        ))
        
        # append another link list module for "support".
        self.children.append(modules.LinkList(
            _('Getting In Touch With ARTMINSTER'),
            column=2,
            children=[
                {
                    'title': _('Technical Support'),
                    'url': 'mailto:support@artminster.com',
                    'external': True,
                },
                {
                    'title': _('Sales'),
                    'url': 'mailto:sales@artminster.com',
                    'external': True,
                },
                {
                    'title': _('View our up-to-date portfolio'),
                    'url': 'http://www.artminster.com/our-work/',
                    'external': True,
                },
            ]
        ))
        
        # append a feed module
        self.children.append(modules.Feed(
            _('Latest ARTMINSTER News'),
            column=2,
            feed_url='http://www.artminster.com/feeds/news/',
            limit=5
        ))
        
        # append a recent actions module
        self.children.append(modules.RecentActions(
            _('Recent Actions'),
            limit=5,
            collapsible=False,
            column=3,
        ))


