import socket
import threading
import time
import sys
import os
from datetime import datetime

class PortScanner:
    def __init__(self):
        self.open_ports = []
        self.scan_count = 0
        self.total_ports = 0
        
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_banner(self):
        banner = """
\033[1;91m
 ██████╗██╗  ██╗ ██████╗ ██╗    ██╗██████╗ ██╗   ██╗██████╗ ██████╗ ██╗   ██╗
██╔════╝██║  ██║██╔═══██╗██║    ██║██╔══██╗██║   ██║██╔══██╗██╔══██╗╚██╗ ██╔╝
██║     ███████║██║   ██║██║ █╗ ██║██║  ██║██║   ██║██████╔╝██████╔╝ ╚████╔╝ 
██║     ██╔══██║██║   ██║██║███╗██║██║  ██║██║   ██║██╔══██╗██╔══██╗  ╚██╔╝  
╚██████╗██║  ██║╚██████╔╝╚███╔███╔╝██████╔╝╚██████╔╝██║  ██║██║  ██║   ██║   
 ╚═════╝╚═╝  ╚═╝ ╚═════╝  ╚══╝╚══╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   
                                                                              
\033[1;92m
╔══════════════════════════════════════════════════════════════════════════════╗
║                         PORT SCANNER TOOL v2.0                              ║
║                    Created by: CHOWDHURYVAI                                 ║
╚══════════════════════════════════════════════════════════════════════════════╝
\033[0m
"""
        print(banner)
    
    def print_contact_info(self):
        info = """
\033[1;96m
╔══════════════════════════════════════════════════════════════════════════════╗
║                           CONTACT INFORMATION                               ║
╠══════════════════════════════════════════════════════════════════════════════╣
║ 📱 Telegram ID: https://t.me/darkvaiadmin                                  ║
║ 📢 Telegram Channel: https://t.me/windowspremiumkey                        ║
║ 🌐 Hacking/Cracking Website: https://crackyworld.com/                      ║
╚══════════════════════════════════════════════════════════════════════════════╝
\033[0m
"""
        print(info)
    
    def validate_ip(self, ip):
        try:
            socket.inet_aton(ip)
            return True
        except socket.error:
            return False
    
    def scan_port(self, target, port, timeout=1):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            result = sock.connect_ex((target, port))
            sock.close()
            
            if result == 0:
                self.open_ports.append(port)
                return True
            return False
        except:
            return False
    
    def get_service_name(self, port):
        common_ports = {
            21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS",
            80: "HTTP", 110: "POP3", 115: "SFTP", 135: "RPC", 139: "NetBIOS",
            143: "IMAP", 194: "IRC", 443: "HTTPS", 445: "SMB", 993: "IMAPS",
            995: "POP3S", 1723: "PPTP", 3306: "MySQL", 3389: "RDP",
            5432: "PostgreSQL", 5900: "VNC", 6379: "Redis", 27017: "MongoDB"
        }
        return common_ports.get(port, "Unknown")
    
    def loading_animation(self, stop_event):
        animations = ["⣾", "⣽", "⣻", "⢿", "⡿", "⣟", "⣯", "⣷"]
        i = 0
        while not stop_event.is_set():
            sys.stdout.write(f"\r\033[1;93mScanning {animations[i]} \033[0m")
            sys.stdout.flush()
            time.sleep(0.1)
            i = (i + 1) % len(animations)
    
    def scan_ports_range(self, target, start_port, end_port, max_threads=100):
        self.open_ports = []
        self.scan_count = 0
        self.total_ports = end_port - start_port + 1
        
        print(f"\n\033[1;94m[*] Starting scan on {target}\033[0m")
        print(f"\033[1;94m[*] Scanning ports {start_port}-{end_port}\033[0m")
        print(f"\033[1;94m[*] Maximum threads: {max_threads}\033[0m")
        print(f"\033[1;94m[*] Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\033[0m")
        print("-" * 60)
        
        # Start loading animation
        stop_animation = threading.Event()
        animation_thread = threading.Thread(target=self.loading_animation, args=(stop_animation,))
        animation_thread.start()
        
        threads = []
        for port in range(start_port, end_port + 1):
            while threading.active_count() > max_threads:
                time.sleep(0.01)
            
            thread = threading.Thread(target=self.scan_port, args=(target, port))
            thread.daemon = True
            thread.start()
            threads.append(thread)
            self.scan_count += 1
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        # Stop loading animation
        stop_animation.set()
        animation_thread.join()
        
        print("\r" + " " * 50 + "\r")  # Clear loading line
    
    def display_results(self, target, scan_time):
        print("\n" + "=" * 70)
        print(f"\033[1;92mSCAN COMPLETED!\033[0m")
        print("=" * 70)
        print(f"\033[1;96mTarget: {target}\033[0m")
        print(f"\033[1;96mScan duration: {scan_time:.2f} seconds\033[0m")
        print(f"\033[1;96mTotal ports scanned: {self.total_ports}\033[0m")
        print(f"\033[1;96mOpen ports found: {len(self.open_ports)}\033[0m")
        print("-" * 70)
        
        if self.open_ports:
            print("\033[1;95mPORT     SERVICE     STATUS\033[0m")
            print("-" * 70)
            for port in sorted(self.open_ports):
                service = self.get_service_name(port)
                print(f"\033[1;92m{port:<8} {service:<11} OPEN\033[0m")
        else:
            print("\033[1;91mNo open ports found!\033[0m")
        
        print("=" * 70)
    
    def quick_scan(self, target):
        common_ports = [21, 22, 23, 25, 53, 80, 110, 115, 135, 139, 143, 
                       194, 443, 445, 993, 995, 1723, 3306, 3389, 5432, 
                       5900, 6379, 27017]
        
        print(f"\n\033[1;94m[*] Quick scan on {target}\033[0m")
        print(f"\033[1;94m[*] Scanning common ports...\033[0m")
        
        self.open_ports = []
        for port in common_ports:
            if self.scan_port(target, port, 2):
                service = self.get_service_name(port)
                print(f"\033[1;92m[+] Port {port} ({service}) is OPEN\033[0m")
    
    def main_menu(self):
        while True:
            self.clear_screen()
            self.print_banner()
            self.print_contact_info()
            
            print("\033[1;95m" + "╔══════════════════════════════════════════════════════════════════════════════╗")
            print("║                            MAIN MENU                                           ║")
            print("╠══════════════════════════════════════════════════════════════════════════════╣")
            print("║ \033[1;93m1\033[1;95m. Custom Port Range Scan                                               ║")
            print("║ \033[1;93m2\033[1;95m. Quick Scan (Common Ports)                                            ║")
            print("║ \033[1;93m3\033[1;95m. Scan Specific Port                                                   ║")
            print("║ \033[1;93m4\033[1;95m. About Tool                                                           ║")
            print("║ \033[1;93m5\033[1;95m. Exit                                                                 ║")
            print("╚══════════════════════════════════════════════════════════════════════════════╝\033[0m")
            
            choice = input("\n\033[1;94mEnter your choice (1-5): \033[0m")
            
            if choice == "1":
                self.custom_scan()
            elif choice == "2":
                self.quick_scan_menu()
            elif choice == "3":
                self.specific_port_scan()
            elif choice == "4":
                self.about_tool()
            elif choice == "5":
                print("\n\033[1;92mThank you for using CHOWDHURYVAI Port Scanner!\033[0m")
                sys.exit()
            else:
                print("\n\033[1;91mInvalid choice! Please try again.\033[0m")
                input("\nPress Enter to continue...")
    
    def custom_scan(self):
        self.clear_screen()
        self.print_banner()
        
        print("\033[1;95m" + "╔══════════════════════════════════════════════════════════════════════════════╗")
        print("║                         CUSTOM PORT SCAN                                           ║")
        print("╚══════════════════════════════════════════════════════════════════════════════╝\033[0m")
        
        target = input("\n\033[1;94mEnter target IP or hostname: \033[0m")
        
        if not self.validate_ip(target):
            try:
                target = socket.gethostbyname(target)
            except:
                print("\n\033[1;91mInvalid IP or hostname!\033[0m")
                input("\nPress Enter to continue...")
                return
        
        try:
            start_port = int(input("\033[1;94mEnter start port (1-65535): \033[0m"))
            end_port = int(input("\033[1;94mEnter end port (1-65535): \033[0m"))
            
            if not (1 <= start_port <= 65535 and 1 <= end_port <= 65535):
                print("\n\033[1;91mPorts must be between 1 and 65535!\033[0m")
                input("\nPress Enter to continue...")
                return
            
            if start_port > end_port:
                print("\n\033[1;91mStart port cannot be greater than end port!\033[0m")
                input("\nPress Enter to continue...")
                return
            
            max_threads = input("\033[1;94mEnter max threads (default 100): \033[0m")
            max_threads = int(max_threads) if max_threads.isdigit() else 100
            
            start_time = time.time()
            self.scan_ports_range(target, start_port, end_port, max_threads)
            end_time = time.time()
            
            self.display_results(target, end_time - start_time)
            
        except ValueError:
            print("\n\033[1;91mInvalid port number!\033[0m")
        
        input("\nPress Enter to continue...")
    
    def quick_scan_menu(self):
        self.clear_screen()
        self.print_banner()
        
        print("\033[1;95m" + "╔══════════════════════════════════════════════════════════════════════════════╗")
        print("║                          QUICK SCAN                                             ║")
        print("╚══════════════════════════════════════════════════════════════════════════════╝\033[0m")
        
        target = input("\n\033[1;94mEnter target IP or hostname: \033[0m")
        
        if not self.validate_ip(target):
            try:
                target = socket.gethostbyname(target)
            except:
                print("\n\033[1;91mInvalid IP or hostname!\033[0m")
                input("\nPress Enter to continue...")
                return
        
        start_time = time.time()
        self.quick_scan(target)
        end_time = time.time()
        
        print(f"\n\033[1;94mQuick scan completed in {end_time - start_time:.2f} seconds\033[0m")
        input("\nPress Enter to continue...")
    
    def specific_port_scan(self):
        self.clear_screen()
        self.print_banner()
        
        print("\033[1;95m" + "╔══════════════════════════════════════════════════════════════════════════════╗")
        print("║                       SPECIFIC PORT SCAN                                        ║")
        print("╚══════════════════════════════════════════════════════════════════════════════╝\033[0m")
        
        target = input("\n\033[1;94mEnter target IP or hostname: \033[0m")
        
        if not self.validate_ip(target):
            try:
                target = socket.gethostbyname(target)
            except:
                print("\n\033[1;91mInvalid IP or hostname!\033[0m")
                input("\nPress Enter to continue...")
                return
        
        try:
            port = int(input("\033[1;94mEnter port to scan (1-65535): \033[0m"))
            
            if not 1 <= port <= 65535:
                print("\n\033[1;91mPort must be between 1 and 65535!\033[0m")
                input("\nPress Enter to continue...")
                return
            
            print(f"\n\033[1;94mScanning port {port} on {target}...\033[0m")
            
            if self.scan_port(target, port, 3):
                service = self.get_service_name(port)
                print(f"\n\033[1;92m[SUCCESS] Port {port} ({service}) is OPEN on {target}\033[0m")
            else:
                print(f"\n\033[1;91m[FAILED] Port {port} is CLOSED on {target}\033[0m")
            
        except ValueError:
            print("\n\033[1;91mInvalid port number!\033[0m")
        
        input("\nPress Enter to continue...")
    
    def about_tool(self):
        self.clear_screen()
        self.print_banner()
        
        about_text = """
\033[1;95m
╔══════════════════════════════════════════════════════════════════════════════╗
║                             ABOUT TOOL                                       ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║ \033[1;93mTool Name:\033[1;95m CHOWDHURYVAI Port Scanner v2.0                                ║
║ \033[1;93mDeveloper:\033[1;95m ChowdhuryVAI Team                                            ║
║ \033[1;93mPurpose:\033[1;95m Advanced Network Port Scanning & Security Analysis             ║
║                                                                              ║
║ \033[1;96mFEATURES:\033[1;95m                                                               ║
║ • Multi-threaded port scanning                                              ║
║ • Custom port range scanning                                                ║
║ • Quick common ports scan                                                   ║
║ • Specific port checking                                                    ║
║ • Service detection                                                         ║
║ • Real-time progress display                                                ║
║ • Professional UI with colors                                               ║
║                                                                              ║
║ \033[1;91mWARNING:\033[1;95m Use this tool only on networks you own or have                 ║
║          explicit permission to scan!                                       ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
\033[0m
"""
        print(about_text)
        input("\nPress Enter to continue...")

def main():
    try:
        scanner = PortScanner()
        scanner.main_menu()
    except KeyboardInterrupt:
        print("\n\n\033[1;91mScan interrupted by user!\033[0m")
        sys.exit()
    except Exception as e:
        print(f"\n\033[1;91mAn error occurred: {str(e)}\033[0m")
        sys.exit()

if __name__ == "__main__":
    main()
