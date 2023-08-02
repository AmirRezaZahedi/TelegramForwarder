# 🚀 TeleForwarder 📢

The Telegram Message Forwarding Bot simplifies the process of forwarding messages to a large number of recipients on Telegram. Whether you're running a promotional campaign, sending announcements, or sharing content, this bot streamlines communication with your audience.

## Prerequisites 📋

Before using the Telegram Bulk Message Forwarding Bot, make sure you have:

- `api_id` and `api_hash` from your [Telegram Developer Account](https://my.telegram.org).
- Your mobile number and Telegram account password.
- An Excel file (`.xlsx`) with recipient IDs.
- The Excel file should be in the bot's installation environment.
- Identify the sheet and column where recipient IDs are stored.

## Required Libraries 📚

Install the necessary libraries:

```bash
pip install openpyxl
pip install asyncio
pip install pyfiglet
pip install colorama
pip install telethon
pip install prettytable
```

You can install these libraries using the provided commands before running the bot.

## Download and Installation 💽

To download and install the Telegram Bulk Message Forwarding Bot:

1. Clone the repository with Git.
2. Run the `bot.py` file.

## Initial Setup ⚙️

During the first run:

1. Provide `api_id` and `api_hash`.
2. Enter your mobile number and the password sent from the official Telegram account.
3. Specify the Excel file name, sheet, and recipient column.

## Forwarding Messages ➡️

To forward messages:

1. Use the `savemessage` page to forward messages.
2. You have to wait between each sent message.
3. Adhere to Telegram's message limits (currently up to 50 messages per day to unknown individuals).

## Storing Recipient IDs 📝

Recipient IDs are read from the Excel file and stored in a list. IDs can also be stored in a `.txt` file in the program's environment.

## Important Notes 📌

- Follow Telegram's guidelines to avoid account suspension.
- Keep the Excel file updated within the bot's environment.

## Contributions 🤝

Contributions are welcome! Submit issues or pull requests to improve the bot.

## Disclaimer ⚠️

Use responsibly and comply with Telegram's terms of service.
