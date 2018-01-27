"""
Main function to handle websocket
"""

import json
import signal

import tornado.ioloop
import tornado.web
import tornado.websocket

from Engine import Engine


# WEBSOCKET SETTINGS
WS_PORT = 8888
CALLBACK_TIME = 300

# WEBSOCKET MESSAGE
MSG_REGISTER = 0
MSG_UPDATE = 1
MSG_DEAD = 2

# GAME SETTINGS
CLIENTS = []
GE = Engine()

class MainHandler(tornado.web.RequestHandler):
    """
    Http handler
    """
    def get(self):
        self.render("index.html")


class SocketHandler(tornado.websocket.WebSocketHandler):
    """
    Websocket handler
    """
    def check_origin(self, origin):
        return True

    def open(self):
        """ On open connection """
        if self not in CLIENTS:
            player = GE.spawn_player()
            CLIENTS.append([self, player.id])

        msg = {"type": MSG_REGISTER, "player": player.id}
        self.write_message(msg)
        print("Client count: ", len(CLIENTS))

    def on_message(self, msg):
        """ On message connection """
        command = json.loads(msg)
        GE.issue_command(command["player_id"], command["units"], command["dest"])
        print("[Client] Message from client", command["player_id"])

    def on_close(self):
        """ On close connection """
        for client in CLIENTS:
            if client[0] == self:
                CLIENTS.remove(client)
        print("Client count: ", len(CLIENTS))


def signal_handler(signum, frame):
    """ Keyboard interupt handler """
    tornado.ioloop.IOLoop.instance().stop()

def make_app():
    """ handler """
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/ws", SocketHandler),
    ])

def update_client():
    """ Update every clients """
    GE.update()

    for player, pid in CLIENTS:
        msg = {}
        if GE.players[pid].isDead:
            msg["type"] = MSG_DEAD
            player.write_message(msg)
            player.on_close()
            continue

        msg["type"] = MSG_UPDATE
        msg["map"] = GE.arena
        msg["player_map"] = GE.players[pid].playerMap
        player.write_message(msg)

def main():
    """ Main function """
    signal.signal(signal.SIGINT, signal_handler)

    callback = tornado.ioloop.PeriodicCallback(update_client, CALLBACK_TIME)
    callback.start()

    app = make_app()
    app.listen(WS_PORT)

    print("Listening at port ", WS_PORT)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
