# -*- coding: utf-8 -*- # Added for potentially broader compatibility
import socket
import json
import sys
import os

# --- Configuration ---
JSON_FILE = 'tcp_data_strings.json'  # Name of the file to store data strings
SOCKET_TIMEOUT = 10                  # Timeout for socket connection in seconds
DEFAULT_ENCODING = 'utf-8'           # Encoding for sending data

# --- ASCII Art Logo ---
# Simple silhouette of a wolf howling at a moon
# Raw string (r"") is used to avoid issues with backslashes
ASCII_LOGO = r"""

         .-"      "-.
        /            \
       |              |
       |,  .-.  .-.  ,|
       | )(_o/  \o_)( |
       |/     /\     \|
       (_     ^^     _)
        \__|IIIIII|__/
         | \IIIIII/ |
         \          /
          `--------`
           Mr. Wolf

     "I solve problems."

"""

# --- Helper Functions ---

def load_data(filename):
    """Loads data strings from the JSON file."""
    if not os.path.exists(filename):
        print(f"Info: JSON file '{filename}' not found. Will create a new one if needed.")
        return []
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
            if not content:
                return []
            data = json.loads(content)
            if not isinstance(data, list):
                print(f"Warning: JSON file '{filename}' does not contain a list. Starting fresh.")
                return []
            return data
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from '{filename}'. Check file format.")
        print("Starting with an empty list.")
        return []
    except IOError as e:
        print(f"Error reading file '{filename}': {e}")
        sys.exit(1)

def save_data(filename, data):
    """Saves the data strings list to the JSON file."""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        print(f"Data saved to '{filename}'.")
    except IOError as e:
        print(f"Error writing to file '{filename}': {e}")
    except TypeError as e:
        print(f"Error serializing data to JSON: {e}")


def find_entry_by_data(data_list, data_string):
    """Checks if a data string already exists in the list."""
    for entry in data_list:
        if entry.get('data') == data_string:
            return entry
    return None


def display_choices(data_list):
    """Displays the available data strings from the list."""
    if not data_list:
        print("\nNo saved data strings found.")
        return False

    print("\n--- Available Data Strings ---")
    for i, item in enumerate(data_list):
        title = item.get('title', 'N/A')
        desc = item.get('description', 'N/A')
        data_preview = item.get('data', 'N/A')[:60]
        if len(item.get('data', '')) > 60:
            data_preview += "..."
        print(f"  {i + 1}. Title: {title}")
        print(f"     Desc:  {desc}")
        print(f"     Data:  {data_preview}")
        print("-" * 10)
    return True

def get_target_details():
    """Prompts the user for target IP address and port."""
    while True:
        ip_address = input("Enter the target IP address: ").strip()
        if ip_address:
            break
        else:
            print("IP address cannot be empty.")

    while True:
        port_str = input("Enter the target port number (1-65535): ").strip()
        try:
            port = int(port_str)
            if 0 < port < 65536:
                return ip_address, port
            else:
                print("Port number must be between 1 and 65535.")
        except ValueError:
            print("Invalid port number. Please enter an integer.")

def send_tcp_data(ip, port, data_string):
    """Connects to the target and sends the data string via TCP/IP."""
    print(f"\nAttempting to send data to {ip}:{port}...")
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(SOCKET_TIMEOUT)
            server_address = (ip, port)
            print(f"Connecting to {ip} port {port}")
            sock.connect(server_address)
            print("Connection successful.")

            message_bytes = data_string.encode(DEFAULT_ENCODING)
            print(f"Sending {len(message_bytes)} bytes: '{data_string}'")
            sock.sendall(message_bytes)
            print("Data sent successfully.")

    except socket.timeout:
        print(f"Error: Connection to {ip}:{port} timed out after {SOCKET_TIMEOUT} seconds.")
    except socket.gaierror:
        print(f"Error: Hostname or IP address '{ip}' could not be resolved.")
    except ConnectionRefusedError:
         print(f"Error: Connection to {ip}:{port} was refused. Is the server running?")
    except socket.error as e:
        print(f"Socket Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred during TCP communication: {e}")
    finally:
        print("Communication attempt finished.")


# --- Main Execution ---
if __name__ == "__main__":
    # Print the logo first!
    print(ASCII_LOGO)

    print("TCP/IP Data Sender - Wolf Protocol") # Slightly modified title
    print("=" * 35) # Adjusted underline length

    # 1. Load existing data
    data_entries = load_data(JSON_FILE)

    # 2. Get target IP and Port
    target_ip, target_port = get_target_details()

    # 3. Choose data source (existing or manual)
    selected_data = None
    while selected_data is None:
        print("\nSelect data source:")
        print("  1. Choose from existing saved strings")
        print("  2. Enter data string manually (copy/paste)")
        choice = input("Enter choice (1 or 2): ").strip()

        if choice == '1':
            have_choices = display_choices(data_entries)
            if not have_choices:
                print("No existing strings. Please choose option 2 to add one.")
                continue

            while True:
                try:
                    select_idx_str = input(f"Enter the number of the string to send (1-{len(data_entries)}): ").strip()
                    select_idx = int(select_idx_str) - 1
                    if 0 <= select_idx < len(data_entries):
                        selected_data = data_entries[select_idx]['data']
                        print(f"Selected: '{data_entries[select_idx]['title']}'")
                        break
                    else:
                        print("Invalid selection number.")
                except ValueError:
                    print("Invalid input. Please enter a number.")
                except IndexError:
                     print("Selection number out of range.")

        elif choice == '2':
            manual_data = input("Paste or type the data string to send:\n").strip()

            if not manual_data:
                print("Data string cannot be empty. Please try again.")
                continue

            existing_entry = find_entry_by_data(data_entries, manual_data)

            if existing_entry:
                print("This data string already exists in the JSON file.")
                print(f"(Title: '{existing_entry.get('title', 'N/A')}')")
                selected_data = manual_data
            else:
                print("Data string not found in JSON. Adding as a new entry.")
                new_title = input("Enter a short title for this new entry: ").strip()
                new_desc = input("Enter a brief description: ").strip()

                new_entry = {
                    "title": new_title if new_title else "Untitled Manual Entry",
                    "description": new_desc if new_desc else "Manually entered data",
                    "data": manual_data
                }

                data_entries.append(new_entry)
                save_data(JSON_FILE, data_entries)
                selected_data = manual_data

        else:
            print("Invalid choice. Please enter 1 or 2.")

    # 4. Send the selected data
    if selected_data is not None:
        send_tcp_data(target_ip, target_port, selected_data)
    else:
        print("\nError: No data was selected or entered. Exiting.")

    print("\nScript finished.")
