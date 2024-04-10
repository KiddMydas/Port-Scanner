# A simple port scanner made by Mydas


import socket
import threading
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

def scan_port(target, port, verbose=False):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        result = s.connect_ex((target, port))
        if result == 0:
            output = f'[+] Port {port} is open\n'
            banner = retrieve_banner(s)
            if verbose:
                output += f'[+] Banner for port {port}: {banner}\n'
            logging.info(f'Port {port} is open')
            logging.info(f'Banner for port {port}: {banner}')
        else:
            if verbose:
                output = f'[-] Port {port} is closed\n'
            logging.info(f'Port {port} is closed')
        s.close()
        return output
    except KeyboardInterrupt:
        print("\n[!] Exiting program.")
        exit()
    except socket.gaierror:
        logging.error("Error: Hostname could not be resolved.")
        exit()
    except socket.error:
        logging.error("Error: Couldn't connect to server.")
        exit()

def retrieve_banner(socket):
    try:
        banner = socket.recv(1024).decode().strip()
        return banner
    except:
        return "Banner not available"

def scan_ports(target, start_port, end_port, verbose=False):
    print(f'Scanning target: {target}')
    output = ''
    for port in range(start_port, end_port + 1):
        thread = threading.Thread(target=update_output, args=(target, port, verbose, output))
        thread.start()
    for port in range(start_port, end_port + 1):
        thread.join()

    return output

def update_output(target, port, verbose, output):
    output += scan_port(target, port, verbose)

## usage:
if __name__ == "__main__":
    print("Mydas Scanner")
    target_host = input("Enter the target host IP address or hostname: ")
    start_port = int(input("Enter the starting port number: "))
    end_port = int(input("Enter the ending port number: "))
    if start_port > end_port:
        print("Error: Starting port cannot be greater than the ending port.")
        exit()
    verbose_mode = input("Enable verbose mode? (y/n): ").lower() == 'y'
    output = scan_ports(target_host, start_port, end_port, verbose=verbose_mode)

    save_option = input("Do you want to save the output to a file? (y/n): ").lower()
    if save_option == 'y':
        filename = input("Enter the filename to save the output: ")
        with open(filename, 'w') as f:
            f.write(output)
        print(f"Output saved to {filename}")

