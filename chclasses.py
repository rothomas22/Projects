class Channels:

    counter = 1

    def __init__(self, channelname):

        # Keep track of id number.
        self.id = Channels.counter
        Channels.counter += 1

        # Keep track of mesages.
        self.messages = []

        # Details about flight.
        self.channelname = channelname


    def print_info(self):
        print(f"Channel name: {self.channelname}")

        print()
        print("Messages:")
        for message in self.messages:
            print(f"{message.messagetext}")

    
    def add_message(self, m):
        self.messages.append(m)
        m.channel_id = self.id


class Message:

    def __init__(self, messageText, personName, msgdate):
        self.messageText = messageText
        self.personName = personName
        self.msgdate = msgdate
