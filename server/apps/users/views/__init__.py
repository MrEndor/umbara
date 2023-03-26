from server.apps.users.views.axes import unlock
from server.apps.users.views.detail import user_detail
from server.apps.users.views.list import user_list
from server.apps.users.views.profile import change_profile, profile
from server.apps.users.views.sing_up import activate_user, create_signup, signup

__all__ = (
    'user_detail',
    'create_signup',
    'change_profile',
    'activate_user',
    'user_list',
    'signup',
    'profile',
    'unlock',
)
