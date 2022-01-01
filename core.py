from fabric import task
from .servers import *

BACKUP_DIR="/backups"
KEY_DIR=BACKUP_DIR + "/keys"

@task
def help(c):
        pass

@task
def rsync(c, host):
        if host not in servers:
                raise Exception("Unknown host " + host)
        print("Downloading from " + host)
        if c.run("test -d " + get_host_directory(host), warn=True).exited != 0:
                print("Creating the directory for " + host)
                c.run("mkdir " + get_host_directory(host))
        if c.run("test -d " + get_host_directory(host) + "/daily.0", warn=True).exited != 0:
                c.run("mkdir " + get_host_directory(host) + "/daily.0")
        if c.run("test -d " + get_host_directory(host) + "/current", warn=True).exited != 0:
                print("Link to current does not exist. Creating it now...")
                c.run("ln -s " + get_host_directory(host) + "/daily.0 " + get_host_directory(host) + "/current")

        rsync_params = "-amz --stats --delete --include=/etc --include=/home --include=/root --include=/usr --include=/var --exclude=/* --link-dest=" + get_host_directory(host) + "/current"
        rsync_params = rsync_params + " -e \"ssh -4 -p 222 -i " + KEY_DIR + "/" + host + "\" " + servers[host]["user"] + "@" + servers[host]["host"] + ":/ " + get_host_directory(host) + "/latest"

        if servers[host]["user"] != "root":
                rsync_params = rsync_params + " --rsync-path=\"sudo rsync\""

        c.run("sudo rsync " + rsync_params)

        if c.run("test -d " + get_host_directory(host) + "/daily.6", warn=True).exited == 0:
                c.run("sudo rm -rf " + get_host_directory(host) + "/daily.6")
        if c.run("test -d " + get_host_directory(host) + "/daily.5", warn=True).exited == 0:
                c.run("sudo mv " + get_host_directory(host) + "/daily.5 " + get_host_directory(host) + "/daily.6")
        if c.run("test -d " + get_host_directory(host) + "/daily.4", warn=True).exited == 0:
                c.run("sudo mv " + get_host_directory(host) + "/daily.4 " + get_host_directory(host) + "/daily.5")
        if c.run("test -d " + get_host_directory(host) + "/daily.3", warn=True).exited == 0:
                c.run("sudo mv " + get_host_directory(host) + "/daily.3 " + get_host_directory(host) + "/daily.4")
        if c.run("test -d " + get_host_directory(host) + "/daily.2", warn=True).exited == 0:
                c.run("sudo mv " + get_host_directory(host) + "/daily.2 " + get_host_directory(host) + "/daily.3")
        if c.run("test -d " + get_host_directory(host) + "/daily.1", warn=True).exited == 0:
                c.run("sudo mv " + get_host_directory(host) + "/daily.1 " + get_host_directory(host) + "/daily.2")
        if c.run("test -d " + get_host_directory(host) + "/daily.0", warn=True).exited == 0:
                c.run("sudo mv " + get_host_directory(host) + "/daily.0 " + get_host_directory(host) + "/daily.1")
        c.run("sudo mv " + get_host_directory(host) + "/latest " + get_host_directory(host) + "/daily.0")
        print("Rsync complete for " + host)

@task
def all_rsync(c):
        for server in servers.keys():
                try:
                        rsync(c, server)
                except Exception as err:
                        print("Exception while rsyncing " + server)
                        print(err)

@task
def mysql(c, host):
        if host not in servers:
                raise Exception("Unknown host " + host)
        if servers[host]["mysql"] != True:
                return
        print("Dumping mysql for " + host)
        c.run(get_host_ssh_command(host) + " " + get_host_ssh_user(host) + " \"sudo mysqldump -A | sudo tee /root/mysql/databases.sql >/dev/null\"")

@task
def all_mysql(c):
        for server in servers.keys():
                try:
                        mysql(c, server)
                except Exception as err:
                        print("Exception while dumping mysql for " + server)
                        print(err)

@task
def tar(c, host):
        if host not in servers:
                raise Exception("Unknown host " + host)
        print("Taring the latest backup for " + host)
        c.run("sudo tar -zcpf " + get_host_directory(host) + "/weekly.tar.gz --directory=" + get_host_directory(host) + "/current .")

@task
def all_tar(c):
        for server in servers.keys():
                try:
                        tar(c, server)
                except Exception as err:
                        print("Exception while compressing backup for " + server)
                        print(err)

@task
def cron(c, compress=False):
        all_mysql(c)
        all_rsync(c)
        if compress:
                all_tar(c)

def get_host_directory(host):
        return BACKUP_DIR + "/" + host

def get_host_ssh_command(host):
        return "ssh -4 -p 222 -i " + KEY_DIR + "/" + host

def get_host_ssh_user(host):
        return servers[host]["user"] + "@" + servers[host]["host"]