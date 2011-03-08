import unipath
from fabric.api import *
from fabric.contrib import project

env.hosts      = ['jacobian.org']
env.user       = 'root'
env.venv       = unipath.Path('/home/web/venvs/djangome')
env.deployroot = unipath.Path('/home/web/djangome')

def deploy():
    deploy_code()
    run('kill -HUP `cat /var/run/djangome.pid`')

def deploy_code():
    project.rsync_project(env.deployroot.parent, delete=True, exclude=['*.pyc'])
    
def update_deps():
    run('%s/bin/pip install -r %s/requirements.txt' % (env.venv, env.deployroot))
    
def refresh_objects():
    run('%s/bin/python %s/manage.py refresh_objects' % (env.venv, env.deployroot))