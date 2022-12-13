#!/usr/bin/env python3

import json
import os
import re
import sys
from  datetime import datetime
from github import Github
from dotenv import load_dotenv
from git import Repo


load_dotenv() 


if len(sys.argv) != 2:
    print('Error: Wrong argumets')
    exit(1)

git_path = '{}/.git'.format(sys.path[0])

commit_message = sys.argv[1]

# pull_request the same neame of commit

pull_request = commit_message

repo = Repo(git_path)
origin = repo.remote(name='origin')
origin.pull()
original_branch = repo.active_branch
branch_name = 'feature/{}'.format(hash(datetime.now()))
branch = repo.create_head(branch_name)
branch.checkout()
repo.git.add('.')
repo.index.commit(commit_message)
repo.git.push('--set-upstream', 'origin', branch)
original_branch.checkout()


remote_url = repo.remote().url
remote_repo = re.sub('.git','', re.sub('..*/', '', remote_url))
remote_user = re.sub('..*:','', re.sub('/..*', '', remote_url))


g = Github(os.getenv('key'))


repo_github = g.get_repo("{}/{}".format(remote_user, remote_repo))
body = '''Please pull these awesome changes in!'''

pr = repo_github.create_pull(title=pull_request, body=body, head=branch_name, base="main")
pr

