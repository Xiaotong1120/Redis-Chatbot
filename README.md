
# Chatbot README

## Overview
This project is a chatbot built in Python, utilizing Redis for data storage and management. The chatbot allows users to interact in predefined channels, send messages, and receive responses, such as fun facts or weather updates. By leveraging Redis, user information and channel subscriptions are stored persistently, providing a consistent user experience across multiple sessions.

The chatbot serves as an interactive tool that showcases how Redis can be integrated into a Python application for effective data management.

## Features
- **Persistent User Profiles**: User details (like name, age, and location) are saved in Redis, allowing for personalized interactions each time the user logs in.
- **Channel Functionality**:
  - Users can **join**, **leave**, **listen to**, and **send messages** within channels.
  - Channels are predefined and saved in Redis to keep them consistent across sessions.
- **Command-Based Interactions**:
  - `!help`: Displays available commands for user assistance.
  - `!weather <city>`: Provides mock weather data for a selected city.
  - `!fact`: Returns a random fun fact.
  - `!whoami`: Displays the current user's saved information.
- **Preloaded Data**: Includes fun facts and weather data for popular cities, offering ready-to-use information for users.

## Prerequisites
- **Python 3.x**: The script is written in Python, so you’ll need Python installed.
- **Redis Server**: A running Redis server is required for storing and managing user data and channel information.
- **Redis Python Library**: The script uses the `redis` library, which will be installed automatically if not already present.

## Installation
1. **Install Dependencies**: If you want to manually install the required Python library, use the following command:
   ```sh
   pip install redis
   ```
2. The script will attempt to install the `redis` package automatically if it is missing, so there is no need to worry about missing dependencies when running it for the first time.

## Running the Chatbot
1. **Start Redis Server**: Ensure that a Redis server is running. The chatbot defaults to `localhost` on port `6379`. If your setup differs, you may need to adjust the connection parameters in the script.
2. **Run the Script**: Execute the Python script using the command below:
   ```sh
   python chatbot.py
   ```
3. **Interacting with the Chatbot**: The chatbot will guide you through different menus to set up your profile, join channels, send messages, or use special commands.

## Usage
### Main Menu
Upon running the chatbot, you will have the following options:
1. **Channel-Related Commands**: Join or leave channels, listen to channel messages, or send messages.
2. **Special Commands**: Use chatbot commands like `!help`, `!weather <city>`, `!fact`, or `!whoami` to get information.
3. **Quit**: Exit the chatbot application.

### Channel Menu
- **Join a Channel**: You can select and join predefined channels (e.g., "cat", "dog").
- **Leave a Channel**: Leave any channel you are currently subscribed to.
- **Start Listening**: Start listening to messages in a channel you have joined.
- **Send a Message**: Send a message to one of the channels you are subscribed to.

### Special Commands Menu
- **!help**: Displays a list of available commands.
- **!weather <city>**: Provides mock weather information for popular cities.
- **!fact**: Returns a fun fact from the stored list in Redis.
- **!whoami**: Displays the saved information about the user.

## Customizing the Chatbot
- **Predefined Channels**: You can modify the channels in the `setup_predefined_channels()` method if you want to add new ones.
- **Fun Facts**: Additional facts can be added in the `store_mock_data()` method to enrich the user experience.
- **Weather Data**: Edit the weather information in `store_mock_data()` to change the weather data for cities of your choice.

## Requirements
The Python dependencies for this project are minimal:
- **Redis Library**: The Python `redis` library is used for connecting to the Redis server.

To install, include this in a `requirements.txt` file:
```text
redis
```

## Code Structure
- **Redis Setup**: Checks if the `redis` package is installed and installs it if missing.
- **Chatbot Class**: Manages the core functionality of the chatbot, including user profiles, channels, and command processing.
- **Menus**: Provides a structured way to interact with the chatbot, including the main menu, channel menu, and command menu.

### Key Methods
- **install_redis()**: Installs the Redis library if it is not already present.
- **setup_predefined_channels()**: Sets up and saves channels like "cat" and "dog" for users to join.
- **identify()**: Prompts the user for information like their username, age, and location, and saves it in Redis for future use.
- **join_channel()**, **leave_channel()**, **listen_to_joined_channel()**, **send_message()**: Handle all channel-related operations.
- **provide_fact()**, **provide_weather(city)**, **whoami()**: Provide specific responses based on user commands.
- **main_menu()**, **channel_menu()**, **specific_commands_menu()**: Guides users through different actions they can take with the chatbot.

## Important Notes
- **Persistent Storage**: All user data and channel subscriptions are stored in Redis. Ensure that your Redis server is running during use, or the chatbot will not function as expected.
- **Security**: Since Redis stores user information, it's important to ensure that the Redis server is properly secured.
- **Learning and Exploration**: This chatbot is intended for educational purposes, demonstrating how to integrate Redis for data persistence in Python applications.

## License
This project is licensed under the MIT License, so feel free to use, modify, and expand upon it as you like.
