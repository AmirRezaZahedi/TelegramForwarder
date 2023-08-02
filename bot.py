
import os
import asyncio
from telethon import TelegramClient, events

    

# Replace with your actual API ID and API Hash
api_id = *
api_hash = '*'




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


    idsListExtract = ['test']
    problematic_rows = [7]

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

    print("Starting Telegram client...")
    with client:
        client.loop.run_until_complete(start_client())
        client.loop.run_until_complete(run_client())