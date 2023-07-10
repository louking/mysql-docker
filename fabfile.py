'''
fabfile  -- deployment using Fabric
=================================================================

expecting local fabric.json with following content
    {
        "connect_kwargs": {
            "key_filename": sshkeyfilename (export OpenSSH key from puttygen)
        },
        "user": "appuser"
    }

execute as follows

    fab -H <target-host> deploy

or 

    fab -H <target1>,<target2> deploy

if you need to check out a particular branch

    fab -H <target-host> deploy --branchname=<branch>

'''

from fabric import task
from invoke import Exit

APP_NAME = 'mysql-docker'

@task
def deploy(c, branchname='main', qualifier='prod'):
    print(f'c.user={c.user} c.host={c.host} branchname={branchname}')

    project_dir = f'/var/www/{c.host}/{APP_NAME}/{APP_NAME}'

    c.run(f'cd {project_dir} && git pull')
    
    if not c.run(f'cd {project_dir} && git show-ref --verify --quiet refs/heads/{branchname}', warn=True):
        raise Exit(f'branchname {branchname} does not exist')

    c.run(f'cd {project_dir} && git checkout {branchname}')
    
    # stop and build/start docker services
    c.run(f'cd {project_dir} && docker compose down')
    c.run(f'cd {project_dir} && docker compose -f docker-compose.yml -f docker-compose.{qualifier}.yml up --build -d')