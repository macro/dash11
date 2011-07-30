from fabric.api import cd, run, sudo, env
from fabric.contrib.files import exists


env.user = 'pyrun'
env.hosts = ['gitawesome.com']

def hup():
    sudo('svc -t /etc/service/gitawesome')

def deploy(hard=False):
    """
    """
    with cd('/home/pyrun/dash11/dash_proj/'):
        if exists('.deploy.lck'):
            print 'ABORT: Another upgrade is in progress, exiting...'
            return
        run('touch .deploy.lck')
        run('git pull')
        run('. ../virtualenv/bin/activate && \
                pip install -r requirements_prod.txt && \
                FLAVOR=prod python manage.py migrate')
        hup()
        run('rm .deploy.lck')
