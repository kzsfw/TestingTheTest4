import os, json, sys, requests, msvcrt

# colors - standard stuff, don't change it
class Colors:
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    RESET = '\033[0m'

# original ascii as requested
logo = f"""{Colors.CYAN}
   ___    ______                            
  / _ )  / __/ /________ ____  ___  ___ ____
 / _  | _\ \/ __/ __/ _ `/ _ \/ _ \/ -_) __/
/____(_)___/\__/_/  \_,_/ .__/ .__/\__/_/   
                       /_/  /_/                
{Colors.YELLOW}~~~ by VR ~~~{Colors.RESET}
"""

# constants
cfg_url = "https://github.com/kzsfw/TestingTheTest4/raw/refs/heads/main/config.json"
tmp_dir = os.path.join(os.environ.get('TEMP', 'C:\\'), 'BootTest')
v_file = os.path.join(tmp_dir, 'ver.txt')

# env setup
os.system('') # vt100 enable
os.system('ipconfig /flush >nul') # clear dns, ignore output
os.system('cls')

def main():
    print(logo)
    
    # folder check
    if not os.path.exists(tmp_dir): os.makedirs(tmp_dir)

    # fetch remote config
    try:
        r = requests.get(cfg_url, timeout=5).json()
    except Exception as e:
        print(f"{Colors.RED}[!] network error: {e}{Colors.RESET}")
        return

    # map config keys
    rem_v = str(r.get("version", "0.0"))
    url = r.get("link")
    auto = r.get("autodl", False)
    msg = r.get("message", "update available")
    
    # version check logic
    upd = False
    if not os.path.exists(v_file):
        print(f"{Colors.YELLOW}[*] init: local version missing.{Colors.RESET}")
        upd = True
    else:
        with open(v_file, 'r') as f: loc_v = f.read().strip()
        if loc_v != rem_v:
            print(f"{Colors.YELLOW}[!] sync: {loc_v} -> {rem_v}{Colors.RESET}")
            upd = True
        else:
            print(f"{Colors.GREEN}[+] version current.{Colors.RESET}")
            return

    # update flow
    if upd:
        do_upd = False
        if auto:
            print(f"{Colors.CYAN}[*] {msg}{Colors.RESET}")
            do_upd = True
        else:
            print(f"{Colors.YELLOW}[?] {msg}{Colors.RESET}")
            print(f"{Colors.BOLD}confirm update [y/n]:{Colors.RESET}")
            # getch is cleaner than input() for single chars
            if msvcrt.getch().decode(errors='ignore').lower() == 'y': do_upd = True

        if do_upd:
            print(f"{Colors.CYAN}[*] downloading file...{Colors.RESET}")
            try:
                # stream to disk to save memory
                with requests.get(url, stream=True) as res:
                    res.raise_for_status()
                    path = os.path.join(tmp_dir, "latest_file.txt")
                    with open(path, 'wb') as f:
                        for chunk in res.iter_content(8192): f.write(chunk)
                
                # sync version file
                with open(v_file, 'w') as f: f.write(rem_v)
                print(f"{Colors.GREEN}[+] update success.{Colors.RESET}")
                os.system(f"start notepad {path}") # fire and forget
            except:
                print(f"{Colors.RED}[!] download failed.{Colors.RESET}")
        else:
            print(f"{Colors.RED}[-] operation aborted.{Colors.RESET}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass # user killed it, fine by me
    except Exception as e:
        print(f"\n{Colors.RED}[!] fatal: {e}{Colors.RESET}")
    
    # hold window
    print(f"\n{Colors.CYAN}exit: press any key...{Colors.RESET}")
    msvcrt.getch()
