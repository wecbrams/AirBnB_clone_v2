#!/usr/bin/python3
"""Generates a .tgz archive and distributes the archive to the web servers"""

from fabric.api import run, env, put
from os import path

env.hosts = ['34.234.201.130', '54.236.51.83']
env.user = "ubuntu"


def do_deploy(archive_path):
    """Distributes the .tgz archive to the web servers"""

    if not path.exists(archive_path):
        return False

    try:
        archived_file = archive_path[9:]
        newest_version = "/data/web_static/releases/{}".format(
            archived_file[:-4])
        archived_file = "/tmp/{}".format(archived_file)

        put(archive_path, "/tmp/")
        run("sudo mkdir -p {}".format(newest_version))
        run("sudo tar -xzf {} -C {}/".format(archived_file,
                                             newest_version))
        run("sudo rm {}".format(archived_file))
        run("sudo mv {}/web_static/* {}".format(newest_version,
                                                newest_version))
        run("sudo rm -rf {}/web_static".format(newest_version))
        run("sudo rm -rf /data/web_static/current")
        run("sudo ln -s {} /data/web_static/current".format(newest_version))

        print("New version deployed!")

        return True
    except Exception:
        return False
