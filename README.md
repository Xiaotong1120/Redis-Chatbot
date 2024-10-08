
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
- **Docker**: A Docker environment is required to use the provided Docker setup, which simplifies running the Redis server and the chatbot.

## Installation
1. **Start Services with Docker Compose**: Ensure that Docker is installed and running, then use `docker-compose` to start Redis. The setup is entirely handled through Docker, so there is no need to manually configure a local Redis server. However, remember to mount the volume in the `docker-compose.yaml` file.
   ```sh
   docker-compose up
   ```
2. **Go into the docker environment**: Make sure the container is running, then open a new terminal to interact with it, and then run the following command.
   ```sh
   docker exec -it slim-python bash
   ```
3. **Interacting with the Chatbot**: Locate to the folder where contains the `chatbot.py` file, run the following command.
   ```sh
   python chatbot.py
   ```
   
## Usage
### Main Menu
Upon running the chatbot, you will be lead to the user identification first, after typing your personal information, you will have the following options:
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
- **Persistent Storage**: All user data and channel subscriptions are stored in Redis. Ensure that Docker is running during use, or the chatbot will not function as expected.
- **Security**: Since Redis stores user information, it's important to ensure that the Docker environment is properly secured.
- **Learning and Exploration**: This chatbot is intended for educational purposes, demonstrating how to integrate Redis for data persistence in Python applications.


## Acknowledgment of Assistance

I utilized ChatGPT for assistance with the following aspects of this project:

1. Writing the code to install the Redis library if it was not found.
2. Modifying the predefined object "self" for better structure.
3. Loading channels that users have already subscribed to and understanding the decoding process.
4. Designing the overall logic of the Redis-based chatbot.
5. Writing and improving the project documentation.
6. Implementing threads to handle multiple tasks simultaneously.
7. Creating the function for continuously listening to messages in channels.
