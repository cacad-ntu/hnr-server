"""
Main function to handle websocket
"""

import argparse
import json
import signal

import tornado.ioloop
import tornado.web
import tornado.websocket

from Engine import Engine
from Constants import Constants


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
        for client in CLIENTS:
            if client[0] == self:
                player = GE.players[client[1]]
                payload = {"player_id": player.id, "row": Constants.ROW, "col": Constants.COL}
                msg = {"type": MSG_REGISTER, "payload": payload}
                self.write_message(msg)
                print("Client count: ", len(CLIENTS))
                return
        player = GE.spawn_player()
        CLIENTS.append([self, player.id])
        payload = {"player_id": player.id, "row": Constants.ROW, "col": Constants.COL}
        msg = {"type": MSG_REGISTER, "payload": payload}
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
                GE.remove_player(client[1])
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
    sorted_players = GE.get_sorted_players()

    for player, pid in CLIENTS:
        msg = {}
        payload = {}
        payload["player_id"] = pid
        payload["points"] = GE.players[pid].points

        if GE.players[pid].isDead:
            msg["type"] = MSG_DEAD
            msg["payload"] = payload

            player.write_message(msg)
            player.on_close()
            continue

        payload["players"] = sorted_players
        payload["map"] = GE.arena
        payload["player_map"] = GE.players[pid].playerMap
        payload["towers"] = GE.get_all_towers()
        payload["hqs"] = GE.get_all_hqs()
        payload["tower_max_hp"] = Constants.TOWER_HP
        payload["hq_max_hp"] = Constants.HQ_HP

        msg["type"] = MSG_UPDATE
        msg["payload"] = payload

        player.write_message(msg)

def parse_argument():
    """ Argument parser """
    parser = argparse.ArgumentParser()
    parser.add_argument("--bfs", help="Use bfs in finding path", action="store_true")
    arguments = parser.parse_args()
    return arguments

def main(arg):
    """ Main function """
    signal.signal(signal.SIGINT, signal_handler)

    if arg.bfs:
        GE.toggle_bfs(True)

    callback = tornado.ioloop.PeriodicCallback(update_client, CALLBACK_TIME)
    callback.start()

    app = make_app()
    app.listen(WS_PORT)

    print("Listening at port ", WS_PORT)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    args = parse_argument()
    main(args)
