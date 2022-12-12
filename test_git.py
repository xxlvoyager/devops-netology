import os
from github import Github
from dotenv import load_dotenv


load_dotenv() 

g = Github(os.getenv('key'))


repo = g.get_repo("xxlvoyager/ugc_sprint_2")
body = '''
    SUMMARY
    Change HTTP library used to send requests

    TESTS
    - [x] Send 'GET' request
    - [x] Send 'POST' request with/without body
    '''
pr = repo.create_pull(title="Use 'requests' instead of 'httplib'", body=body, head="issue", base="main")
pr


