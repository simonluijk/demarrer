#-*- coding:utf-8 -*-
import os
import re
import boto

from fabric.api import lcd, local, task, hide, prefix
from boto.s3.connection import Location as _Location
from boto.exception import S3CreateError as _S3CreateError
from boto.cloudfront.origin import CustomOrigin as _CustomOrigin


CLOUDFRONT_ENABLED = True
CLOUDFRONT_CUSTOM_ORIGIN = None

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
PROJECT_NAME = os.path.basename(PROJECT_ROOT).lower()
LOCAL_VENV = '$WORKON_HOME/%s' % PROJECT_NAME


@task
def setup_s3(bucket_name=None):
    """ Setup s3 instance with cloudfront distribution """
    if not bucket_name:
        bucket_name = '{0}-media'.format(PROJECT_NAME)
    conn = boto.connect_s3()
    try:
        conn.create_bucket(bucket_name, location=_Location.EU,
                           policy='public-read')
    except _S3CreateError:
        pass

    print('AWS_STORAGE_BUCKET_NAME={0}'.format(bucket_name))

    if CLOUDFRONT_ENABLED:
        try:
            origin = CLOUDFRONT_CUSTOM_ORIGIN
        except NameError:
            origin = None
        if not origin:
            origin = '{0}.s3.amazonaws.com'.format(bucket_name)

        origin = _CustomOrigin(origin, origin_protocol_policy='http-only')
        conn = boto.connect_cloudfront()
        distro = conn.create_distribution(origin=origin, enabled=True)
        print('MEDIA_DOMAIN={0}'.format(distro.domain_name))
    else:
        bucket_url = '{0}.s3.amazonaws.com'.format(bucket_name)
        print('MEDIA_DOMAIN={0}'.format(bucket_url))


@task
def freeze_requirements():
    """ Freeze python requirements into requirements.txt file """
    with lcd(PROJECT_ROOT):
        requirements = open('requirements.txt', 'r').read().split('\n')
        if len(requirements[-1]) == 0:
            requirements.pop()

        activate_path = os.path.join(LOCAL_VENV, 'bin', 'activate')
        with prefix('source "{0}"'.format(activate_path)):
            with hide('running'):
                packages = local('pip freeze --local', capture=True)
                packages = packages.split('\n')

        for pkg in packages:
            found_req = False

            try:
                pkg, version = pkg.split('==')
            except ValueError:
                print('Ignoring:\n{0}\n'.format(pkg))
                continue

            for idx, req in enumerate(requirements):
                try:
                    req, old_version = req.split('==')
                except ValueError:
                    pass
                if req.lower() == pkg.lower():
                    found_req = True
                    requirements[idx] = '%s==%s' % (pkg, version)
                    break

            if not found_req:
                msg = '## Pip frozen requirements'
                if msg not in requirements:
                    requirements.append('\n')
                    requirements.append(msg)
                requirements.append('%s==%s' % (pkg, version))

        req_file = open('requirements.txt', 'w')
        req_file.writelines(['%s\n' % r for r in requirements])


@task
def mk_venv():
    """ Build local vitualenv """
    with lcd(PROJECT_ROOT):
        local('rm -rf "{0}"'.format(LOCAL_VENV))
        local('virtualenv "{0}"'.format(LOCAL_VENV))
        activate_path = os.path.join(LOCAL_VENV, 'bin', 'activate')
        with prefix('source "{0}"'.format(activate_path)):
            local('pip install -r requirements.txt')


VM_RE = re.compile(r'"([^"]+)"\s\{([^\}]+)\}')


@task
def set_vagrant_id():
    """ Set vagrant machine id if already created. """
    new_vm_id = None
    vms = local('vboxmanage list vms', capture=True)
    match = VM_RE.findall(vms)
    if match:
        for vm_name, vm_id in match:
            if vm_name.startswith('{0}_default_'.format(PROJECT_NAME)):
                new_vm_id = vm_id

    if new_vm_id:
        with lcd(PROJECT_ROOT):
            directory = '.vagrant/machines/default/virtualbox'
            local('mkdir -p {0}'.format(directory))
            local('echo "{0}" > {1}/id'.format(new_vm_id, directory))
