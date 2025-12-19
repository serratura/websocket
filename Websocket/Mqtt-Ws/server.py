import asyncio
import json
import logging
import sys
import tornado.web
import tornado.websocket
import aiomqtt

if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

BROKER = "test.mosquitto.org"
TOPIC = "sensor/#"

clients = set()

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")

class SelectHandler(tornado.web.RequestHandler):
    def get(self):
        sensore = self.get_query_argument("sensor")
        self.render("selected.html", sensor=sensore)

class WSHandler(tornado.websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True

    def open(self):
        clients.add(self)

    def on_close(self):
        clients.remove(self)

async def mqtt_listener():
    async with aiomqtt.Client(BROKER) as client:
        await client.subscribe(TOPIC)

        async for message in client.messages:
            data = json.loads(message.payload.decode())
            ws_message = json.dumps({
                "type": "sensor",
                "data": data
            })

            for c in list(clients):
                await c.write_message(ws_message)

async def main():
    logging.basicConfig(level=logging.INFO)

    app = tornado.web.Application(
        [
            (r"/", MainHandler),
            (r"/selected", SelectHandler),
            (r"/ws", WSHandler),
        ],
        template_path="templates",
    )

    app.listen(8888)
    print("Server Tornado avviato su http://localhost:8888")

    await asyncio.gather(
        mqtt_listener(),
        asyncio.Event().wait()
    )

if __name__ == "__main__":
    asyncio.run(main())
