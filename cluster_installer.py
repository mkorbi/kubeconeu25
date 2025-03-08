import os
from utils import *

# Delete cluster first, in case this is a re-run
run_command(["kind", "delete", "cluster"])


# Find and replace GITHUB_DOT_COM_REPO_PLACEHOLDER with real text eg. "https://github.com/yourOrg/yourRepo.git"
do_file_replace(pattern="./**/*.y*ml", find_string="GITHUB_DOT_COM_REPO_PLACEHOLDER", replace_string=GITHUB_DOT_COM_REPO, recursive=True)
do_file_replace(pattern="./**/*.json", find_string="GITHUB_DOT_COM_REPO_PLACEHOLDER", replace_string=GITHUB_DOT_COM_REPO, recursive=True)
git_commit(target_file="-A", commit_msg="update GITHUB_DOT_COM_REPO_PLACEHOLDER", push=False)

# Find and replace GITHUB_REPOSITORY_PLACEHOLDER with real text. eg "yourOrg/yourRepo"
do_file_replace(pattern="./**/*.y*ml", find_string="GITHUB_REPOSITORY_PLACEHOLDER", replace_string=GITHUB_ORG_SLASH_REPOSITORY, recursive=True)
do_file_replace(pattern="./**/*.json", find_string="GITHUB_REPOSITORY_PLACEHOLDER", replace_string=GITHUB_ORG_SLASH_REPOSITORY, recursive=True)
do_file_replace(pattern="./apptemplates/docs/*.md", find_string="GITHUB_REPOSITORY_PLACEHOLDER", replace_string=GITHUB_ORG_SLASH_REPOSITORY, recursive=False)
git_commit(target_file="-A", commit_msg="update GITHUB_REPOSITORY_PLACEHOLDER", push=False)

# Find and replace GITHUB_REPO_NAME_PLACEHOLDER with real text. eg. `yourRepo`
do_file_replace(pattern="./**/*.y*ml", find_string="GITHUB_REPO_NAME_PLACEHOLDER", replace_string=GITHUB_REPO_NAME, recursive=True)
do_file_replace(pattern="./**/*.json", find_string="GITHUB_REPO_NAME_PLACEHOLDER", replace_string=GITHUB_REPO_NAME, recursive=True)
git_commit(target_file="-A", commit_msg="update GITHUB_REPO_NAME_PLACEHOLDER", push=False)

github_org = get_github_org(github_repo=GITHUB_ORG_SLASH_REPOSITORY)
# Find and replace GITHUB_ORG_NAME_PLACEHOLDER with real text. eg. `yourOrg`
do_file_replace(pattern="./**/*.y*ml", find_string="GITHUB_ORG_NAME_PLACEHOLDER", replace_string=github_org, recursive=True)
do_file_replace(pattern="./**/*.json", find_string="GITHUB_ORG_NAME_PLACEHOLDER", replace_string=github_org, recursive=True)
git_commit(target_file="-A", commit_msg="update GITHUB_ORG_NAME_PLACEHOLDER", push=False)

# Find and replace CODESPACE_NAME_PLACEHOLDER with real text. eg. `fantastic-onion-123ab233`
do_file_replace(pattern="./**/*.y*ml", find_string="CODESPACE_NAME_PLACEHOLDER", replace_string=CODESPACE_NAME, recursive=True)
do_file_replace(pattern="./**/*.json", find_string="CODESPACE_NAME_PLACEHOLDER", replace_string=CODESPACE_NAME, recursive=True)
do_file_replace(pattern="./apptemplates/docs/*.md", find_string="CODESPACE_NAME_PLACEHOLDER", replace_string=CODESPACE_NAME, recursive=False)
git_commit(target_file="-A", commit_msg="update CODESPACE_NAME_PLACEHOLDER", push=False)

# Find and replace DEMO_APP_PORT_NUMBER_PLACEHOLDER with real text. eg. `80`
do_file_replace(pattern="./**/*.y*ml", find_string="DEMO_APP_PORT_NUMBER_PLACEHOLDER", replace_string=f"{DEMO_APP_PORT_NUMBER}", recursive=True)
do_file_replace(pattern="./**/*.json", find_string="DEMO_APP_PORT_NUMBER_PLACEHOLDER", replace_string=f"{DEMO_APP_PORT_NUMBER}", recursive=True)
git_commit(target_file="-A", commit_msg="update DEMO_APP_PORT_NUMBER_PLACEHOLDER", push=False)

# Find and replace GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN_PLACEHOLDER with real text. eg. `.app.github.dev`
do_file_replace(pattern="./**/*.y*ml", find_string="GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN_PLACEHOLDER", replace_string=GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN, recursive=True)
do_file_replace(pattern="./**/*.json", find_string="GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN_PLACEHOLDER", replace_string=GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN, recursive=True)
do_file_replace(pattern="./apptemplates/docs/*.md", find_string="GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN_PLACEHOLDER", replace_string=GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN, recursive=False)
git_commit(target_file="-A", commit_msg="update GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN_PLACEHOLDER", push=True)

## Lets get started with Kind
# Create cluster
output = run_command(["kind", "create", "cluster", "--config", ".devcontainer/kind-cluster.yml", "--wait", STANDARD_TIMEOUT])

# Create namespaces
namespaces = ["gateway", "opentelemetry"]

for namespace in namespaces:
    output = run_command(["kubectl", "create", "namespace", namespace])

# Send startup ping
send_startup_ping()
