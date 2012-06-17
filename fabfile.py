import os

from fabric.api import cd, env, get, hide, local, put, require, run, settings, sudo, task
from fabric.contrib import files, console

# Directory structure
PROJECT_ROOT = os.path.dirname(__file__)
env.user = 'letsgetlouder'
env.project = 'letsgetlouder'
env.project_user = 'letsgetlouder'
env.repo = u'git@github.com:juliaelman/letsgetlouder.git'
env.shell = '/bin/bash -c'
env.disable_known_hosts = True
env.port = '052909'
env.forward_agent = True


def setup_path():
    """Configure fabric environment."""
    env.home = '/home/%(project_user)s/' % env
    env.root = os.path.join(env.home, 'www', env.environment)
    env.code_root = os.path.join(env.root, env.project)
    env.project_root = os.path.join(env.code_root, env.project)
    env.virtualenv_root = os.path.join(env.root, 'env')
    env.static_root = os.path.join(env.code_root, 'static_root')
    env.media_root = os.path.join(env.code_root, 'media_root')
    env.log_dir = os.path.join(env.root, 'log')
    env.settings = '%(project)s.settings' % env


def venv(cmd):
    """Run binaries from within the virtualenv root."""
    if isinstance(cmd, list):
        cmd = ' '.join(cmd)
    return run('%s/bin/%s' % (env.virtualenv_root, cmd))


@task
def production():
    """Run on production environment."""
    env.environment = 'production'
    env.hosts = ['50.56.29.156']
    env.branch = 'master'
    setup_path()


@task
def update_requirements():
    """Update Python requirements."""
    require('environment')
    venv('pip install -r %s' % os.path.join(env.code_root, 'requirements/apps.txt'))


@task
def manage_run(command):
    """Run a Django management command on the server."""
    require('environment')
    if '--settings' not in command:
        command = u"%s --settings=%s" % (command, env.settings)
    venv(u'django-admin.py %s' % command)


@task
def touch():
    with cd(env.project_root):
        run('touch wsgi.py')


@task
def bootstrap():
    """Setup Django environment on server."""
    run('mkdir -p %(code_root)s' % env)
    run('mkdir -p %(log_dir)s' % env)
    run('mkdir -p %(media_root)s' % env)
    run('mkdir -p %(static_root)s' % env)
    with settings(warn_only=True):
        run('git clone %(repo)s %(code_root)s' % env)
    with cd(env.code_root):
        run('git checkout %(branch)s' % env)
    run('virtualenv -p python2.6 --clear --distribute %s' % env.virtualenv_root)
    update_requirements()
    # add project dir to Python path
    path_file = os.path.join(env.virtualenv_root, 'lib', 'python2.6',
                             'site-packages', 'project.pth')
    files.append(path_file, env.code_root)


@task
def deploy():
    """Deploy latest changes."""
    with cd(env.code_root):
        run('git pull origin')
    with cd(env.code_root):
        run('git checkout %(branch)s' % env)
    update_requirements()
    manage_run('collectstatic --noinput')
    touch()
