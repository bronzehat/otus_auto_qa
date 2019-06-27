"""
This is a small ssh client to connect by hostname, user and password data.
Also if flag -ftp is chosen it configures vsftpd on the host
"""
import argparse
import paramiko
from ftplib import FTP, error_reply, error_perm

#   Parsing command line arguments
PARSER = argparse.ArgumentParser()
PARSER.add_argument("-hostname", action="store", dest="hostname", type=str, default="192.168.85.154",
                    help="type the hostname to connect by ssh")
PARSER.add_argument("-user", action="store", dest="user", type=str, default="asayapova",
                    help="type the user to connect by ssh")
PARSER.add_argument("-password", action="store", dest="password", type=str, default="o9p0[-]=",
                    help="type the password to connect by ssh")
PARSER.add_argument("-exec", action="append", dest="commands", type=str, nargs='*',
                    help='type the command to execute by ssh (if you have whitespaces, '
                         'type command in such quotes: ""')
PARSER.add_argument("-shell", action="store", dest="shell", type=str, default="bash",
                    help="type the shell to execute commands by ssh")
PARSER.add_argument("-ftp", action="store_true", dest="ftp",
                    help="choose this option if you want to configure ftp server on the remote host")

ARGS = PARSER.parse_args()
user = ARGS.user
password = ARGS.password
hostname = ARGS.hostname
commands = ARGS.commands[0]
command_shell = ARGS.shell
ftp_config = ARGS.ftp
ftp_user = user
ftp_password = password
ftp_new_port = "2121"
new_ftp_user = "ftpuser"
new_ftp_user_password = password
ftp = FTP(hostname)

#   Setting up ssh-connection
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(hostname=hostname, username=user, password=password)
shell = client.invoke_shell()

# Preparing commands to execution
execute_command = ["".join(["sudo ", command_shell, " -c '"])]
if isinstance(commands, list):
    for command in commands:
        # stdin, stdout, stderr = client.exec_command(command)
        execute_command.append("".join([command, ";"]))
    execute_command.append("'")
elif isinstance(commands, str):
    # stdin, stdout, stderr = client.exec_command(commands)
    execute_command.append("".join([commands, "'"]))
execution = "".join(execute_command)
# executing commands and getting output
stdin, stdout, stderr = client.exec_command(execution, get_pty=True)
output = stdout.read().decode()
error = stderr.read().decode()
if output:
    print("Command: {} \nOutput:".format(execution), output.strip())
if error:
    print("Error text:", error)

class FTP_Server:
    """
    Class for ftp configuration of the target host
    """

    def ftp_status(self, hostname=hostname):
        print("Checking if vsftpd is up...")
        stdin, stdout, stderr = client.exec_command("sudo systemctl status vsftpd.service")
        output = stdout.read().decode()
        error = stderr.read().decode()
        if "Active" in output:
            print("vsftpd is already installed on host {}".format(hostname))
            return True
        else:
            print("vsftpd is not installed on host {}".format(hostname))
            if error: print(error)
            return False

    def ftp_restart(self, hostname=hostname):
        try:
            client.exec_command("sudo systemctl restart vsftpd.service", get_pty=True)
        except Exception as e:
            print("Could not restart vsftpd service:", e)

    def ftp_start(self, hostname=hostname):
        try:
            client.exec_command("sudo systemctl start vsftpd.service", get_pty=True)
        except Exception as e:
            print("Could not start vsftpd service:", e)

    def ftp_stop(self, hostname=hostname):
        try:
            client.exec_command("sudo systemctl stop vsftpd.service", get_pty=True)
        except Exception as e:
            print("Could not stop vsftpd service:", e)

    def ftp_login(self, user, password, hostname):
        try:
            ftp.login(user=user, passwd=password)
            print("Logged in as {} by FTP on host {}".format(user, hostname))
            return True
        except error_perm as e:
            print("Error connecting to host {} by user '{}', exception text: {}".format(hostname, user, e))
        except error_reply as e:
            print("Error connecting to host {} by user '{}', exception text: {}".format(hostname, user, e))
            return False

    def ftp_login_logout(self, user, password, hostname=hostname):
        try:
            ftp.login(user=user, passwd=password)
            print("Logged in as {} by FTP on host {}".format(user, hostname))
            ftp.close()
            print("Logged out as {} by FTP on host {}".format(user, hostname))
            return True
        except error_perm as e:
            print("Error connecting to host {} by user '{}', exception text: {}".format(hostname, user, e))
        except error_reply as e:
            print("Error connecting to host {} by user '{}', exception text: {}".format(hostname, user, e))
            return False

    def install_ftp_server(self):
        print("Updating links to install...")
        client.exec_command("sudo apt-get update",  get_pty=True)
        print("Links to install updated")
        print("Installing vsftpd...")
        client.exec_command("sudo apt-get install vsftpd -y", get_pty=True)
        client.exec_command("sudo systemctl enable vsftpd", get_pty=True)
        stdin, stdout, stderr = client.exec_command("sudo ufw status", get_pty=True)
        output = stdout.read().decode()
        error = stderr.read().decode()
        if error: print(error)
        if "inactive" in output and not error:
            print("UFW is inactive, no configuration is needed")
        else:
            print("UFW is active, configuring 20/tcp and 21/tcp ports...")
            client.exec_command("sudo ufw allow 20/tcp")
            client.exec_command("sudo ufw allow 21/tcp")
            print("Configured 20/tcp and 21/tcp ports")
        print("Checking version of vsftpd...")
        try:
            std_in, std_out, std_err = client.exec_command("vsftpd -version")
            version_output = stdout.read().decode()
            version_err = stderr.read().decode()
            if std_out: print(version_output)
            if version_err: print(version_err)
        except error_reply as e:
            print("Error while checking vsftpd version")
            print(e)
        print("Vsftpd installed")
        print("Adding lines to vsftpd.conf")
        client.exec_command("".join(["sudo bash -c ", "'echo ",
                                     '"local_enable=YES\n'
                                     'write_enable=YES\nlocal_umask=022\ndirmessage_enable=YES\nuse_localtime=YES\n'
                                     'xferlog_enable=YES\nconnect_from_port_20=YES\nchroot_local_user=YES\n'
                                     'secure_chroot_dir=/var/run/vsftpd/empty\npam_service_name=vsftpd\n'
                                     'rsa_cert_file=/etc/ssl/certs/ssl-cert-snakeoil.pem\n'
                                     'rsa_private_key_file=/etc/ssl/private/ssl-cert-snakeoil.key\nssl_enable=Yes\n'
                                     'pasv_enable=Yes\npasv_min_port=10000\npasv_max_port=10100\n'
                                     'allow_writeable_chroot=YES\n'
                                     'listen_port={}" >>/etc/vsftpd.conf'.format(ftp_new_port), "'"]))

    def check_listen_ports(self):
        print("Checking listen ports in vsftpd config..")
        try:
            stdin, stdout, stderr = client.exec_command("sudo cat /etc/vsftpd.conf | grep listen_port")
            output = stdout.read().decode()
            if not output:
                print("No 'listen_port' subline in config")
            else:
                print("Check listen ports output:\n", output)
        except Exception as e:
            print("Error checking listen ports: ", e)

    def new_listen_port(self, port):
        std_in, std_out, std_err = client.exec_command("sudo cat /etc/vsftpd.conf | grep listen_port")
        out_put = std_out.read().decode()
        if "listen_port={}".format(port) in out_put:
            print("Port {} is already in listen_ports in vsftpd config, check output: ".format(port), out_put)
        else:
            try:
                client.exec_command("".join(["sudo bash -c ", "'echo ",
                                         '"listen_port={}\n" >> /etc/vsftpd.conf'.format(ftp_new_port), "'"]))
                stdin, stdout, stderr = client.exec_command("sudo cat /etc/vsftpd.conf | grep 'listen_port={}'".format(port))
                output = stdout.read().decode()
                if "listen_port={}".format(port) in output:
                    print("Port {} added as listen_port in vsftpd config".format(port))
            except Exception as e:
                print("Couldn't add new listen_port to vsftpd config: ", e)

    def change_listen_port(self, old_port, new_port):
        stdin, stdout, stderr = client.exec_command("sudo cat /etc/vsftpd.conf | grep listen_port")
        output = stdout.read().decode()
        error = stderr.read().decode()
        if not output and not error:
            self.new_listen_port(new_port)
        else:
            client.exec_command("sudo sed -i 's/listen_port={}/listen_port={}' /etc/vsftpd.conf".format(old_port,
                                                                                                        new_port))

    def ftp_user_add(self, user, hostname=hostname):
        print("Adding user {} on hostname {}".format(user, hostname))
        stdin, stdout, stderr = client.exec_command("sudo useradd -m {}".format(user), get_pty=True)
        error = stderr.read().decode()
        output = stdout.read().decode()
        if "already exists" in output:
            print("User {} already exists on host {}".format(user, hostname))
        elif not error:
            print("User {} added on host {}".format(user, hostname))
        if error: print("Error: ", error)


    def ftp_user_set_password(self, user, password):
        print("Setting {}'s password...".format(user))
        stdin, stdout, stderr = client.exec_command("sudo passwd {}".format(user))
        stdin.write("".join([password, "\n", password, "\n"]))
        stdin.flush()
        print("{}'s password updated".format(user))
        client.exec_command("exit", get_pty=True)

    def ftp_user_delete(self, user):
        print("Deleting user {} from hostname {}...".format(user, hostname))
        try:
            stdin, stdout, stderr = client.exec_command("sudo userdel {}".format(user))
            stdin.write("".join([password, "\n"]))
            stdin.flush()
            print("User {} deleted from hostname {}".format(user, hostname))
        except Exception:
            print(Exception)

#   Configuring ftp on the server, if it's not configured yet
if ftp_config is True:
    ftp_server = FTP_Server()
    if not ftp_server.ftp_status():
        try:
            ftp_server.install_ftp_server()
            ftp_server.ftp_status()
        except error_reply as e:
            print("Could not install vsftpd and check it's status")
            print(e)

    ftp_server.check_listen_ports()
    ftp_server.new_listen_port(ftp_new_port)
    ftp_server.ftp_user_add(new_ftp_user)
    ftp_server.ftp_user_set_password(new_ftp_user, new_ftp_user_password)
    ftp_server.ftp_login_logout(new_ftp_user, new_ftp_user_password)
    ftp_server.ftp_user_delete(new_ftp_user)

shell.close()
client.close()
