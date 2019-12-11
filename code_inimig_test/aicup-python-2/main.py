import model
from stream_wrapper import StreamWrapper
from debug import Debug
from my_strategy import MyStrategy
import socket
import sys

import errno
from socket import error as socket_error


class Runner:
    def __init__(self, host, port, token):
        self.socket = socket.socket()
        self.socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, True)
        self.socket.connect((host, port))
        socket_stream = self.socket.makefile('rwb')
        self.reader = StreamWrapper(socket_stream)
        self.writer = StreamWrapper(socket_stream)
        self.token = token
        self.writer.write_string(self.token)
        self.writer.flush()

    def run(self):
        strategy = MyStrategy()
        debug = Debug(self.writer)

        while True:
            message = model.ServerMessageGame.read_from(self.reader)
            
            if message.player_view is None:
                print("THE AND")
                break
            player_view = message.player_view

            #print("Level:" , player_view.game.level)
            
            actions = {}
            cont = 0
            for unit in player_view.game.units:
                #print("cont = ", cont , " >>  my_id", player_view.my_id)
                #print("cont = ", cont , " >>   unit", unit)
                #print("cont = ", cont , " >>units::", player_view.game.units , "XXX")
                #print("cont = ", cont , " >>game::", player_view.game , "YYY")
                cont += 1
                if unit.player_id == player_view.my_id:
                    actions[unit.id] = strategy.get_action(unit, player_view.game, debug)
                else:
                    print("PLAYER:unit.position.x" , unit.position.x)
                    print("PLAYER:unit.position.y" , unit.position.y)
                    '''
                    print("PLAYER:unit" , unit)
                    print("PLAYER:unit.mines" , unit.mines)
                    print("PLAYER:unit.health" , unit.health)
                    print("PLAYER:unit.weapon" , unit.weapon)
                    print("PLAYER:unit.id" , unit.id)
                    print("PLAYER:unit.jump_state" , unit.jump_state)
                    print("PLAYER:unit.on_ground" , unit.on_ground)
                    print("PLAYER:unit.on_ladder" , unit.on_ladder)
                    print("PLAYER:unit.player_id" , unit.player_id)
                    print("PLAYER:unit.position" , unit.position)
                    print("PLAYER:unit.size" , unit.size)
                    print("PLAYER:unit.stand" , unit.stand)
                    print("PLAYER:unit.walked_right" , unit.walked_right)
                    print("PLAYER:unit_pos.y" , unit.position.y)
                    '''
            model.PlayerMessageGame.ActionMessage(model.Versioned(actions)).write_to(self.writer)
            self.writer.flush()


if __name__ == "__main__":
    host = "127.0.0.1" if len(sys.argv) < 2 else sys.argv[1]
    port = 31001 if len(sys.argv) < 3 else int(sys.argv[2])
    token = "0000000000000000" if len(sys.argv) < 4 else sys.argv[3]
    while True:
        try:
            Runner(host, port, token).run()
        except socket_error as s:
            print("WAIT... SOCKET PORT31001")
