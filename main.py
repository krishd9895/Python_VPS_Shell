import paramiko
import threading
import sys
from io import StringIO

# Connection Details
vps_ip = ""
username = "ubuntu"

# PEM Key as a multiline string
pem_key = """-----BEGIN RSA PRIVATE KEY-----
YOUR PEM KEY CONTENT HERE
-----END RSA PRIVATE KEY-----"""

def read_from_shell(shell):
    """Function to read data from the shell in a non-blocking manner."""
    while True:
        if shell.recv_ready():
            output = shell.recv(4096).decode('utf-8')
            if output:
                sys.stdout.write(output)  # Write output directly to stdout
                sys.stdout.flush()

def main():
    # Create SSH client
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        # Load the PEM private key from the string
        key = paramiko.RSAKey(file_obj=StringIO(pem_key))

        # Connect to the server
        ssh.connect(hostname=vps_ip, username=username, pkey=key)

        # Open an interactive shell session
        shell = ssh.invoke_shell()

        # Start a thread to read from the shell
        threading.Thread(target=read_from_shell, args=(shell,), daemon=True).start()

        # Interact with the shell
        while True:
            command = input()  # No prompt needed here
            if command.lower() in ['exit', 'quit']:
                break
            shell.send(command + '\n')

    except Exception as e:
        print(f"Error: {e}")

    finally:
        ssh.close()

if __name__ == "__main__":
    main()
