from fabric.api import cd, run, sudo, env
from fabric.contrib.files import exists


env.user = 'pyrun'
env.hosts = ['gitawesome.com']

def hup():
    sudo('svc -t /etc/service/gitawesome')
    sudo('svc -t /etc/service/celeryd')

def cleanup():
    with cd('/home/pyrun/dash11/dash_proj/'):
        if exists('.deploy.lck'):
            run('rm -rf .deploy.lck')

def deploy(hard=False):
    """
    """
    with cd('/home/pyrun/dash11/dash_proj/'):
        if exists('.deploy.lck'):
            print 'ABORT: Another upgrade is in progress, exiting...'
            return
        run('touch .deploy.lck')
        run('git fetch')
        run('git reset --hard origin/master')
        sudo('git clean -f -d')
        run('. ../virtualenv/bin/activate && \
                pip install -r requirements_prod.txt && \
                FLAVOR=prod python manage.py collectstatic --noinput && \
                FLAVOR=prod python manage.py migrate')
        hup()
