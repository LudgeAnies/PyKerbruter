
# PyKerbruter - Python wrapper over the Kerbrute utility
It is designed to spray passwords using the Kerberos protocol. Functional:
- Accepts in the parameters a list of logins, a list of passwords, a domain, and a delay in seconds between spray breaks;
- The delay means a pause in seconds after the password has been verified on all logins. Helps to avoid account blocking;
- Creates the output directory, which contains logs for the date and time of the script launch;
- Creates a file checked.txt , which records the verified passwords line by line;
- If checked.txt if it exists, then passwords from it are not checked again. The following from the list are checked (the same applies to an empty line in the file);
- Output of the final kerbrute command to the console.
- Output of the result to the console and to the log.

## Usage:
```bash
py-kerbruter.py [-h] -u USERS -p PASSWORDS -d DOMAIN -dc DC [-t DELAY] [--kerbrute-path KERBRUTE_PATH]


  -h, --help            Show this help message and exit
  -u, --users USERS     User list for spraying
  -p, --passwords PASSWORDS
                        Password list for spraying
  -d, --domain DOMAIN   Domain name
  -dc, --dc DC          Domain Controller
  -t, --delay DELAY     Delay between spreading cycles in seconds (default: 155)
  --kerbrute-path KERBRUTE_PATH
                        Path to kerbrute (default: "kerbrute")

Required arguments:
  -u USERS, --users 
                    User list for spraying
  -p PASSWORDS, --passwords
                    Password list for spraying
  -d DOMAIN, --domain 
                    Domain name
  -dc DC    --dc            
                    Domain Controller

Optional arguments:
  -t DELAY, --delay 
                    Delay between spreading cycles in seconds (default: 155)
  --kerbrute-path KERBRUTE_PATH
                    Path to Kerbrute (default: ./kerbrute)
```

## Example:
```bash
python py-kerbruter.py -u users.txt -p passwords.txt -d example.com -dc dc01.example.com -t 230
```
