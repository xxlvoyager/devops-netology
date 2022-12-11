#!/usr/bin/env python3
"""
this script use GitHub CLI 
to get help goto https://docs.github.com/en/rest
"""
import json
import os
import re
import sys
from  datetime import datetime

from git import Repo

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


command_chunk = ('/usr/bin/gh  api --method POST', 
                 '-H "Accept: application/vnd.github+json"',
                 '/repos/{}/{}/pulls'.format(remote_user, remote_repo),
                 '-f title="{}"'.format(pull_request),
                 '-f body="Please pull these awesome changes in!"',
                 '-f head="{}"'.format(branch_name),
                 '-f base="main"'
                 )


bash_command = ' '.join(command_chunk)

result_os = os.popen(bash_command).readlines()
result = json.loads(result_os[0])

print('Created pull request', result['url'] )
