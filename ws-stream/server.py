import asyncio
import websockets
import datetime
import json

class DanmakuServer:
    """
    Receive danmakus from clients, reply them correctly
    """

    def __init__(self):
        self.texts = []#record the chat box
        self.users=set()#record all the websocket
    async def reply(self, websocket):
        while True:
            text = await websocket.recv()
            self.users.add(websocket)#add websocket
            name, msg = text.split(",")
            if name != "":# name is not "" meaning that new danmaku comes
                current_time = datetime.datetime.now()#record cureent time
                self.texts.append(str(current_time)+"   "+name+":"+msg)#concat the info when,who and say what
                all="\n".join(self.texts)
                c_j = json.dumps({"type": "da", "content": msg,"all":all})
                await asyncio.wait([user.send(c_j) for user in self.users])#send to all websocket
            else:#refresh the chatbox
                all = "\n".join(self.texts)
                c_j = json.dumps({"type": "no", "all": all})
                print(self.texts)
                await websocket.send(c_j)





if __name__ == "__main__":
    server = DanmakuServer()
    asyncio.get_event_loop().run_until_complete(
        websockets.serve(server.reply, 'localhost', 8765))
    asyncio.get_event_loop().run_forever()
