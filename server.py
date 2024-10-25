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
THREAD_LIMIT = 500
JOIN_THREADS = False
#### HTTP PRODUCER
SERVICE_IP = "127.0.0.1"
SERVICE_PORT = 8000
#####

###############################
CLIENTS = set()
CLIENTS_IDS = set()
###############################

CLIENT_APPS = {}
PATHS = {}


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


def AppWorker(websocket, clients, clientsIds, _queue, clientId, path, clientAppId):
    App = PATHS[path]
    asyncio.run(
        App(websocket, clients, clientsIds, _queue, clientId, path, clientAppId).run()
    )


def initApps(websocket, path, clientId):
    clientAppId = getClientAppId(path, clientId)
    if path in PATHS:
        _queue = queue.Queue()
        _thread = threading.Thread(
            target=AppWorker,
            args=(
                websocket,
                CLIENTS,
                CLIENTS_IDS,
                _queue,
                clientId,
                path,
                clientAppId,
            ),
        )
        _thread.start()
        CLIENT_APPS[clientAppId] = {
            "thread": _thread,
            "queue": _queue,
            "clientId": clientId,
            "path": path,
            "websocket": websocket,
        }
        # Thread que
        _queue.put(
            {
                "event": "open",
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
    initApps(websocket, path, clientId)
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
        _queue = CLIENT_APP["queue"]
        if _thread.is_alive():  # if thread is alive
            # send message to apps
            try:
                _queue.put(
                    {
                        "event": "close",
                        "clients": CLIENTS,
                        "clientIds": CLIENTS_IDS,
                        "clientId": clientId,
                        "clientAppId": clientAppId,
                        "path": path,
                        "message": "",
                    }
                )
            except Exception as e:
                print(f"Error: {e}")
        ### remove session from SESSION QUE
        CLIENT_APPS.pop(clientAppId)
        print(f"Removed Client {clientId} App at path {path}")
        print(f"No of connected  clients Apps: {len(CLIENT_APPS)}")


# Client Handler
async def HandleClient(message, ws, path, clientId):
    clientAppId = getClientAppId(path, clientId)
    CLIENT_APP = CLIENT_APPS[clientAppId]
    # print("Path: " + path)
    # print(f"Message: " + message)
    # print(f"From Client ID: " + clientId)
    _thread = CLIENT_APP["thread"]
    _queue = CLIENT_APP["queue"]
    if _thread.is_alive():  # if thread is alive
        # send message to apps
        _queue.put(
            {
                "event": "message",
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
        path = url["path"]
        app = url["app"]
        PATHS[path] = app
    print(f"Initailizing {len(PATHS)} apps urls")


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
