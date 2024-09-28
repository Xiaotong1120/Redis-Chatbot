import subprocess
import sys
import threading
import random

# Function to install the required package
def install_redis():
    try:
        import redis
    except ImportError:
        print("Redis package not found. Installing it now...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "redis"])
        print("Redis package installed successfully!")

# Call the installation function
install_redis()

import redis
import json
import random

class Chatbot:
    def __init__(self, host='redis', port=6379):
        self.client = redis.StrictRedis(host=host, port=port)
        self.pubsub = self.client.pubsub()
        self.username = None
        self.listening = False
        self.subscribed_channels = []

    def setup_predefined_channels(self):
        # Predefine a list of channels
        predefined_channels = ["cat", "dog", "bear", "monkey", "bird"]
        
        # Store them in Redis to be persistent across sessions
        for channel in predefined_channels:
            self.client.sadd("predefined_channels", channel)

        print("Predefined channels set up: cat, dog, bear, monkey")

    def introduce(self):
        # Provide an introduction and list of commands
        intro = """
        Hi, this is the one and only chatbot built for animals!
        You can join channels, chat, or ask me for fun facts and weather updates!
        Let's explore the options together—type away!
        """
        print(intro)

    def identify(self):
        # Ask the user for their username
        username = input("Please enter your username: ")

        # Check if the user already exists in Redis
        user_info = self.client.hgetall(f"user:{username}")

        if user_info:
            # User exists, retrieve their information
            print(f"Welcome back, {username}!")
            print(f"Details: {user_info}")
            # Load the user's subscribed channels from Redis
            self.subscribed_channels = [ch.decode() for ch in self.client.smembers(f"user:{username}:channels")]
        else:
            # New user, prompt for additional information
            print("It seems you're a new user. Let's get you set up!")
            age = input("Please enter your age: ")
            gender = input("Please enter your gender: ")
            location = input("Please enter your location: ")

            # Store the new user information in Redis using hset()
            self.client.hset(f"user:{username}", "username", username)
            self.client.hset(f"user:{username}", "age", age)
            self.client.hset(f"user:{username}", "gender", gender)
            self.client.hset(f"user:{username}", "location", location)
        
            print("Your information has been saved!")

        # Store the username in the instance variable for future reference
        self.username = username

    def join_channel(self):
            # Fetch predefined channels from Redis
            predefined_channels = [ch.decode() for ch in self.client.smembers("predefined_channels")]
            
            if not predefined_channels:
                print("No predefined channels found.")
                return
            
            # Display predefined channels to the user
            print("Available channels to join:")
            for i, channel in enumerate(predefined_channels, 1):
                print(f"{i}. {channel}")
            
            # Ask the user to select a channel
            try:
                choice = int(input("Enter the number of the channel you want to join: "))
                if 1 <= choice <= len(predefined_channels):
                    channel_to_join = predefined_channels[choice - 1]
                    
                    # Check if already subscribed
                    if self.client.sismember(f"user:{self.username}:channels", channel_to_join):
                        print(f"Already subscribed to channel: {channel_to_join}")
                    else:
                        self.pubsub.subscribe(channel_to_join)
                        self.client.sadd(f"user:{self.username}:channels", channel_to_join)
                        print(f"Joined channel: {channel_to_join}")
                else:
                    print("Invalid choice. Please enter a valid number.")
            except ValueError:
                print("Invalid input. Please enter a number.")

    def leave_channel(self):
        # Display the list of subscribed channels before asking the user to leave one
        subscribed_channels = self.client.smembers(f"user:{self.username}:channels")
        if not subscribed_channels:
            print("You have not joined any channels.")
            return
        
        print("You have joined the following channels:")
        subscribed_channels = [ch.decode() for ch in subscribed_channels]
        for i, channel in enumerate(subscribed_channels, 1):
            print(f"{i}. {channel}")
        
        # Prompt the user to choose a channel to leave by number
        try:
            choice = int(input("Enter the number of the channel you want to leave: "))
            if 1 <= choice <= len(subscribed_channels):
                channel_to_leave = subscribed_channels[choice - 1]
                self.pubsub.unsubscribe(channel_to_leave)
                self.client.srem(f"user:{self.username}:channels", channel_to_leave)
                print(f"Left channel: {channel_to_leave}")
            else:
                print("Invalid choice. Please enter a valid number.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    def listen_to_joined_channel(self):
        # Fetch subscribed channels from Redis
        subscribed_channels = self.client.smembers(f"user:{self.username}:channels")
        if not subscribed_channels:
            print("You have not joined any channels.")
            return
        
        subscribed_channels = [ch.decode() for ch in subscribed_channels]
        print("You have joined the following channels:")
        for i, channel in enumerate(subscribed_channels, 1):
            print(f"{i}. {channel}")
        
        # Ask the user to select a channel to listen to
        try:
            choice = int(input("Enter the number of the channel you want to listen to: "))
            if 1 <= choice <= len(subscribed_channels):
                channel_to_listen = subscribed_channels[choice - 1]
                print(f"Subscribing to channel '{channel_to_listen}'...")
                self.pubsub.subscribe(channel_to_listen)
                print(f"Now listening to channel '{channel_to_listen}'. Type 'quit' to stop listening.")
                
                # Start a separate thread for listening to messages
                listener_thread = threading.Thread(target=self.read_messages_from_channel, args=(channel_to_listen,))
                listener_thread.daemon = True
                listener_thread.start()
                
                # Loop for user input to quit listening
                while True:
                    command = input("").strip().lower()
                    if command == 'quit':
                        self.listening = False
                        self.pubsub.unsubscribe(channel_to_listen)
                        print(f"Stopped listening to channel '{channel_to_listen}'.")
                        break
            else:
                print("Invalid choice. Please enter a valid number.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    def read_messages_from_channel(self, channel_to_listen):
        # Separate thread function to listen for messages
        self.listening = True
        for message in self.pubsub.listen():
            if not self.listening:
                break
            if message['type'] == 'message' and message['channel'].decode() == channel_to_listen:
                print(f"Message from {message['channel'].decode()}: {message['data'].decode('utf-8')}")

    def send_message(self):
        # Fetch subscribed channels from Redis
        subscribed_channels = self.client.smembers(f"user:{self.username}:channels")
        if not subscribed_channels:
            print("You have not joined any channels.")
            return
        
        subscribed_channels = [ch.decode() for ch in subscribed_channels]
        print("You have joined the following channels:")
        for i, channel in enumerate(subscribed_channels, 1):
            print(f"{i}. {channel}")
        
        # Ask the user to select a channel to send the message
        try:
            choice = int(input("Enter the number of the channel to send your message: "))
            if 1 <= choice <= len(subscribed_channels):
                channel_to_send = subscribed_channels[choice - 1]
                message = input(f"What message do you want to send to {channel_to_send}? ")
                self.client.publish(channel_to_send, message)
                print(f"Message sent to {channel_to_send}: {message}")
            else:
                print("Invalid choice. Please enter a valid number.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    def channel_menu(self):
        while True:
            print("\nChannel Menu: What would you like to do?")
            print("1. Join a channel")
            print("2. Leave a channel")
            print("3. Start listening to an already joined channel")
            print("4. Send a message to a channel")
            print("5. Back to main menu")
            choice = input("Enter the number of your choice: ")

            if choice == '1':
                self.join_channel()
            elif choice == '2':
                self.leave_channel()
            elif choice == '3':
                self.listen_to_joined_channel()  # 调用封装的函数
            elif choice == '4':
                self.send_message()
            elif choice == '5':
                return
            else:
                print("Invalid choice. Please try again.")

    def provide_fact(self):
        # Provide a random fun fact from Redis
        facts = self.client.lrange("fun_facts", 0, -1)
        if facts:
            fact = random.choice(facts).decode('utf-8')
            print(f"Fun fact: {fact}")
        else:
            print("Sorry, no fun facts available right now.")

    def whoami(self):
        # Provide information about the user
        if self.username:
            user_info = self.client.hgetall(f"user:{self.username}")
            if user_info:
                print(f"Your details: {user_info}")
            else:
                print("No user information found.")
        else:
            print("You are not identified yet.")

    def provide_weather(self, city):
        # Provide mock weather data
        weather_data = self.client.hget("weather_data", city)
        if weather_data:
            print(f"The weather in {city} is: {weather_data.decode('utf-8')}")
        else:
            print(f"Sorry, I don't have weather data for {city}.")

    # Command Processing (for specific commands)
    def process_commands(self, message):
        if message == "!help":
            self.introduce()
        elif message.startswith("!weather"):
            parts = message.split(" ", 1)
            if len(parts) > 1:
                city = parts[1].strip().strip('"')
                self.provide_weather(city)
            else:
                print("Please specify a city.")
        elif message == "!fact":
            self.provide_fact()
        elif message == "!whoami":
            self.whoami()
        else:
            print("Unknown command")

    def specific_commands_menu(self):

        cities = [
            "New York", "Nashville", "London", "Paris", "Berlin",
            "Tokyo", "Sydney", "Toronto", "Beijing", "Mexico City"
        ]
        
        while True:
            print("\nSpecific Commands Menu: What would you like to do?")
            print("1. !help")
            print("2. !weather (choose from predefined cities)")
            print("3. !fact")
            print("4. !whoami")
            print("5. Back to main menu")
            choice = input("Enter the number of your choice or command: ")

            if choice == '1':
                self.process_commands("!help")
            elif choice == '2':
                print("Select a city:")
                for i, city in enumerate(cities, 1):
                    print(f"{i}. {city}")
                
                try:
                    city_choice = int(input("Enter the number of the city: "))
                    if 1 <= city_choice <= len(cities):
                        selected_city = cities[city_choice - 1]
                        self.process_commands(f"!weather {selected_city}")
                    else:
                        print("Invalid choice. Please enter a valid number.")
                except ValueError:
                    print("Invalid input. Please enter a number.")
            elif choice == '3':
                self.process_commands("!fact")
            elif choice == '4':
                self.process_commands("!whoami")
            elif choice == '5':
                return
            else:
                print("Invalid choice. Please try again.")

    # Main Menu
    def main_menu(self):
        while True:
            print("\nMain Menu: What would you like to do?")
            print("1. Channel-related commands")
            print("2. Specific commands (!help, !weather <city>, !fact, !whoami)")
            print("3. Quit")
            choice = input("Enter the number of your choice: ")

            if choice == '1':
                self.channel_menu()
            elif choice == '2':
                self.specific_commands_menu()
            elif choice == '3':
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")

    def store_mock_data(self):
        # Store mock data for weather and fun facts
        self.client.hset("weather_data", "New York", "Sunny and 75°F")
        self.client.hset("weather_data", "Nashville", "Rainy and 60°F")
        self.client.hset("weather_data", "London", "Cloudy and 60°F")
        self.client.hset("weather_data", "Paris", "Sunny and 72°F")
        self.client.hset("weather_data", "Berlin", "Rainy and 55°F")
        self.client.hset("weather_data", "Tokyo", "Humid and 80°F")
        self.client.hset("weather_data", "Sydney", "Warm and 78°F")
        self.client.hset("weather_data", "Toronto", "Cool and 50°F")
        self.client.hset("weather_data", "Beijing", "Sunny and 85°F")
        self.client.hset("weather_data", "Mexico City", "Rainy and 65°F")

        self.client.delete("fun_facts")
        self.client.rpush("fun_facts", "The term 'Data Science' was coined by William S. Cleveland in 2001.")
        self.client.rpush("fun_facts", "More data has been created in the past two years than in the entire previous history of the human race.")
        self.client.rpush("fun_facts", "Data scientists spend around 80% of their time cleaning and preparing data.")
        self.client.rpush("fun_facts", "The first modern computer, ENIAC, was built in 1945 and weighed about 27 tons.")
        self.client.rpush("fun_facts", "Data science is used to analyze customer data to help businesses personalize marketing efforts.")
        self.client.rpush("fun_facts", "The world creates about 2.5 quintillion bytes of data every day.")
        self.client.rpush("fun_facts", "Machine learning algorithms can outperform doctors at diagnosing certain types of cancer from images.")
        self.client.rpush("fun_facts", "Data science can help predict outcomes in sports, healthcare, finance, and more.")
        self.client.rpush("fun_facts", "Python is the most popular programming language for data science, followed by R.")
        self.client.rpush("fun_facts", "Data science can help reduce energy consumption by optimizing processes in industries like manufacturing.")
        self.client.rpush("fun_facts", "In 2020, the global data science and analytics market was valued at over $45 billion.")
        self.client.rpush("fun_facts", "Big data is used in sentiment analysis to gauge public opinion on social media.")
        self.client.rpush("fun_facts", "The Netflix recommendation engine saves the company $1 billion per year in customer retention.")
        self.client.rpush("fun_facts", "Data science plays a major role in self-driving car technology, such as Tesla's Autopilot.")
        self.client.rpush("fun_facts", "Natural language processing (NLP) allows computers to understand and interpret human language.")
        self.client.rpush("fun_facts", "Data science is essential for fraud detection in banking and finance.")
        self.client.rpush("fun_facts", "The demand for data scientists has grown by 650% since 2012.")

if __name__ == "__main__":
    bot = Chatbot()
    bot.setup_predefined_channels()
    bot.store_mock_data()
    bot.introduce()
    bot.identify()

    # Start the main interaction menu
    bot.main_menu()