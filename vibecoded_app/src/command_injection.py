#!/usr/bin/env python3
"""
Vulnerable Python code with Command Injection examples
FOR SAST TESTING ONLY - DO NOT RUN IN PRODUCTION
"""

import os
import subprocess

from flask import Flask, request

app = Flask(__name__)


# VULNERABLE: os.system with user input
def vulnerable_ping(host):
    # CRITICAL VULNERABILITY: User input directly in command
    command = f"ping -c 4 {host}"
    os.system(command)


# VULNERABLE: subprocess.call with shell=True
def vulnerable_ls(directory):
    # CRITICAL VULNERABILITY: Shell=True with user input
    command = f"ls -la {directory}"
    subprocess.call(command, shell=True)


# VULNERABLE: subprocess.Popen with shell=True
def vulnerable_cat(filename):
    # CRITICAL VULNERABILITY: User input in shell command
    command = f"cat {filename}"
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    output = process.communicate()[0]
    return output


# VULNERABLE: Flask route with command injection
@app.route("/ping")
def ping_host():
    host = request.args.get("host", "localhost")

    # CRITICAL VULNERABILITY: User input in command
    command = f"ping -c 1 {host}"
    result = subprocess.check_output(command, shell=True)
    return result


# VULNERABLE: Multiple command injection patterns
def vulnerable_file_operations():
    filename = request.args.get("file", "")

    # CRITICAL VULNERABILITY: Multiple dangerous patterns
    os.system(f"rm {filename}")  # Dangerous file deletion
    subprocess.call(f"chmod 777 {filename}", shell=True)  # Dangerous permissions
    subprocess.Popen(f"cp {filename} /tmp/", shell=True)  # File copy


# VULNERABLE: Command injection with environment variables
def vulnerable_env_command():
    user_input = request.args.get("input", "")

    # CRITICAL VULNERABILITY: User input in environment command
    command = f"echo {user_input} | grep -v secret"
    os.system(command)


# VULNERABLE: Process execution with user input
def vulnerable_process_exec():
    program = request.args.get("program", "ls")
    args = request.args.get("args", "")

    # CRITICAL VULNERABILITY: User input in process execution
    command = f"{program} {args}"
    subprocess.run(command, shell=True)


# VULNERABLE: Command injection in file operations
def vulnerable_file_read():
    filepath = request.args.get("file", "/etc/passwd")

    # CRITICAL VULNERABILITY: User input in file reading command
    command = f"head -10 {filepath}"
    result = subprocess.check_output(command, shell=True)
    return result


# VULNERABLE: Network command injection
def vulnerable_network_command():
    target = request.args.get("target", "localhost")
    port = request.args.get("port", "80")

    # CRITICAL VULNERABILITY: User input in network command
    command = f"nmap -p {port} {target}"
    subprocess.call(command, shell=True)


# VULNERABLE: System information command injection
def vulnerable_system_info():
    info_type = request.args.get("type", "cpu")

    # CRITICAL VULNERABILITY: User input in system command
    if info_type == "cpu":
        command = "cat /proc/cpuinfo"
    elif info_type == "memory":
        command = "free -h"
    else:
        command = f"cat /proc/{info_type}"

    result = subprocess.check_output(command, shell=True)
    return result


if __name__ == "__main__":
    vulnerable_ping("; echo 'pwned. again ☺️'")
