from hashlib import sha512
from console.models import BotbuilderProject
from github import Github, GithubException
from django.core.management import BaseCommand
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


def create_webhook(project_name, tenant, provider, access_token, url):
    g = Github(access_token)
    user = g.get_user()
    repo = user.get_repo(project_name)
    events = ["push"]
    secret_token = sha512(access_token.encode("utf-8")).hexdigest()
    config = {
        "url": url.format(tenant=tenant, provider=provider),
        "content_type": "json",
        "secret": secret_token,
    }
    try:
        repo.create_hook("web", config, events, active=True)
    except GithubException as e:
        print("An error occurred:", str(e))


class Command(BaseCommand):
    def handle(self, **options):
        access_token = settings.GIT_TOKEN
        projects = BotbuilderProject.objects.using("botbuilder").all()
        url = (
            f"https://{settings.DNS}/analytics-new/reports/vcs/"
            + "{provider}/{tenant}/"
        )
        for project in projects:
            try:
                create_webhook(
                    project.name, project.tenant, "github", access_token, url
                )
            except Exception as e:
                print(
                    f"Failed to update secret for project {project.repo_url} {str(e)}"
                )
