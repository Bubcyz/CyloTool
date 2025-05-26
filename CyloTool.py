#!/usr/bin/python

import random
import urllib.parse
import requests
from time import sleep
import os, signal, sys
from rich.console import Console
from rich.prompt import Prompt, IntPrompt
from rich.text import Text
from rich.style import Style
import pystyle
from pystyle import Colors, Colorate

from cylo import Bubcyz

# Initialize console at global level
console = Console()

def signal_handler(sig, frame):
    print("\n Bye Bye...")
    sys.exit(0)

def gradient_text(text, colors):
    lines = text.splitlines()
    height = len(lines)
    width = max(len(line) for line in lines)
    colorful_text = Text()
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char != ' ':
                color_index = int((x/(width-1 if width>1 else 1) + y/(height-1 if height>1 else 1)) * 0.5 * (len(colors)-1))
                color_index = min(max(color_index, 0), len(colors) - 1)
                style = Style(color=colors[color_index])
                colorful_text.append(char, style=style)
            else:
                colorful_text.append(char)
        colorful_text.append("\n")
    return colorful_text

def banner(console):
    os.system('cls' if os.name == 'nt' else 'clear')
    brand_name = "𝐏𝐨𝐰𝐞𝐫𝐞𝐝 𝐁𝐲: 𝐊𝐚𝐲𝐳𝐞𝐧 𝐱 𝐂𝐲𝐥𝐨𝐓𝐨𝐨𝐥 𝐕𝟑"
    
    text = Text(brand_name, style="bold bright_cyan")
    
    console.print(text)
    console.print("[bold deep_sky_blue3]============================================================[/]")
    console.print("[bold gold1]      𝗣𝗟𝗘𝗔𝗦𝗘 𝗟𝗢𝗚 𝗢𝗨𝗧 𝗙𝗥𝗢𝗠 𝗖𝗣𝗠 𝗕𝗘𝗙𝗢𝗥𝗘 𝗨𝗦𝗜𝗡𝗚 𝗧𝗛𝗜𝗦 𝗧𝗢𝗢𝗟[/]")
    console.print("[bold dark_orange]      𝗦𝗛𝗔𝗥𝗜𝗡𝗚 𝗧𝗛𝗘 𝗔𝗖𝗖𝗘𝗦𝗦 𝗞𝗘𝗬 𝗜𝗦 𝗡𝗢𝗧 𝗔𝗟𝗟𝗢𝗪𝗘𝗗[/]")
    console.print("[bold deep_sky_blue3]============================================================[/]")  

def load_player_data(cpm):
    response = cpm.get_player_data()
    
    if response.get('ok'):
        data = response.get('data')

        if all(key in data for key in ['floats', 'localID', 'money', 'coin', "integers"]):
            
            console.print("[dodger_blue1]========[/] [steel_blue1]ᴘʟᴀʏᴇʀ ᴅᴇᴛᴀɪʟꜱ[/] [dodger_blue1]========[/]")
            
            console.print(f"[steel_blue1]   >> Name        :[/] [bright_white]{data.get('Name', 'UNDEFINED')}[/]")
            console.print(f"[steel_blue1]   >> LocalID     :[/] [bright_white]{data.get('localID', 'UNDEFINED')}[/]")
            console.print(f"[steel_blue1]   >> Moneys      :[/] [spring_green3]{data.get('money', 'UNDEFINED')}[/]")
            console.print(f"[steel_blue1]   >> Coins       :[/] [gold3]{data.get('coin', 'UNDEFINED')}[/]")
            friends_count = len(data.get("FriendsID", []))
            console.print(f"[steel_blue1]   >> Friends     :[/] [bright_white]{friends_count}[/]")
            car_data = data.get("carIDnStatus", {}).get("carGeneratedIDs", [])
            unique_car_data = set(car_data)
            car_count = len(unique_car_data)
            console.print(f"[steel_blue1]   >> Car Count   :[/] [bright_white]{car_count}[/]")
       
        else:
            console.print("[red1] ! ERROR: new accounts must be signed-in to the game at least once (✘)[/]")
            sleep(1)
    else:
        console.print("[red1] ! ERROR: seems like your login is not properly set (✘)[/]")
        exit(1)

def load_key_data(cpm):
    data = cpm.get_key_data()
    
    console.print("[dodger_blue1]========[/] [steel_blue1]𝘼𝘾𝘾𝙀𝙎𝙎 𝙆𝙀𝙔 𝘿𝙀𝙏𝘼𝙄𝙇𝙎[/] [dodger_blue1]========[/]")
    
    console.print(f"[steel_blue1]   >> Access Key  :[/] [grey70]{data.get('access_key')}[/]")
    console.print(f"[steel_blue1]   >> Telegram ID :[/] [bright_white]{data.get('telegram_id')}[/]")
    
    if data.get('is_unlimited'):
        console.print(f"[steel_blue1]   >> Balance     :[/] [spring_green4]Unlimited[/]")
    else:
        console.print(f"[steel_blue1]   >> Balance     :[/] [chartreuse2]{data.get('coins')}[/]")

def prompt_valid_value(content, tag, password=False):
    while True:
        value = Prompt.ask(content, password=password)
        if not value or value.isspace():
            console.print(f"[red1]{tag} cannot be empty or just spaces. Please try again (✘)[/]")
        else:
            return value
            
def load_client_details():
    response = requests.get("http://ip-api.com/json")
    data = response.json()
    console.print("[purple] =============[white][ 𝙇𝙊𝘾𝘼𝙏𝙄𝙊𝙉 ][/]==============[/]")
    console.print(f"[white]    >> Country    : {data.get('country')} {data.get('zip')}[/]")
    console.print("[purple] ===============[white][ ＭＥＮＵ ][/]=============[/]")

def interpolate_color(start_color, end_color, fraction):
    start_rgb = tuple(int(start_color[i:i+2], 16) for i in (1, 3, 5))
    end_rgb = tuple(int(end_color[i:i+2], 16) for i in (1, 3, 5))
    interpolated_rgb = tuple(int(start + fraction * (end - start)) for start, end in zip(start_rgb, end_rgb))
    return "{:02x}{:02x}{:02x}".format(*interpolated_rgb)

def rainbow_gradient_string(customer_name):
    modified_string = ""
    num_chars = len(customer_name)
    start_color = "{:06x}".format(random.randint(0, 0xFFFFFF))
    end_color = "{:06x}".format(random.randint(0, 0xFFFFFF))
    for i, char in enumerate(customer_name):
        fraction = i / max(num_chars - 1, 1)
        interpolated_color = interpolate_color(start_color, end_color, fraction)
        modified_string += f'[{interpolated_color}]{char}'
    return modified_string

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    while True:
        banner(console)
        acc_email = prompt_valid_value("[?] Account Email", "Email", password=False)
        acc_password = prompt_valid_value("[?] Account Password", "Password", password=False)
        acc_access_key = prompt_valid_value("[?] Access Key", "Access Key", password=False)
        console.print("[gold1][%] Trying to Login[/]: ", end="")
        cpm = Bubcyz(acc_access_key)
        login_response = cpm.login(acc_email, acc_password)
        if login_response != 0:
            if login_response == 100:
                console.print("[red1]ACCOUNT NOT FOUND (✘)[/]")
                sleep(2)
                continue
            elif login_response == 101:
                console.print("[red1]WRONG PASSWORD (✘)[/]")
                sleep(2)
                continue
            elif login_response == 103:
                console.print("[red1]INVALID ACCESS KEY (✘)[/]")
                sleep(2)
                continue
            else:
                console.print("[red1]TRY AGAIN[/]")
                console.print("[gold1] '! Note: make sure you filled out the fields ![/]")
                sleep(2)
                continue
        else:
            console.print("[green1]SUCCESSFUL (✔)[/]")
            sleep(1)
        while True:
            banner(console)
            load_player_data(cpm)
            load_key_data(cpm)
            load_client_details()
            choices = ["00", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31", "32", "33", "34", "35", "36", "37", "38", "39"]
            
            # Menu options
choices = ["00", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", 
                      "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", 
                      "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", 
                      "31", "32", "33", "34", "35", "36", "37", "38", "39"]
            
            # Menu options with consistent formatting and indentation
            menu_items = [
                ("(01)", "Increase Money", "1.5K"),
                ("(02)", "Increase Coins", "1.5K"), 
                ("(03)", "King Rank", "8K"),
                ("(04)", "Change ID", "4.5K"),
                ("(05)", "Change Name", "100"),
                ("(06)", "Change Name (Rainbow)", "100"),
                ("(07)", "Number Plates", "2K"),
                ("(08)", "Account Delete", "Free"),
                ("(09)", "Account Register", "Free"),
                ("(10)", "Delete Friends", "500"),
                ("(11)", "Unlock Paid Cars", "5K"),
                ("(12)", "Unlock All Cars", "6K"),
                ("(13)", "Unlock All Cars Siren", "3.5K"),
                ("(14)", "Unlock W16 Engine", "4K"),
                ("(15)", "Unlock All Horns", "3K"),
                ("(16)", "Unlock Disable Damage", "3K"),
                ("(17)", "Unlock Unlimited Fuel", "3K"),
                ("(18)", "Unlock Home 3", "4K"),
                ("(19)", "Unlock Smoke", "4K"),
                ("(20)", "Unlock Wheels", "4K"),
                ("(21)", "Unlock Animations", "2K"),
                ("(22)", "Unlock Equipaments M", "3K"),
                ("(23)", "Unlock Equipaments F", "3K"),
                ("(24)", "Change Race Wins", "1K"),
                ("(25)", "Change Race Loses", "1K"),
                ("(26)", "Clone Account", "7K"),
                ("(27)", "Custom HP", "2.5K"),
                ("(28)", "Custom Angle", "1.5K"),
                ("(29)", "Custom Tire burner", "1.5K"),
                ("(30)", "Custom Car Millage", "1.5K"),
                ("(31)", "Custom Car Brake", "2K"),
                ("(32)", "Remove Rear Bumper", "2K"),
                ("(33)", "Remove Front Bumper", "2K"),
                ("(34)", "Change Account Password", "2K"),
                ("(35)", "Change Account Email", "2K"),
                ("(36)", "Custom Spoiler", "10K"),
                ("(37)", "Custom BodyKit", "10K"),
                ("(38)", "Unlock Premium Wheels", "4.5K"),
                ("(39)", "Unlock Toyota Crown", "2K"),
                ("(0)", "Exit From Tool", "")
            ]

            # Print menu with perfect alignment
            for num, item, price in menu_items:
                if price:  # For items with prices
                    console.print(f"[yellow]{num}[/] [white]{item:<28}[/] [red]{price:>5}[/]")
                else:  # For exit option
                    console.print(f"[yellow]{num}[/] [white]{item}[/]")

            console.print("[red]===============[white][ ᴄʏʟᴏ ᴛᴏᴏʟ ][/]===============[/]")
            service = IntPrompt.ask("[?] Select a Service [red][1-39 or 0][/]", 
                                  choices=choices, 
                                  show_choices=False)
            console.print("[red]===============[white][ ᴄʏʟᴏ ᴛᴏᴏʟ ][/]===============[/]")
```
            
            if service == 0: # Exit
                console.print("[bold white] Thank You for using my tool[/bold white]")
            elif service == 1: # Increase Money
                console.print("[bold yellow][bold white][?][/bold white] Insert how much money do you want[/bold yellow]")
                amount = IntPrompt.ask("[?] Amount")
                console.print("[%] Saving your data: ", end=None)
                if amount > 0 and amount <= 500000000:
                    if cpm.set_player_money(amount):
                        console.print("[bold green]SUCCESSFUL (✔)[/bold green]")
                        console.print("[bold green]======================================[/bold green]")
                        answ = Prompt.ask("[?] Do You want to Exit ?", choices=["y", "n"], default="n")
                        if answ == "y": console.print("[bold white] Thank You for using my tool[/bold white]")
                        else: continue
                    else:
                        console.print("[bold red]FAILED (✘)[/bold red]")
                        console.print("[bold red]please try again later! (✘)[/bold red]")
                        sleep(2)
                        continue
                else:
                    console.print("[bold red]FAILED (✘)[/bold red]")
                    console.print("[bold red]please use valid values! (✘)[/bold red]")
                    sleep(2)
                    continue
            elif service == 2:  # Increase Coins
                console.print("[bold yellow][bold white][?][/bold white] Insert how much coins do you want[/bold yellow]")
                amount = IntPrompt.ask("[?] Amount")
                print("[ % ] Saving your data: ", end="")
                if amount > 0 and amount <= 500000:
                    if cpm.set_player_coins(amount):
                        console.print("[bold green]SUCCESSFUL (✔)[/bold green]")
                        console.print("[bold green]======================================[/bold green]")
                        answ = Prompt.ask("[?] Do You want to Exit ?", choices=["y", "n"], default="n")
                        if answ == "y": console.print("[bold white] Thank You for using my tool[/bold white]")
                        else: continue
                    else:
                        console.print("[bold red]FAILED[/bold red]")
                        console.print("[bold red]Please Try Again[/bold red]")
                        sleep(2)
                        continue
                else:
                    console.print("[bold red]FAILED[/bold red]")
                    console.print("[bold yellow] 'Please use valid values[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 3: # King Rank
                console.print("[bold red][!] Note:[/bold red]: if the king rank doesn't appear in game, close it and open few times.", end=None)
                console.print("[bold red][!] Note:[/bold red]: please don't do King Rank on same account twice.", end=None)
                sleep(2)
                console.print("[%] Giving you a King Rank: ", end=None)
                if cpm.set_player_rank():
                    console.print("[bold yellow] 'SUCCESSFUL[/bold yellow]")
                    console.print("[bold yellow] '======================================[/bold yellow]")
                    answ = Prompt.ask("[?] Do You want to Exit ?", choices=["y", "n"], default="n")
                    if answ == "y": console.print("[bold white] Thank You for using my tool[/bold white]")
                    else: continue
                else:
                    console.print("[bold red]FAILED[/bold red]")
                    console.print("[bold red]Please Try Again[/bold red]")
                    sleep(2)
                    continue
            elif service == 4: # Change ID
                console.print("[bold yellow] '[?] Enter your new ID[/bold yellow]")
                new_id = Prompt.ask("[?] ID")
                console.print("[%] Saving your data: ", end=None)
                if len(new_id) >= 0 and len(new_id) <= 9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999 and (' ' in new_id) == False:
                    if cpm.set_player_localid(new_id.upper()):
                        console.print("[bold yellow] 'SUCCESSFUL[/bold yellow]")
                        console.print("[bold yellow] '======================================[/bold yellow]")
                        answ = Prompt.ask("[?] Do You want to Exit ?", choices=["y", "n"], default="n")
                        if answ == "y": console.print("[bold white] Thank You for using my tool[/bold white]")
                        else: continue
                    else:
                        console.print("[bold red]FAILED[/bold red]")
                        console.print("[bold red]Please Try Again[/bold red]")
                        sleep(2)
                        continue
                else:
                    console.print("[bold red]FAILED[/bold red]")
                    console.print("[bold yellow] 'Please use valid ID[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 5: # Change Name
                console.print("[bold yellow] '[?] Enter your new Name[/bold yellow]")
                new_name = Prompt.ask("[?] Name")
                console.print("[%] Saving your data: ", end=None)
                if len(new_name) >= 0 and len(new_name) <= 999999999:
                    if cpm.set_player_name(new_name):
                        console.print("[bold yellow] 'SUCCESSFUL[/bold yellow]")
                        console.print("[bold yellow] '======================================[/bold yellow]")
                        answ = Prompt.ask("[?] Do You want to Exit ?", choices=["y", "n"], default="n")
                        if answ == "y": console.print("[bold white] Thank You for using my tool[/bold white]")
                        else: continue
                    else:
                        console.print("[bold red]FAILED[/bold red]")
                        console.print("[bold red]Please Try Again[/bold red]")
                        sleep(2)
                        continue
                else:
                    console.print("[bold red]FAILED[/bold red]")
                    console.print("[bold yellow] 'Please use valid values[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 6: # Change Name Rainbow
                console.print("[bold yellow] '[?] Enter your new Rainbow Name[/bold yellow]")
                new_name = Prompt.ask("[?] Name")
                console.print("[%] Saving your data: ", end=None)
                if len(new_name) >= 0 and len(new_name) <= 999999999:
                    if cpm.set_player_name(rainbow_gradient_string(new_name)):
                        console.print("[bold yellow] 'SUCCESSFUL[/bold yellow]")
                        console.print("[bold yellow] '======================================[/bold yellow]")
                        answ = Prompt.ask("[?] Do You want to Exit ?", choices=["y", "n"], default="n")
                        if answ == "y": console.print("[bold white] Thank You for using my tool[/bold white]")
                        else: continue
                    else:
                        console.print("[bold red]FAILED[/bold red]")
                        console.print("[bold red]Please Try Again[/bold red]")
                        sleep(2)
                        continue
                else:
                    console.print("[bold red]FAILED[/bold red]")
                    console.print("[bold yellow] 'Please use valid values[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 7: # Number Plates
                console.print("[%] Giving you a Number Plates: ", end=None)
                if cpm.set_player_plates():
                    console.print("[bold green]SUCCESSFUL (✔)[/bold green]")
                    console.print("[bold green]======================================[/bold green]")
                    answ = Prompt.ask("[?] Do You want to Exit ?", choices=["y", "n"], default="n")
                    if answ == "y": console.print("[bold white] Thank You for using my tool[/bold white]")
                    else: continue
                else:
                    console.print("[bold red]FAILED[/bold red]")
                    console.print("[bold red]Please Try Again[/bold red]")
                    sleep(2)
                    continue
            elif service == 8: # Account Delete
                console.print("[bold yellow] '[!] After deleting your account there is no going back !![/bold yellow]")
                answ = Prompt.ask("[?] Do You want to Delete this Account ?!", choices=["y", "n"], default="n")
                if answ == "y":
                    cpm.delete()
                    console.print("[bold yellow] 'SUCCESSFUL[/bold yellow]")
                    console.print("[bold yellow] '======================================[/bold yellow]")
                    console.print("[bold yellow] f'Thank You for using our tool, please join our telegram channe: @{__CHANNEL_USERNAME__}[/bold yellow]")
                else: continue
            elif service == 9: # Account Register
                console.print("[bold yellow] '[!] Registring new Account[/bold yellow]")
                acc2_email = prompt_valid_value("[?] Account Email", "Email", password=False)
                acc2_password = prompt_valid_value("[?] Account Password", "Password", password=False)
                console.print("[%] Creating new Account: ", end=None)
                status = cpm.register(acc2_email, acc2_password)
                if status == 0:
                    console.print("[bold yellow] 'SUCCESSFUL[/bold yellow]")
                    console.print("[bold yellow] '======================================[/bold yellow]")
                    console.print("[bold yellow] f'INFO: In order to tweak this account with Telmun[/bold yellow]")
                    console.print("[bold yellow] 'you most sign-in to the game using this account[/bold yellow]")
                    sleep(2)
                    continue
                elif status == 105:
                    console.print("[bold red]FAILED[/bold red]")
                    console.print("[bold yellow] 'This email is already exists ![/bold yellow]")
                    sleep(2)
                    continue
                else:
                    console.print("[bold red]FAILED[/bold red]")
                    console.print("[bold red]Please Try Again[/bold red]")
                    sleep(2)
                    continue
            elif service == 10: # Delete Friends
                console.print("[%] Deleting your Friends: ", end=None)
                if cpm.delete_player_friends():
                    console.print("[bold green]SUCCESSFUL (✔)[/bold green]")
                    console.print("[bold green]======================================[/bold green]")
                    answ = Prompt.ask("[?] Do You want to Exit ?", choices=["y", "n"], default="n")
                    if answ == "y": console.print("[bold white] Thank You for using my tool[/bold white]")
                    else: continue
                else:
                    console.print("[bold red]FAILED[/bold red]")
                    console.print("[bold red]Please Try Again[/bold red]")
                    sleep(2)
                    continue
            elif service == 11: # Unlock All Paid Cars
                console.print("[!] Note: this function takes a while to complete, please don't cancel.", end=None)
                console.print("[%] Unlocking All Paid Cars: ", end=None)
                if cpm.unlock_paid_cars():
                    console.print("[bold green]SUCCESSFUL (✔)[/bold green]")
                    console.print("[bold green]======================================[/bold green]")
                    answ = Prompt.ask("[?] Do You want to Exit ?", choices=["y", "n"], default="n")
                    if answ == "y": console.print("[bold white] Thank You for using my tool[/bold white]")
                    else: continue
                else:
                    console.print("[bold red]FAILED[/bold red]")
                    console.print("[bold red]Please Try Again[/bold red]")
                    sleep(2)
                    continue
            elif service == 12: # Unlock All Cars
                console.print("[%] Unlocking All Cars: ", end=None)
                if cpm.unlock_all_cars():
                    console.print("[bold green]SUCCESSFUL (✔)[/bold green]")
                    console.print("[bold green]======================================[/bold green]")
                    answ = Prompt.ask("[?] Do You want to Exit ?", choices=["y", "n"], default="n")
                    if answ == "y": console.print("[bold white] Thank You for using my tool[/bold white]")
                    else: continue
                else:
                    console.print("[bold red]FAILED[/bold red]")
                    console.print("[bold red]Please Try Again[/bold red]")
                    sleep(2)
                    continue
            elif service == 13: # Unlock All Cars Siren
                console.print("[%] Unlocking All Cars Siren: ", end=None)
                if cpm.unlock_all_cars_siren():
                    console.print("[bold green]SUCCESSFUL (✔)[/bold green]")
                    console.print("[bold green]======================================[/bold green]")
                    answ = Prompt.ask("[?] Do You want to Exit ?", choices=["y", "n"], default="n")
                    if answ == "y": console.print("[bold white] Thank You for using my tool[/bold white]")
                    else: continue
                else:
                    console.print("[bold red]FAILED[/bold red]")
                    console.print("[bold red]Please Try Again[/bold red]")
                    sleep(2)
                    continue
            elif service == 14: # Unlock w16 Engine
                console.print("[%] Unlocking w16 Engine: ", end=None)
                if cpm.unlock_w16():
                    console.print("[bold green]SUCCESSFUL (✔)[/bold green]")
                    console.print("[bold green]======================================[/bold green]")
                    answ = Prompt.ask("[?] Do You want to Exit ?", choices=["y", "n"], default="n")
                    if answ == "y": console.print("[bold white] Thank You for using my tool[/bold white]")
                    else: continue
                else:
                    console.print("[bold red]FAILED[/bold red]")
                    console.print("[bold red]Please Try Again[/bold red]")
                    sleep(2)
                    continue
            elif service == 15: # Unlock All Horns
                console.print("[%] Unlocking All Horns: ", end=None)
                if cpm.unlock_horns():
                    console.print("[bold green]SUCCESSFUL (✔)[/bold green]")
                    console.print("[bold green]======================================[/bold green]")
                    answ = Prompt.ask("[?] Do You want to Exit ?", choices=["y", "n"], default="n")
                    if answ == "y": console.print("[bold white] Thank You for using my tool[/bold white]")
                    else: continue
                else:
                    console.print("[bold red]FAILED[/bold red]")
                    console.print("[bold red]Please Try Again[/bold red]")
                    sleep(2)
                    continue
            elif service == 16: # Disable Engine Damage
                console.print("[%] Unlocking Disable Damage: ", end=None)
                if cpm.disable_engine_damage():
                    console.print("[bold green]SUCCESSFUL (✔)[/bold green]")
                    console.print("[bold green]======================================[/bold green]")
                    answ = Prompt.ask("[?] Do You want to Exit ?", choices=["y", "n"], default="n")
                    if answ == "y": console.print("[bold white] Thank You for using my tool[/bold white]")
                    else: continue
                else:
                    console.print("[bold red]FAILED[/bold red]")
                    console.print("[bold red]Please Try Again[/bold red]")
                    sleep(2)
                    continue
            elif service == 17: # Unlimited Fuel
                console.print("[%] Unlocking Unlimited Fuel: ", end=None)
                if cpm.unlimited_fuel():
                    console.print("[bold green]SUCCESSFUL (✔)[/bold green]")
                    console.print("[bold green]======================================[/bold green]")
                    answ = Prompt.ask("[?] Do You want to Exit ?", choices=["y", "n"], default="n")
                    if answ == "y": console.print("[bold white] Thank You for using my tool[/bold white]")
                    else: continue
                else:
                    console.print("[bold red]FAILED[/bold red]")
                    console.print("[bold red]Please Try Again[/bold red]")
                    sleep(2)
                    continue
            elif service == 18: # Unlock House 3
                console.print("[%] Unlocking House 3: ", end=None)
                if cpm.unlock_houses():
                    console.print("[bold green]SUCCESSFUL (✔)[/bold green]")
                    console.print("[bold green]======================================[/bold green]")
                    answ = Prompt.ask("[?] Do You want to Exit ?", choices=["y", "n"], default="n")
                    if answ == "y": console.print("[bold white] Thank You for using my tool[/bold white]")
                    else: continue
                else:
                    console.print("[bold red]FAILED[/bold red]")
                    console.print("[bold red]Please Try Again[/bold red]")
                    sleep(2)
                    continue
            elif service == 19: # Unlock Smoke
                console.print("[%] Unlocking Smoke: ", end=None)
                if cpm.unlock_smoke():
                    console.print("[bold green]SUCCESSFUL (✔)[/bold green]")
                    console.print("[bold green]======================================[/bold green]")
                    answ = Prompt.ask("[?] Do You want to Exit ?", choices=["y", "n"], default="n")
                    if answ == "y": console.print("[bold white] Thank You for using my tool[/bold white]")
                    else: continue
                else:
                    console.print("[bold red]FAILED[/bold red]")
                    console.print("[bold red]Please Try Again[/bold red]")
                    sleep(2)
                    continue
            elif service == 20: # Unlock Smoke
                console.print("[%] Unlocking Wheels: ", end=None)
                if cpm.unlock_wheels():
                    console.print("[bold green]SUCCESSFUL (✔)[/bold green]")
                    console.print("[bold green]======================================[/bold green]")
                    answ = Prompt.ask("[?] Do You want to Exit ?", choices=["y", "n"], default="n")
                    if answ == "y": console.print("[bold white] Thank You for using my tool[/bold white]")
                    else: continue
                else:
                    console.print("[bold red]FAILED[/bold red]")
                    console.print("[bold red]Please Try Again[/bold red]")
                    sleep(8)
                    continue
            elif service == 21: # Unlock Smoke
                console.print("[%] Unlocking Animations: ", end=None)
                if cpm.unlock_animations():
                    console.print("[bold green]SUCCESSFUL (✔)[/bold green]")
                    console.print("[bold green]======================================[/bold green]")
                    answ = Prompt.ask("[?] Do You want to Exit ?", choices=["y", "n"], default="n")
                    if answ == "y": console.print("[bold white] Thank You for using my tool[/bold white]")
                    else: continue
                else:
                    console.print("[bold red]FAILED[/bold red]")
                    console.print("[bold red]Please Try Again[/bold red]")
                    sleep(2)
                    continue
            elif service == 22: # Unlock Smoke
                console.print("[%] Unlocking Equipaments Male: ", end=None)
                if cpm.unlock_equipments_male():
                    console.print("[bold green]SUCCESSFUL (✔)[/bold green]")
                    console.print("[bold green]======================================[/bold green]")
                    answ = Prompt.ask("[?] Do You want to Exit ?", choices=["y", "n"], default="n")
                    if answ == "y": console.print("[bold white] Thank You for using my tool[/bold white]")
                    else: continue
                else:
                    console.print("[bold red]FAILED[/bold red]")
                    console.print("[bold red]Please Try Again[/bold red]")
                    sleep(2)
                    continue
            elif service == 23: # Unlock Smoke
                console.print("[%] Unlocking Equipaments Female: ", end=None)
                if cpm.unlock_equipments_female():
                    console.print("[bold green]SUCCESSFUL (✔)[/bold green]")
                    console.print("[bold green]======================================[/bold green]")
                    answ = Prompt.ask("[?] Do You want to Exit ?", choices=["y", "n"], default="n")
                    if answ == "y": console.print("[bold white] Thank You for using my tool[/bold white]")
                    else: continue
                else:
                    console.print("[bold red]FAILED[/bold red]")
                    console.print("[bold red]Please Try Again[/bold red]")
                    sleep(2)
                    continue
            elif service == 24: # Change Races Wins
                console.print("[bold yellow] '[!] Insert how much races you win[/bold yellow]")
                amount = IntPrompt.ask("[?] Amount")
                console.print("[%] Changing your data: ", end=None)
                if amount > 0 and amount <= 999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999:
                    if cpm.set_player_wins(amount):
                        console.print("[bold yellow] 'SUCCESSFUL[/bold yellow]")
                        console.print("[bold yellow] '======================================[/bold yellow]")
                        answ = Prompt.ask("[?] Do You want to Exit ?", choices=["y", "n"], default="n")
                        if answ == "y": console.print("[bold white] Thank You for using my tool[/bold white]")
                        else: continue
                    else:
                        console.print("[bold red]FAILED[/bold red]")
                        console.print("[bold red]Please Try Again[/bold red]")
                        sleep(2)
                        continue
                else:
                    console.print("[bold red]FAILED[/bold red]")
                    console.print("[bold yellow] '[!] Please use valid values[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 25: # Change Races Loses
                console.print("[bold yellow] '[!] Insert how much races you lose[/bold yellow]")
                amount = IntPrompt.ask("[?] Amount")
                console.print("[%] Changing your data: ", end=None)
                if amount > 0 and amount <= 999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999:
                    if cpm.set_player_loses(amount):
                        console.print("[bold yellow] 'SUCCESSFUL[/bold yellow]")
                        console.print("[bold yellow] '======================================[/bold yellow]")
                        answ = Prompt.ask("[?] Do You want to Exit ?", choices=["y", "n"], default="n")
                        if answ == "y": console.print("[bold white] Thank You for using my tool[/bold white]")
                        else: continue
                    else:
                        console.print("[bold red]FAILED[/bold red]")
                        console.print("[bold yellow] '[!] Please use valid values[/bold yellow]")
                        sleep(2)
                        continue
                else:
                    console.print("[bold red]FAILED[/bold red]")
                    console.print("[bold yellow] '[!] Please use valid values[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 26: # Clone Account
                console.print("[bold yellow] '[!] Please Enter Account Detalis[/bold yellow]")
                to_email = prompt_valid_value("[?] Account Email", "Email", password=False)
                to_password = prompt_valid_value("[?] Account Password", "Password", password=False)
                console.print("[%] Cloning your account: ", end=None)
                if cpm.account_clone(to_email, to_password):
                    console.print("[bold green]SUCCESSFUL (✔)[/bold green]")
                    console.print("[bold green]======================================[/bold green]")
                    answ = Prompt.ask("[?] Do You want to Exit ?", choices=["y", "n"], default="n")
                    if answ == "y": console.print("[bold white] Thank You for using my tool[/bold white]")
                    else: continue
                else:     
                    console.print("[bold red]FAILED[/bold red]")
                    console.print("[bold yellow] '[!] THAT RECIEVER ACCOUNT IS GMAIL PASSWORD IS NOT VALID OR THAT ACCOUNT IS NOT REGISTERED[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 27:
                console.print("[bold yellow][!] Note[/bold yellow]: original speed can not be restored!.")
                console.print("[bold yellow][!] Enter Car Details.[/bold yellow]")
                car_id = IntPrompt.ask("[bold][?] Car Id[/bold]")
                new_hp = IntPrompt.ask("[bold][?]Enter New HP[/bold]")
                new_inner_hp = IntPrompt.ask("[bold][?]Enter New Inner Hp[/bold]")
                new_nm = IntPrompt.ask("[bold][?]Enter New NM[/bold]")
                new_torque = IntPrompt.ask("[bold][?]Enter New Torque[/bold]")
                console.print("[bold yellow][%] Hacking Car Speed[/bold yellow]:",end=None)
                if cpm.hack_car_speed(car_id, new_hp, new_inner_hp, new_nm, new_torque):
                    console.print("[bold green]SUCCESFUL (✔)[/bold green]")
                    console.print("================================")
                    answ = Prompt.ask("[?] Do You want to Exit ?", choices=["y", "n"], default="n")
                    if answ == "y": console.print("[bold white] Thank You for using my tool[/bold white]")
                    else: continue
                else:
                    console.print("[bold red]FAILED[/bold red]")
                    console.print("[bold yellow] '[!] Please use valid values[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 28: # ANGLE
                console.print("[bold yellow] '[!] ENTER CAR DETALIS[/bold yellow]")
                car_id = IntPrompt.ask("[bold][?] CAR ID[/bold]")
                console.print("[bold yellow] '[!] ENTER STEERING ANGLE[/bold yellow]")
                custom = IntPrompt.ask("[red][?]﻿ENTER THE AMOUNT OF ANGLE YOU WANT[/red]")                
                console.print("[red][%] HACKING CAR ANGLE[/red]: ", end=None)
                if cpm.max_max1(car_id, custom):
                    console.print("[bold yellow] 'SUCCESSFUL[/bold yellow]")
                    answ = Prompt.ask("[red][?] DO YOU WANT TO EXIT[/red] ?", choices=["y", "n"], default="n")
                    if answ == "y": console.print("[bold white] Thank You for using my tool[/bold white]")
                    else: continue
                else:
                    console.print("[bold red]FAILED[/bold red]")
                    console.print("[bold red]Please Try Again[/bold red]")
                    sleep(2)
                    continue
            elif service == 29: # tire
                console.print("[bold yellow] '[!] ENTER CAR DETALIS[/bold yellow]")
                car_id = IntPrompt.ask("[bold][?] CAR ID[/bold]")
                console.print("[bold yellow] '[!] ENTER PERCENTAGE[/bold yellow]")
                custom = IntPrompt.ask("[pink][?]﻿ENTER PERCENTAGE TIRES U WANT[/pink]")                
                console.print("[red][%] Setting Percentage [/red]: ", end=None)
                if cpm.max_max2(car_id, custom):
                    console.print("[bold yellow] 'SUCCESSFUL[/bold yellow]")
                    answ = Prompt.ask("[bold green][?] DO YOU WANT TO EXIT[/bold green] ?", choices=["y", "n"], default="n")
                    if answ == "y": console.print("[bold white] Thank You for using my tool[/bold white]")
                    else: continue
                else:
                    console.print("[bold red]FAILED[/bold red]")
                    console.print("[bold red]Please Try Again[/bold red]")
                    sleep(2)
                    continue
            elif service == 30: # Millage
                console.print("[bold]ENTER CAR DETAILS![/bold]")
                car_id = IntPrompt.ask("[bold][?] CAR ID[/bold]")
                console.print("[bold]ENTER NEW MILLAGE![/bold]")
                custom = IntPrompt.ask("[bold blue][?]﻿ENTER MILLAGE U WANT[/bold blue]")                
                console.print("[bold red][%] Setting Percentage [/bold red]: ", end=None)
                if cpm.millage_car(car_id, custom):
                    console.print("[bold green]SUCCESSFUL (✔)[/bold green]")
                    answ = Prompt.ask("[bold][?] DO YOU WANT TO EXIT[/bold] ?", choices=["y", "n"], default="n")
                    if answ == "y": console.print("[bold white] Thank You for using my tool[/bold white]")
                    else: continue
                else:
                    console.print("[bold red]FAILED[/bold red]")
                    console.print("[bold red]Please Try Again[/bold red]")
                    sleep(2)
                    continue
            elif service == 31: # Brake
                console.print("[bold]ENTER CAR DETAILS![/bold]")
                car_id = IntPrompt.ask("[bold][?] CAR ID[/bold]")
                console.print("[bold]ENTER NEW BRAKE![/bold]")
                custom = IntPrompt.ask("[bold blue][?]﻿ENTER BRAKE U WANT[/bold blue]")                
                console.print("[bold red][%] Setting BRAKE [/bold red]: ", end=None)
                if cpm.brake_car(car_id, custom):
                    console.print("[bold green]SUCCESSFUL (✔)[/bold green]")
                    answ = Prompt.ask("[bold][?] DO YOU WANT TO EXIT[/bold] ?", choices=["y", "n"], default="n")
                    if answ == "y": console.print("[bold white] Thank You for using my tool[/bold white]")
                    else: continue
                else:
                    console.print("[bold red]FAILED[/bold red]")
                    console.print("[bold red]Please Try Again[/bold red]")
                    sleep(2)
                    continue
            elif service == 32: # Bumper rear
                console.print("[bold]ENTER CAR DETAILS![/bold]")
                car_id = IntPrompt.ask("[bold][?] CAR ID[/bold]")                
                console.print("[bold red][%] Removing Rear Bumper [/bold red]: ", end=None)
                if cpm.rear_bumper(car_id):
                    console.print("[bold green]SUCCESSFUL (✔)[/bold green]")
                    answ = Prompt.ask("[bold][?] DO YOU WANT TO EXIT[/bold] ?", choices=["y", "n"], default="n")
                    if answ == "y": console.print("[bold white] Thank You for using my tool[/bold white]")
                    else: continue
                else:
                    console.print("[bold red]FAILED[/bold red]")
                    console.print("[bold red]Please Try Again[/bold red]")
                    sleep(2)
                    continue
            elif service == 33: # Bumper front
                console.print("[bold]ENTER CAR DETAILS![/bold]")
                car_id = IntPrompt.ask("[bold][?] CAR ID[/bold]")                
                console.print("[bold red][%] Removing Front Bumper [/bold red]: ", end=None)
                if cpm.front_bumper(car_id):
                    console.print("[bold green]SUCCESSFUL (✔)[/bold green]")
                    answ = Prompt.ask("[bold][?] DO YOU WANT TO EXIT[/bold] ?", choices=["y", "n"], default="n")
                    if answ == "y": console.print("[bold white] Thank You for using my tool[/bold white]")
                    else: continue
                else:
                    console.print("[bold red]FAILED[/bold red]")
                    console.print("[bold red]Please Try Again[/bold red]")
                    sleep(2)
                    continue
            elif service == 75:  # /testin endpoint
                console.print("[bold]ENTER CUSTOM FLOAT DATA[/bold]")
                custom = IntPrompt.ask("[bold][?] VALUE (e.g. 1 or 0)[/bold]")     # This is the value
                console.print(f"[bold red][%] Setting float key... [/bold red]", end=None)
                if cpm.testin(custom):
                    console.print("[bold green]SUCCESSFUL (✔)[/bold green]")
                    answ = Prompt.ask("[bold][?] DO YOU WANT TO EXIT[/bold] ?", choices=["y", "n"], default="n")
                    if answ == "y": console.print("[bold white] Thank You for using my tool[/bold white]")
                    else: continue
                else:
                    console.print("[bold yellow]FAILED[/bold yellow]")
                    console.print("[bold yellow]PLEASE TRY AGAIN[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 34:
                console.print("[bold]Enter New Password![/bold]")
                new_password = prompt_valid_value("[bold][?] Account New Password[/bold]", "Password", password=False)
                console.print("[bold red][%] Changing Password [/bold red]: ", end=None)
                if cpm.change_password(new_password):
                    console.print("[bold green]SUCCESSFUL (✔)[/bold green]")
                    answ = Prompt.ask("[bold][?] DO YOU WANT TO EXIT[/bold] ?", choices=["y", "n"], default="n")
                    if answ == "y": console.print("[bold white]Thank You for using my tool[/bold white]")
                    else: continue
                else:
                    console.print("[bold yellow]FAILED[/bold yellow]")
                    console.print("[bold yellow]PLEASE TRY AGAIN[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 36: # telmunnongodz
                console.print("[bold]ENTER CAR DETAILS![/bold]")
                car_id = IntPrompt.ask("[bold][?] CAR ID[/bold]")
                console.print("[bold]ENTER SPOILER ID![/bold]")
                custom = IntPrompt.ask("[bold blue][?]ENTER NEW SPOILER ID[/bold blue]")                
                console.print("[bold red][%] SAVING YOUR DATA [/bold red]: ", end=None)
                if cpm.telmunnongodz(car_id, custom):
                    console.print("[bold green]SUCCESSFUL (✔)[/bold green]")
                    answ = Prompt.ask("[bold][?] DO YOU WANT TO EXIT[/bold] ?", choices=["y", "n"], default="n")
                    if answ == "y": console.print("[bold white] Thank You for using my tool[/bold white]")
                    else: continue
                else:
                    console.print("[bold red]FAILED[/bold red]")
                    console.print("[bold red]Please Try Again[/bold red]")
                    sleep(2)
                    continue
            elif service == 37: # telmunnongonz
                console.print("[bold]ENTER CAR DETAILS![/bold]")
                car_id = IntPrompt.ask("[bold][?] CAR ID[/bold]")
                console.print("[bold]ENTER BODYKIT ID![/bold]")
                custom = IntPrompt.ask("[bold blue][?]INSERT BODYKIT ID[/bold blue]")                
                console.print("[bold red][%] SAVING YOUR DATA [/bold red]: ", end=None)
                if cpm.telmunnongonz(car_id, custom):
                    console.print("[bold green]SUCCESSFUL (✔)[/bold green]")
                    answ = Prompt.ask("[bold][?] DO YOU WANT TO EXIT[/bold] ?", choices=["y", "n"], default="n")
                    if answ == "y": console.print("[bold white] Thank You for using my tool[/bold white]")
                    else: continue
                else:
                    console.print("[bold red]FAILED[/bold red]")
                    console.print("[bold red]Please Try Again[/bold red]")
                    sleep(2)
                    continue
            elif service == 35:
                console.print("[bold]Enter New Email![/bold]")
                new_email = prompt_valid_value("[bold][?] Account New Email[/bold]", "Email")
                console.print("[bold red][%] Changing Email [/bold red]: ", end=None)
                if cpm.change_email(new_email):
                    console.print("[bold green]SUCCESSFUL (✔)[/bold green]")
                    answ = Prompt.ask("[bold][?] DO YOU WANT TO EXIT[/bold] ?", choices=["y", "n"], default="n")
                    if answ == "y": console.print("[bold white]Thank You for using my tool[/bold white]")
                    else: break
                else:
                    console.print("[bold red]FAILED[/bold yellow]")
                    console.print("[bold red]EMAIL IS ALREADY REGISTERED [/bold red]")
                    sleep(4)
            elif service == 38: # SHITTIN
                console.print("[%] Unlocking Premium Wheels..: ", end=None)
                if cpm.shittin():
                    console.print("[bold green]SUCCESSFUL (✔)[/bold green]")
                    console.print("[bold green]======================================[/bold green]")
                    answ = Prompt.ask("[?] Do You want to Exit ?", choices=["y", "n"], default="n")
                    if answ == "y": console.print("[bold white] Thank You for using my tool[/bold white]")
                    else: continue
                else:
                    console.print("[bold red]FAILED[/bold red]")
                    console.print("[bold red]Please Try Again[/bold red]")
                    sleep(2)
                    continue
            elif service == 39: # Unlock toyota crown
                console.print("[!] Note: this function takes a while to complete, please don't cancel.", end=None)
                console.print("[%] Unlocking Toyota Crown: ", end=None)
                if cpm.unlock_crown():
                    console.print("[bold green]SUCCESSFUL (✔)[/bold green]")
                    console.print("[bold green]======================================[/bold green]")
                    answ = Prompt.ask("[?] Do You want to Exit ?", choices=["y", "n"], default="n")
                    if answ == "y": console.print("[bold white] Thank You for using my tool[/bold white]")
                    else: continue
                else:
                    console.print("[bold red]FAILED[/bold red]")
                    console.print("[bold red]Please Try Again[/bold red]")
                    sleep(2)
                    continue
            else:
                continue
            break
        break              
