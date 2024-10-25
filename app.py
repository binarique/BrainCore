import asyncio


class App:
    """Handles WebSocket connections and processes data asynchronously."""

    def __init__(self, ws, clients, clientsIds, queue, clientId, path, clientAppId):
        self.ws = ws
        self.clients = clients
        self.clientsIds = clientsIds
        self.queue = queue
        self.clientId = clientId
        self.path = path
        self.clientAppId = clientAppId
        print(f"*****CLIENT: {self.clientId}, PATH: {self.path}****")

    async def OnMessage(self, event):
        # TO DO ::
        """Processes incoming data."""

    async def OnOpen(self, event):
        # TO DO ::
        """On client connected."""

    async def OnClose(self, event):
        # TO DO ::
        """Processes client closed."""

    async def Send(self, message):
        """Sends to the current client in this thread"""
        try:
            await self.ws.send(message)
        except Exception as e:
            print(f"Failed to send message to current client because: {e}")

    def SendAsync(self, message):
        """Sends to the current client in this thread"""
        pass
        # try:
        #     await self.ws.send(message)
        # except Exception as e:
        #     print(f"Failed to send message to current client because: {e}")

    async def SendToAll(self, message):
        """Sends to all clients"""
        for client in self.clients:
            try:
                await client.send(message)
            except Exception as e:
                print(
                    f"Failed to send message to {len(self.clients)} clients because: {e}"
                )

    async def SendAsyncToAll(self, message):
        """Sends to all clients"""
        for client in self.clients:
            try:
                await client.send(message)
            except Exception as e:
                print(
                    f"Failed to send message to {len(self.clients)} clients because: {e}"
                )

    async def run(self):
        """Main loop for handling WebSocket connections."""
        while True:
            try:
                data = self.queue.get()
                if data is not None:
                    if "event" in data:
                        event = data["event"]
                        if event == "open":
                            await self.OnOpen(data)
                        elif event == "message":
                            await self.OnMessage(data)
                        elif event == "close":
                            await self.OnClose(data)
                        else:
                            # You can't be serious, this too??
                            print(
                                f"Unknown event on {self.path} from client {self.clientId}"
                            )
                    else:
                        print(
                            f"Unknown event on {self.path} from client {self.clientId}"
                        )
                else:
                    print(f"No data in path {self.path} from client {self.clientId}")
            except Exception as e:
                print(
                    f"Error processing data from path {self.path} from client {self.clientId}: {e}"
                )
