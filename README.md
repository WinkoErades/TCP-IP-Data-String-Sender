# TCP/IP Data String Sender

This Python script allows users to send a TCP/IP data string to a specified IP address and port. The data string can either be selected from a JSON file or entered manually. If a new string is entered, it will be added to the JSON file (if it doesn't already exist).

---

## Features

- **Select Existing Data**: Choose a data string from a local JSON file.
- **Manual Entry**: Input a new data string manually.
- **Duplicate Check**: Avoids adding duplicate entries to the JSON file.
- **JSON Auto-Update**: Automatically appends new entries.
- **Send via TCP/IP**: Transmits the data string to a user-defined IP and port.

---

## JSON Format

The JSON file (`data.json`) should be structured as follows:

```json
[
  {
    "title": "string",
    "description": "short description",
    "data": "data string"
  }
]
```

## Requirements
Python 3.x

No external libraries needed (uses standard Python socket and json modules)

Installation
Clone the repository:

```
git clone https://github.com/yourusername/tcp-ip-data-sender.git
cd tcp-ip-data-sender
```

Run the script:
```
python send_data.py
```
Usage
1. Launch the script.

2. Choose a data string from the list or enter a new one.

3. If new, the string is checked for duplicates and added to the JSON file if unique.

4. Enter the destination IP address and port number.

5. The selected data string is sent using a TCP/IP socket connection.

