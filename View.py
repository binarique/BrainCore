from App import App


async def App1(websocket, _queue, _event, clientId, path, clientAppId):
    print("\n ############ FROM APP ##################")
    print("App Client: " + clientId)
    print("App Path: " + path)
    print("App clientAppId: " + clientAppId)
    print("\n ############ END APP ##################")
    while True:
        try:
            print(f"Waiting for data from path {path} from client {clientId}")
            data = _queue.get()
            if not (data is None):
                print(f"Got data in path {path} from client {clientId}: {data}")
            else:
                print(f"No data in path {path} from client {clientId}")
        except:
            print(f"Unknown Error from path {path} from client {clientId}")


async def ChatBot(websocket, _queue, _event, clientId, path, clientAppId):
    print("\n ############ FROM APP 2 ##################")
    print("App 2 Client: " + clientId)
    print("App 2 Path: " + path)
    print("App 2 clientAppId: " + clientAppId)
    print("\n ############ END APP 2 ##################")
    while True:
        try:
            print(f"App 2 Waiting for data from path {path} from client {clientId}")
            data = _queue.get()
            if not (data is None):
                print(f"App 2 Got data in path {path} from client {clientId}: {data}")
            else:
                print(f"App 2 No data in path {path} from client {clientId}")
        except:
            print(f"App 2 Unknown Error from path {path} from client {clientId}")


class MyApp(App):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.additional_data = None

    async def handle_data(self, data):
        """Processes incoming data and performs additional actions."""
        await super().handle_data(data)  # Call the parent's handle_data method
        self.additional_data = data  # Store additional data for later use
        # await self.send_response(data)  # Send a custom response
        print(f"Class Got data in path: {data}")
        print("Yes we are running a child class yeah")
        print(f"Data send from {self.path} from client {self.clientId}")
        print(
            f"App {self.path} with client ID: {self.clientId} no of connected clients: {len(self.clients)}"
        )

        self.clients

    async def send_response(self, data):
        """Sends a custom response to the client."""
        # Implement your custom response logic here
        await self.websocket.send_str(f"Received data: {data}")


# class App:
#     """Handles WebSocket connections and processes data asynchronously."""

#     def __init__(self, websocket, queue, event, clientId, path, clientAppId):
#         self.websocket = websocket
#         self.queue = queue
#         self.event = event
#         self.clientId = clientId
#         self.path = path
#         self.clientAppId = clientAppId

#     async def handle_data(self, data):
#         """Processes incoming data."""
#         print(f"Got data in path {self.path} from client {self.clientId}: {data}")
#         # Add your custom data processing logic here

#     async def run(self):
#         """Main loop for handling WebSocket connections."""
#         while True:
#             try:
#                 data = await self.queue.get()
#                 if data is not None:
#                     await self.handle_data(data)
#                 else:
#                     print(f"No data in path {self.path} from client {self.clientId}")
#             except Exception as e:
#                 print(
#                     f"Error processing data from path {self.path} from client {self.clientId}: {e}"
#                 )
