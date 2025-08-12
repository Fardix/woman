from colorama import Fore, Style, init
init(autoreset=True)

def print_response(data):
    print(Fore.CYAN + "📦 Command: " + Style.BRIGHT + str(data.get("command", "")))
    print(Fore.WHITE + "─" * 45)
    
    if data.get("description"):
        print(Fore.CYAN + "📜 Description:")
        print(Fore.WHITE + "  " + str(data["description"]))
        print()
    
    if data.get("options"):
        print(Fore.CYAN + "⚙️ Useful Options:")
        options = data["options"]

        if isinstance(options, list):
            for opt in options:
                if isinstance(opt, dict) and "flag" in opt and "desc" in opt:
                    print(Fore.GREEN + f"  {opt['flag']:<15}" + Fore.WHITE + str(opt['desc']))
                elif isinstance(opt, str):
                    print(Fore.WHITE + "  " + opt)
        elif isinstance(options, str):
            print(Fore.WHITE + "  " + options)
        print()
    
    if data.get("example"):
        print(Fore.CYAN + "💡 Example:")
        print(Fore.YELLOW + "  " + str(data["example"]))
