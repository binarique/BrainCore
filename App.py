import asyncio


class App:
    """Handles WebSocket connections and processes data asynchronously."""

    def __init__(
        self, websocket, clients, clientsIds, queue, event, clientId, path, clientAppId
    ):
        self.websocket = websocket
        self.clients = clients
        self.clientsIds = clientsIds
        self.queue = queue
        self.event = event
        self.clientId = clientId
        self.path = path
        self.clientAppId = clientAppId

    def UpdateClients(self):
        pass

    async def handle_data(self, data):
        # TO DO ::
        """Processes incoming data."""

    async def run(self):
        """Main loop for handling WebSocket connections."""
        while True:
            try:
                data = self.queue.get()
                if data is not None:
                    await self.handle_data(data)
                else:
                    print(f"No data in path {self.path} from client {self.clientId}")
            except Exception as e:
                print(
                    f"Error processing data from path {self.path} from client {self.clientId}: {e}"
                )
