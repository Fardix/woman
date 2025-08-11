from colorama import Fore, Style, init
init(autoreset=True)

def print_response(data):
    print(Fore.CYAN + "📦 Command: " + Style.BRIGHT + data.get("command", ""))
    print(Fore.WHITE + "─" * 45)
    
    if data.get("description"):
        print(Fore.CYAN + "📜 Description:")
        print(Fore.WHITE + "  " + data["description"])
        print()
    
    if data.get("options"):
        print(Fore.CYAN + "⚙️ Useful Options:")
        for opt in data["options"]:
            print(Fore.GREEN + f"  {opt['flag']:<15}" + Fore.WHITE + opt['desc'])
        print()
    
    if data.get("example"):
        print(Fore.CYAN + "💡 Example:")
        print(Fore.YELLOW + "  " + data["example"])
