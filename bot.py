import os
import asyncio
import openpyxl
import re
from telethon import TelegramClient, events

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
def extract_ids_from_excel(file_path, sheet_name, column_index):
    try:
        workbook = openpyxl.load_workbook(file_path)
        sheet = workbook[sheet_name]
        
        # Initialize an empty list to store non-empty cell values
        column_values = []
        
        # Initialize an empty list to store problematic row numbers
        problematic_rows = []
        
        # Loop through each row in the specified column and extract cell values
        for i, row in enumerate(sheet.iter_rows()):
            cell_value = row[column_index - 1].value
            if cell_value is not None:
                cell_value_str = str(cell_value)
                column_values.append(cell_value_str)
                
                # Check if the cell value is in a valid format (contains @, https://t.me/, or xxx)
                if not re.search(r"(?:https:\/\/t\.me\/|@|[A-Za-z_0-9]+)", cell_value_str):
                    problematic_rows.append(i + 1)  # Add the row number to the problematic_rows list
        
        # Concatenate all non-empty cell values to form a single string
        text = " ".join(column_values)
        
        ids_list = extract_ids(text)
        
        return ids_list, problematic_rows
    
    except Exception as e:
        print(f"Error: {e}")
        return None, []

# Replace with your actual API ID and API Hash
api_id = 0
api_hash = ''




# Initialize the Telegram client
client = TelegramClient('aicup', api_id, api_hash)

# Function to send a message to a user
async def send_message_to_user(user, message):
    try:
        await asyncio.sleep(2.5)
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

    fileName = input("Enter Excel file name: ")
    filePath = os.path.join(os.getcwd(), fileName)
    sheetName = input("Enter sheet name: ")
    columnIndex = int(input("Enter column index (RTL): "))

    idsListExtract, problematic_rows = extract_ids_from_excel(filePath, sheetName, columnIndex)
    #idsListExtract = ['test']
    #problematic_rows = [7]

    if idsListExtract is not None:
        fileName = "ids_file.txt"
        with open(fileName, 'w') as file:
            for item in idsListExtract:
                file.write(item + "\n")
        print(idsListExtract)
        print()
        print("The list was saved in the file ids_file.txt")
        
        if problematic_rows:
            print("\nProblematic Rows (Invalid IDs):")
            print(problematic_rows)
        else:
            print("No problematic rows found.")

    api_id = input('Enter api_id in \'my.telegram.org\'')
    api_hash = input('Enter api_hash value in \'my.telegram.org\'')

    print("Starting Telegram client...")
    with client:
        client.loop.run_until_complete(start_client())
        client.loop.run_until_complete(run_client())