# Programming Assignment 2
###### 11911611张通
## Introduction
I have implemented all the tasks including bonus.There are 3 directories:http,ws-stream and ws-video
I think the stream live websocket includes websocket basic part.And u can see all the record of the backend by the console
- http includes the  implementation of basic danmaku by http
- ws-video is the implementation of video by websocket
- ws-stream is the implementation of stream-live by websocket

## http
### model
#### front end
- every 10000 miliseconds,front end will send a get with path="/polling" to ask for new danmaku.After it gets a list of danmaku,it will add it to the screen.
- when user click the button,the front end will  send the danmaku to the backend by post http.

#### back end
- the back end own a damaku_list,when get a get request with "/polling",it will return last 5 items to the front end.(when there are 5 new damaku,the old will be trunked)
- if the back end get a post request,it will append it into the damaku_list.
### result
I have tested on three tabs.All the three can gain the danmaku from each other.
![image.png](https://s2.loli.net/2022/04/27/OBZtWi14yL7hmwG.png)
## websocket video
### model
#### front end
- every 150 miliseconds,the front end send a message which is["","",timestamp]to ask for all the danmaku at the same stamp.
- when user  click the button,the front end will  send [name,danmaku,timestamp] to the backend by websocket.Name is a random string
- when front end recieve message,if the answe is not "no-message",it will add the text to the screen.
#### back end
- the backend has a dictionary.The key is the timestamp and the values are the list of corresponding danmaku.
- if the back end get a message,the message will be split into three parts:name,msg, time
- if name is ''.If there is timestamp in the dictionary,return the list.Otherwise,send 'no-message'
- if name is not '',append the new danmaku into the corresponding list in the dictionary 
### result
when send from one tab,another also show the danmaku
![image.png](https://s2.loli.net/2022/04/27/4eOguSHDvt1ACfU.png)
change the progress bar,the same danmaku appears again
![image.png](https://s2.loli.net/2022/04/27/2PNgFV1HuT3EpDA.png)
## websocket stream
### model
#### front end
- every 50 miliseconds,the front end send a message which is["",""]to ask for the newest chatbox text.
- intialize a random string as a name binding the websocket
- when front end recieve message,if the type field is "da",add the new danmaku.refresh the chatbox at the same time
- when user  click the button,the front end will  send [name,danmaku] to the backend by websocket.

#### back end
- use a set users record all the websocket .When message comes,add it into the set
- use a list to record all the time,name and damakus
- when a message comes,split it into two parts:name and damaku
- name is "" meaning that the query is ask for the new chatbox.send the chatbox to specific websocket
- name is not "".append the time,name and damaku into the text list and send all websockets the new damaku and chatbox

### result
The video is stream.
Each tab can see wthe new damaku and there is a chatbox recording sometime somebody say something
![image.png](https://s2.loli.net/2022/04/27/8Be25wJqS3l1xnC.png)
open a new tab,you can still see the history chat in the chatbox
![image.png](https://s2.loli.net/2022/04/27/eLIE9PMk61ymQXg.png)
## websocket http comparision
### model design
I can only use polling to get new dnamaku in frontend for http and there is layout.
For websocket,I proactively send the new danmaku to all the websockets and there is no layout
- websocket can send message proactively both from backend to frontend and from frontend to backend.
- http can only send message proactively from frontend to backend and backend can only get message in the response


### network traffic
Below is the io graph under websocket live
![image.png](https://s2.loli.net/2022/04/27/xI4XVdsofgvFyWT.png)
Below is the io graph under http
![image.png](https://s2.loli.net/2022/04/27/bwA6d4x3Z8TIqQJ.png)
we can clearly see that websocket's connection does not close so that the packages does not drop down to 0
The http io graph is up and down ,which shows that there is a polling.
Websocket can keep  much more packets without an error . http make tcp errors with much less packets.
In a conclusion,websocket is mor stable and efficiency.
## upgrade efficiency
The websocket program is much easier to upgrade.Actually,I used try to use http to implement the stream live and video.
However,there is no need for polling and handling with complex headers  for websocket.I think websocket is a better choice if u wanna manage a network program and keep contributing for it.