from app import App
import time


class MyApp(App):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.additional_data = None
        print(f"CLIENT: {self.clientId}, PATH: {self.path}")

    async def OnMessage(self, event):
        await super().OnMessage(event)  # Call the parent's OnMessage method
        # TO DO ::
        print(
            f"\n############################# {self.clientId} ##################################"
        )
        for i in range(1, 10):
            print(f"Counting from 1-10 in client {self.clientId}: {i}")
            time.sleep(3)
        await self.Send(
            f"One:::Recieved message {event['message']} from client {self.clientId}"
        )
        print(f"Class Got data in path: {event}")
        print("Yes we are running a child class yeah")
        print(f"Data send from {self.path} from client {self.clientId}")
        print(
            f"### App {self.path} with client ID: {self.clientId} no of connected clients: {len(self.clients)} ####"
        )
        print(
            f"\n############################# {self.clientId} END ##################################"
        )

    async def OnOpen(self, event):
        await super().OnOpen(event)  # Call the parent's onOpen method
        print("\n ############ MY APP CONNECTED ##################")
        print("*************************************")
        print("********* CONNECTED *****************")
        print("*************************************")
        print("MY Client: " + self.clientId)
        print("MY Path: " + self.path)
        print("MY clientAppId: " + self.clientAppId)
        print("\n ############ MY APP ##################")

    async def OnClose(self, event):
        await super().OnClose(event)  # Call the parent's onClose method
        print("\n ############ MY APP CLOSED ##################")
        print("*************************************")
        print("********* CLOSED *****************")
        print("*************************************")
        print("MY Client: " + self.clientId)
        print("MY Path: " + self.path)
        print("MY clientAppId: " + self.clientAppId)
        print("\n ############ MY APP ##################")


class ChatBot(App):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.additional_data = None
        print(f"CLIENT: {self.clientId}, PATH: {self.path}")

    async def OnMessage(self, event):
        await super().OnMessage(event)  # Call the parent's OnMessage method
        # TO DO ::
        print(
            f"\n############################# CHAT BOT APP ON MESSAGE {self.clientId} ##################################"
        )
        for i in range(1, 10):
            print(f"CHAT BOT APP counting from 1-10 in client {self.clientId}: {i}")
            time.sleep(3)
        await self.SendToAll(
            f"All:::Recieved message {event['message']} from client {self.clientId}"
        )
        print(f"Class Got data in path: {event}")
        print("Yes we are running a child class yeah")
        print(f"Data send from {self.path} from client {self.clientId}")
        print(
            f"### App {self.path} with client ID: {self.clientId} no of connected clients: {len(self.clients)} ####"
        )
        print(
            f"\n############################# CHAT BOT APP {self.clientId} END ##################################"
        )

    async def OnOpen(self, event):
        await super().OnOpen(event)  # Call the parent's onOpen method
        print("\n ############ CHAT BOT APP CONNECTED ##################")
        print("*************************************")
        print("********* CONNECTED *****************")
        print("*************************************")
        print("CHAT BOT Client: " + self.clientId)
        print("CHAT BOT Path: " + self.path)
        print("CHAT BOT clientAppId: " + self.clientAppId)
        print("\n ############ CHAT BOT APP ##################")

    async def OnClose(self, event):
        await super().OnClose(event)  # Call the parent's onClose method
        print("\n ############ CHAT BOT APP CLOSED ##################")
        print("*************************************")
        print("********* CLOSED *****************")
        print("*************************************")
        print("CHAT BOT Client: " + self.clientId)
        print("CHAT BOT Path: " + self.path)
        print("CHAT BOT clientAppId: " + self.clientAppId)
        print("\n ############ CHAT BOT APP ##################")
