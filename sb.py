# -*- coding: utf-8 -*-
from linepy import *
import json, time, random, urllib,requests,pytz,sys,os,codecs
from gtts import gTTS
from datetime import datetime


settingsOpen = codecs.open("temp.json", "r", "utf-8")
settings = json.load(settingsOpen)


client = LineClient(id='ennopratama11@gmail.com', passwd='cahklaten11')
#client = LineClient(authToken='AUTH TOKEN')
client.log("Auth Token : " + str(client.authToken))

channel = LineChannel(client)
client.log("Channel Access Token : " + str(channel.channelAccessToken))

poll = LinePoll(client)

cctv={
    "cyduk":{},
    "point":{},
    "sidermem":{}
}
k1MID = client.getProfile().mid
Bots = [k1MID]

wait={
    "autoJoin":True,
    "autoAdd":True
}


def mentionMembers(to, mid):
    try:
        arrData = ""
        textx = "Total Tag User「{}」\n\n  [ Tag ]\n1. ".format(str(len(mid)))
        arr = []
        no = 1
        num = 2
        for i in mid:
            mention = "@x\n"
            slen = str(len(textx))
            elen = str(len(textx) + len(mention) - 1)
            arrData = {'S': slen, 'E': elen, 'M': i}
            arr.append(arrData)
            textx += mention
            if no < len(mid):
                no += 1
                textx += "%i. " % (num)
                num = (num+1)
            else:
                try:
                    no = "\n╚══[ {} ]".format(str(client.getGroup(to).name))
                except:
                    no = "\n╚══[ Success ]"
        client.sendMessage(to, textx, {'MENTION': str('{"MENTIONEES":' + json.dumps(arr) + '}')}, 0)
    except Exception as error:
        client.sendMessage(to, "[ INFO ] Error :\n" + str(error))

while True:
    try:
        ops=poll.singleTrace(count=50)
        for op in ops:
            if op.type == 5:
                if wait["autoAdd"] == True:
            #if op.param3 in k4MID:
                    client.findAndAddContactsByMid(op.param1)
                    client.sendMessage(op.param1, "MAKASIH UDAH DI ADD YA :v")

            if op.type == 13:
                if k1MID in op.param3:
                    if wait["autoJoin"] == True:
                        client.acceptGroupInvitation(op.param1)
                        client.sendMessage(op.param1, "Hallo kakak kakak semua.. \n Perkenalkan saya Cubot \n Terimakasih sudah diajak join ke grup nya :D")

            if op.type == 26:
                msg = op.message
                if msg.text != None:
                    if msg.toType == 2:
                        may = client.getProfile().mid
                        if may in str(msg.contentMetadata) and 'MENTION' in str(msg.contentMetadata):
                            pilih = ['yang tag sy semoga jomblo seumur hidup','ngapain tag tag woe, kangen?','ada apa ini? ko di tag?','duhh kena tag, dianya kesepian kali yah','gk usah tag, gift tikel aja']
                            rslt = random.choice(pilih)
                            client.sendText(msg.to, str(rslt))
                        else:
                            pass
                    else:
                        pass
                else:
                    pass

                text = msg.text
                msg_id = msg.id
                receiver = msg.to
                sender = msg._from
                try:
                    if msg.contentType == 0:
                        if msg.toType == 2:
                            client.sendChatChecked(receiver, msg_id)
                            contact = client.getContact(sender)
                            if text.lower() == 'me':
                                client.sendMessage(receiver, None, contentMetadata={'mid': sender}, contentType=13)
                            elif text.lower() == 'speed':
                                start = time.time()
                                client.sendText(receiver, "TestSpeed")
                                elapsed_time = time.time() - start
                                client.sendText(receiver, "%sdetik" % (elapsed_time))
                            elif 'spic' in text.lower():
                                try:
                                    key = eval(msg.contentMetadata["MENTION"])
                                    u = key["MENTIONEES"][0]["M"]
                                    a = client.getContact(u).pictureStatus
                                    client.sendImageWithURL(receiver, 'http://dl.profile.line.naver.jp/'+a)
                                except Exception as e:
                                    client.sendText(receiver, str(e))
                            elif 'scover' in text.lower():
                                try:
                                    key = eval(msg.contentMetadata["MENTION"])
                                    u = key["MENTIONEES"][0]["M"]
                                    a = channel.getProfileCoverURL(mid=u)
                                    client.sendImageWithURL(receiver, a)
                                except Exception as e:
                                    client.sendText(receiver, str(e))
                            elif 'apakah ' in msg.text.lower():
                                try:
                                    txt = ['iya', 'tidak', 'bisa jadi']
                                    isi = random.choice(txt)
                                    tts = gTTS(text=isi, lang='id', slow=False)
                                    tts.save('temp2.mp3')
                                    client.sendAudio(receiver, 'temp2.mp3')
                                except Exception as e:
                                    client.sendText(receiver, str(e))
                            elif 'cubot' in msg.text.lower():
                                try:
                                    apa = ['iya ada apa kak ?', 'ada yang bisa cubot bantu ?']
                                    hasil = random.choice(apa)
                                    client.sendText(msg.to, str(hasil))
                                except Exception as e:
                                    client.sendText(receiver, str(e))

                            elif text.lower() == 'tagall':
                                group = client.getGroup(msg.to)
                                nama = [contact.mid for contact in group.members]
                                nm1, nm2, nm3, nm4, nm5, jml = [], [], [], [], [], len(nama)
                                if jml <= 10:
                                    client.mention(msg.to, nama)
                                if jml > 10 and jml < 20:
                                    for i in range (0, 9):
                                        nm1 += [nama[i]]
                                    client.mention(msg.to, nm1)
                                    for j in range (10, len(nama)-1):
                                        nm2 += [nama[j]]
                                    client.mention(msg.to, nm2)

                            elif text.lower() == ' cek sider':
                                try:
                                    client.sendText(msg.to,"Siap Laksanakan ..")
                                    del cctv['point'][msg.to]
                                    del cctv['sidermem'][msg.to]
                                    del cctv['cyduk'][msg.to]
                                except:
                                    pass
                                cctv['point'][msg.to] = msg.id
                                cctv['sidermem'][msg.to] = ""
                                cctv['cyduk'][msg.to]=True

                            elif text.lower() == 'offread':
                                if msg.to in cctv['point']:
                                    cctv['cyduk'][msg.to]=False
                                    client.sendText(msg.to, cctv['sidermem'][msg.to])
                                else:
                                    client.sendText(msg.to, "Heh belom di Set")
                except Exception as e:
                    client.log("[SEND_MESSAGE] ERROR : " + str(e))

            elif op.type == OpType.NOTIFIED_READ_MESSAGE:
                try:
                    if cctv['cyduk'][op.param1]==True:
                        if op.param1 in cctv['point']:
                            Name = client.getContact(op.param2).displayName
                            if Name in cctv['sidermem'][op.param1]:
                                pass
                            else:
                                cctv['sidermem'][op.param1] += "\n~ " + Name
                                pref=['eh ada','hai kak','aloo..','nah','lg ngapain','sini kak']
                                client.sendText(op.param1, str(random.choice(pref))+' '+Name)
                        else:
                            pass
                    else:
                        pass
                except:
                    pass

            else:
                pass

            # Don't remove this line, if you wan't get error soon!
            poll.setRevision(op.revision)
            
    except Exception as e:
        client.log("[SINGLE_TRACE] ERROR : " + str(e))
