import asyncio
import websockets


class DanmakuServer:
    """
    Receive danmakus from clients, reply them correctly
    """
    def __init__(self):
        # a damaku dictionary.keys are time stamps,value is a list of the damaku at the same time
        self.texts={}

    async def reply(self, websocket):
        while True:
            text = await websocket.recv()
            name,msg, time = text.split(",")#get the name,msg and time
            if name=='':#if name is '',return a list of corresponding danmaku
                if time  in self.texts.keys():
                    all="$".join(self.texts[time])
                    await websocket.send(all)
                else:
                    await websocket.send("no-message")#return no-message if there is no damaku for the timestamp
            else:
                if time not in self.texts.keys():#if there is no time in the keys of texts,initiate one
                    self.texts[time]=[]
                self.texts[time].append(msg)#append new damaku in the corresponding list in the dictionary
                print(self.texts)






if __name__ == "__main__":
    server = DanmakuServer()
    asyncio.get_event_loop().run_until_complete(
        websockets.serve(server.reply, 'localhost', 8765))
    asyncio.get_event_loop().run_forever()
