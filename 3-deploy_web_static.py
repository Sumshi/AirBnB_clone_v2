#!/usr/bin/python3
"""
This module provides a function to create a .tgz archive from web_static folder
"""


from fabric.api import *
from datetime import datetime
import os


# setting the web-01 and web-02 ip addresses
env.hosts = ['54.90.12.230', '52.86.29.154']
env.user = "ubuntu"


def do_pack():
    """Create a tar gzipped archive of the directory web_static."""
    try:
        # obtain the current date and time
        now = datetime.now().strftime("%Y%m%d%H%M%S")

        # Construct path where archive will be saved
        archive_path = "versions/web_static_{}.tgz".format(now)

        # use fabric function to create directory if it doesn't exist
        local("mkdir -p versions")

        # Use tar command to create a compresses archive
        archived = local("tar -cvzf {} web_static".format(archive_path))
        return archive_path
    except Exception as e:
        return None


def do_deploy(archive_path):
    """
    distributes an archive to your web servers, using the function do_deploy
    """
    # returns false if archive_path does not exitst
    if os.path.exists(archive_path):
        # upload the archive to /tmp/directory in web server
        put(archive_path, '/tmp/')
        # extract filename from a full path, web_static_20231004163451.tgz
        archive_name = archive_path.split('/')[-1]
        # extract only the folder name, web_static_20231004163451
        archive_folder = archive_path.split('.')[0]  # gets filename
        # place the extracted content in desired folder
        run('mkdir -p /data/web_static/releases/{}'.format(archive_folder))

        # using tar command to extract the uploaded contents
        run('tar -xzf /tmp/{} -C /data/web_static/releases/{}/'
            .format(archive_name, archive_folder))

        # Delete archive from web server
        run('rm /tmp/{}'.format(archive_name))

        # Delete symbolic link /data/web_static/current
        # run('rm -rf /data/web_static/current')

        # Create a new symbolic link
        run(
            'mv /data/web_static/releases/{}/web_static/* \
            /data/web_static/releases/{}/'
            .format(archive_folder, archive_folder)
        )
        run(
            'rm -rf /data/web_static/releases/{}/web_static'
            .format(archive_folder)
        )
        run('rm -rf /data/web_static/current')
        run('ln -s /data/web_static/releases/{}/ /data/web_static/current'
            .format(archive_folder))
        return True
    else:
        return False


def deploy():
    """creates path of an archive"""
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)
