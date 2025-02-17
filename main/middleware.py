import threading
from django.utils.deprecation import MiddlewareMixin


local_var = threading.local()


class DatabaseRoutingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        branch = request.COOKIES.get("project", None)
        local_var.branch = branch


def get_current_db_name(model=None):
    branch_name = getattr(local_var, "branch", None)
    if branch_name is None:
        return None
    # if model in [LocalusersAuthdb, OnboardingUserData]:  # Auth models list
    if model.__module__ == "reports.models.auth":
        branch_name = "AUTH_" + str(branch_name)
        return branch_name
