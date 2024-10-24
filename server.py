import asyncio
from websockets.server import serve
import threading
import queue
import urls
import random
import math

# WS ASYNC SERVER
SERVER_PORT = 5060
SERVER_IP = "0.0.0.0"
#### HTTP PRODUCER
SERVICE_IP = "127.0.0.1"
SERVICE_PORT = 8000
#####

###############################
CLIENTS = set()
CLIENTS_IDS = set()
###############################

CLIENT_APPS = {}
URLS = {}


def getURLPath(path):
    return str(path).replace("/", "").lower()


def getClientId():
    return str(math.ceil(random.random() * 1000000))


def ClientIdExists(clientId):
    exists = False
    for clientId in CLIENTS_IDS:
        if clientId == clientId:
            exists = True
    return exists


def AppWorker(
    websocket, clients, clientsIds, _queue, _event, clientId, path, clientAppId
):
    App = URLS[path]
    asyncio.run(
        App(
            websocket, clients, clientsIds, _queue, _event, clientId, path, clientAppId
        ).run()
    )


def initAppThreads(websocket, path, clientId):
    clientAppId = getClientAppId(path, clientId)
    if path in URLS:
        _event = threading.Event()
        _queue = queue.Queue()
        _thread = threading.Thread(
            target=AppWorker,
            args=(
                websocket,
                CLIENTS,
                CLIENTS_IDS,
                _queue,
                _event,
                clientId,
                path,
                clientAppId,
            ),
        )
        _thread.start()
        CLIENT_APPS[clientAppId] = {
            "thread": _thread,
            "event": _event,
            "queue": _queue,
            "clientId": clientId,
            "path": path,
            "websocket": websocket,
        }
        _queue.put(
            {
                "clients": CLIENTS,
                "clientIds": CLIENTS_IDS,
                "clientId": clientId,
                "clientAppId": clientAppId,
                "path": path,
                "message": "",
            }
        )
    else:
        print("APP on path: " + path + " doesn't exist")


async def register(websocket, path, clientId):
    print("Path: " + path)
    ##############################################
    print(f"Client ID: " + clientId + " connected and registered")
    CLIENTS.add(websocket)
    CLIENTS_IDS.add(clientId)
    initAppThreads(websocket, path, clientId)
    ###############################################
    print(f"No of connected  clients: {len(CLIENTS)}")
    print(f"No of connected  clients Apps: {len(CLIENT_APPS)}")


async def unregister(websocket, path, clientId):
    clientAppId = getClientAppId(path, clientId)
    print("Path: " + path)
    print(f"Client ID closed: {clientId}")
    print(CLIENT_APPS)
    if len(CLIENTS) > 0 and ClientIdExists(clientId):
        CLIENT_APP = CLIENT_APPS[clientAppId]
        CLIENTS.remove(websocket)
        CLIENTS_IDS.remove(clientId)
        _thread = CLIENT_APP["thread"]
        _event = CLIENT_APP["event"]
        if _thread.is_alive():  # first stop the thread if it is still alive
            _event.set()
        ### remove session from SESSION QUE
        CLIENT_APPS.pop(clientAppId)
        print(f"Removed Client {clientId} App at path {path}")
        print(f"No of connected  clients Apps: {len(CLIENT_APPS)}")


async def NotifyListeners(message):
    print(f"Notifying listeners...")
    for client in CLIENTS:
        try:
            await client.send(message)
        except:
            pass


async def HandleClient(message, ws, path, clientId):
    clientAppId = getClientAppId(path, clientId)
    await NotifyListeners(message)
    CLIENT_APP = CLIENT_APPS[clientAppId]
    # print("Path: " + path)
    # print(f"Message: " + message)
    # print(f"From Client ID: " + clientId)
    _thread = CLIENT_APP["thread"]
    _event = CLIENT_APP["event"]
    _queue = CLIENT_APP["queue"]
    if _thread.is_alive():  # if thread is alive
        # send new client to all scrapping threads
        _queue.put(
            {
                "clients": CLIENTS,
                "clientIds": CLIENTS_IDS,
                "clientId": clientId,
                "clientAppId": clientAppId,
                "path": path,
                "message": message,
            }
        )


def getClientAppId(path, clientId):
    url_path = getURLPath(path)
    return f"{url_path}_{clientId}"


# Server
async def BrainServer(websocket, path):
    try:
        clientId = getClientId()
        await register(websocket, path, clientId)
        async for message in websocket:
            await HandleClient(message, websocket, path, clientId)
    finally:
        await unregister(websocket, path, clientId)
    print(f"No of connected  clients: {len(CLIENTS)}")
    print(f"No of connected  clients Apps: {len(CLIENT_APPS)}")


def initURLs():
    print("Initailizing apps urls...")
    for url in urls.urls:
        route = url["route"]
        app = url["app"]
        URLS[route] = app
    print(f"Initailizing {len(URLS)} apps urls")


# Main
async def Main():
    # Start server
    ################################
    async with serve(BrainServer, SERVER_IP, SERVER_PORT):
        print(f"Brain core running at port {SERVER_PORT}")
        initURLs()
        await asyncio.Future()  # run forever


#######################################################################
## RUN MIDDLEWARE SERVER AND JOB SHEDULER
asyncio.run(Main())
