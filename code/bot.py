import re
import os
import openpyxl
import asyncio
import pyfiglet
import colorama
from colorama import Fore, Style
from telethon import TelegramClient, events
from prettytable import PrettyTable

# Initialize colorama
colorama.init(autoreset=True)
# Set colorama for colored output
colorama.init()

# Custom font for the banner
BANNER_FONT = "slant"

def print_banner():
    banner_text = pyfiglet.figlet_format("Telegram Forwarder", font=BANNER_FONT)
    banner = f"""
{Fore.CYAN}{banner_text}{Fore.GREEN}
Author: AmirReza zahedi
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
{Fore.CYAN}This script extracts IDs from an Excel file,{Fore.GREEN}
{Fore.CYAN}saves them in 'ids_file.txt', and forwards new{Fore.GREEN}
{Fore.CYAN}messages from 'me' to the specified users.{Fore.GREEN}
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
"""
    print(banner)

def print_success(message):
    print(f"{Fore.GREEN}[SUCCESS] {Style.RESET_ALL}{message}")

def print_error(message):
    print(f"{Fore.RED}[ERROR] {Style.RESET_ALL}{message}")

def clear_terminal():
    if os.name == 'nt':  # For Windows
        os.system('cls')
    else:  # For other platforms (Linux, macOS)
        os.system('clear')






def extract_ids(text):
    ids = []
    
    # Regular expression pattern to find usernames (@xxx), URLs (https://t.me/xxx), and valid format (xxx)
    id_pattern = r"(?:https:\/\/t\.me\/|@)?([A-Za-z_0-9]+)|([A-Za-z_0-9]+)"
    
    # Extract IDs from the text and append them to the list
    ids = [id_group[0] or id_group[1] for id_group in re.findall(id_pattern, text)]
    
    # Filter out None and non-English characters from the list
    ids = [id for id in ids if id is not None and id.isascii()]
    
    return ids

# Function to extract IDs from an Excel file
def extract_ids_from_excel(file_path, sheet_name, column_index, start_row, end_row):
    try:
        workbook = openpyxl.load_workbook(file_path)
        sheet = workbook[sheet_name]
        
        # Initialize an empty list to store non-empty cell values
        column_values = []
        
        # Initialize an empty list to store problematic row numbers
        problematic_rows = []
        
        # Loop through each row in the specified range and extract cell values
        for i, row in enumerate(sheet.iter_rows(), start=1):
            if start_row <= i <= end_row:
                cell_value = row[column_index - 1].value
                if cell_value is not None:
                    cell_value_str = str(cell_value)
                    column_values.append(cell_value_str)
                    
                    # Check if the cell value is in a valid format (contains @, https://t.me/, or xxx)
                    if not re.search(r"(?:https:\/\/t\.me\/|@|[A-Za-z_0-9]+)", cell_value_str):
                        problematic_rows.append(i)  # Add the row number to the problematic_rows list
        
        # Concatenate all non-empty cell values to form a single string
        text = " ".join(column_values)
        
        ids_list = extract_ids(text)
        
        return ids_list, problematic_rows
    
    except Exception as e:
        print(f"Error: {e}")
        return None, []

#List of Validate Id
idsListExtract = []

# Replace with your actual API ID and API Hash
apiId = int(input(f"Enter {Fore.YELLOW}api_id{Style.RESET_ALL} from 'my.telegram.org': "))
apiHash = input(f"Enter {Fore.YELLOW}api_hash{Style.RESET_ALL} value from 'my.telegram.org': ")



client = TelegramClient('TelegramForwarded', apiId, apiHash)

# Function to send a message to a user
async def send_message_to_user(user, message):
    try:
        await asyncio.sleep(10.0)
        print("Id user is: ", user)
        await client.forward_messages(user, message)
    except Exception as e:
        #User's Id is wrong
        print(f"Error while sending message to user {user}: {e}")

# Forward new messages from saved message to the specified users
@client.on(events.NewMessage(chats='me'))
async def forward_messages(event):
    print(f"Received new message: {event.id}")
    for user in idsListExtract:
        try:
            await send_message_to_user(user, event.message)
        except Exception as e:
            print(f"Error while forwarding message to user {user}: {e}")

# Start the Telegram client
async def start_client():
    await client.start()
    print("Telegram client started!")

# Run the Telegram client until disconnected
async def run_client():
    await client.run_until_disconnected()
    print("Telegram client disconnected!")

if __name__ == "__main__":
    print_banner()

    fileName = input("Enter Excel file name: ")
    filePath = os.path.join(os.getcwd(), fileName)
    sheetName = input("Enter sheet name: ")
    columnIndex = int(input("Enter column index (RTL): "))

    startRow = int(input("Enter start row: "))
    endRow = int(input("Enter end row: "))

    idsListExtract, problematic_rows = extract_ids_from_excel(filePath, sheetName, columnIndex, startRow, endRow)

    if idsListExtract is not None:
        fileName = "ids_file.txt"
        with open(fileName, 'w') as file:
            for item in idsListExtract:
                file.write(item + "\n")

        print(f"{Fore.GREEN}[SUCCESS] {Style.RESET_ALL}IDs extracted successfully!")
        print(f"{Fore.GREEN}[SUCCESS] {Style.RESET_ALL}The list was saved in the file {Fore.YELLOW}ids_file.txt{Style.RESET_ALL}")

        if problematic_rows:
            table = PrettyTable([f"{Fore.BLUE}Problematic Rows (Invalid IDs){Style.RESET_ALL}"])
            for row in problematic_rows:
                table.add_row([row])
            print(table)
        else:
            print_success("No problematic rows found.")

    print("Starting Telegram client...")
    with client:
        client.loop.run_until_complete(start_client())
        client.loop.run_until_complete(run_client())


