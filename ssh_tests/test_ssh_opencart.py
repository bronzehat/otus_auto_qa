"""
Here is test of ssh-connect and restart with check if servie
is started and site is available
"""
import paramiko
import requests
import time

ssh_hostname = "192.168.85.154"
ssh_username = "asayapova"
ssh_password = "o9p0[-]="
services = ["apache2.service", "mysql.service"]
keyword = "Active"
opencart_page_protocol = "http"
opencart_ip = ssh_hostname

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# Make connection and create shell.
client.connect(hostname=ssh_hostname, username=ssh_username, password=ssh_password)
shell = client.invoke_shell()

# Restart services and get results.
for service in services:
    client.exec_command("".join(["sudo systemctl restart ", service]))
    time.sleep(10)
    print(service, "restarted")
    stdin, stdout, stderr = client.exec_command("".join(["sudo systemctl status ", service]))
    result = stdout.read().decode()
    error = stderr.read().decode()
    if result:
        for line in result.split("\n"):
            if keyword in line:
                print(line.strip())
    if error:
        print("Error text:", error)

# Close connection.
shell.close()
client.close()

# Check if opencart site is available
responce = requests.get("".join([opencart_page_protocol, "://", opencart_ip, "/opencart/"]))
if responce.status_code == 200:
    print("Opencart site page opens without errors")
