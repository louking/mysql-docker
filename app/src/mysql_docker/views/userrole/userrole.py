'''
userrole - specific user/role management for this application

This provides global access to users, interests, roles tables
'''

# homegrown
from mysql_docker import user_datastore
from ...version import __docversion__
from loutilities.user.views.userrole import UserView, InterestView, RoleView

superadminguide = f'https://mysql-docker.readthedocs.io/en/{__docversion__}/super-admin-guide.html'

class LocalUserView(UserView):
    def editor_method_postcommit(self, form):
        pass
        # update_local_tables()
user_view = LocalUserView(
    pagename='users',
    user_datastore=user_datastore,
    roles_accepted=['super-admin'],
    endpoint='userrole.users',
    rule='/users',
    templateargs={'adminguide': superadminguide},
)
user_view.register()

class LocalInterestView(InterestView):
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        args = dict(
            templateargs={'adminguide': superadminguide},
        )
        args.update(kwargs)

        # initialize inherited class, and a couple of attributes
        super().__init__(**args)

    def editor_method_postcommit(self, form):
        pass
#         update_local_tables()
interest_view = LocalInterestView()
interest_view.register()

class LocalRoleView(RoleView):
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        args = dict(
            templateargs={'adminguide': superadminguide},
        )
        args.update(kwargs)

        # initialize inherited class, and a couple of attributes
        super().__init__(**args)

    def editor_method_postcommit(self, form):
        pass
        # update_local_tables()
role_view = LocalRoleView()
role_view.register()
