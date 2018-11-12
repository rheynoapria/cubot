# -*- coding: utf-8 -*-
from linepy import *
from akad.ttypes import *
import json, time, random, urllib,requests,pytz,sys,os,codecs,re,ast,thrift,pafy
import six.moves.urllib as urllibb
from bs4 import BeautifulSoup
from gtts import gTTS
from threading import Thread
from datetime import datetime



settingsOpen = codecs.open("temp.json", "r", "utf-8")
settings = json.load(settingsOpen)


client = LineClient(id='ennopratama11@gmail.com', passwd='cahklaten11')
#client = LineClient(authToken='AUTH TOKEN')
client.log("Auth Token : " + str(client.authToken))
channel = LineChannel(client)
client.log("Channel Access Token : " + str(channel.channelAccessToken))

poll = LinePoll(client)

bisaApa="""Cubot bisa jawab pertanyaan kakak, bisa tau siapa yang baca chat line,
bisa juga ngambil profile orang atau foto cover orang, cubot juga bisa ngetag semua
member yang ada di grup ini :D
"""
mulai = time.time()

korban=[]
msg_dict = {}

cctv={
    "cyduk":{},
    "point":{},
    "sidermem":{}
}
mid = client.getProfile().mid
Bots = [mid]

wait={
    "autoJoin":True,
    "autoAdd":True,
    "UnsendPesan":True
}



admin = 'u2eff00efff34f390bb83735c1de0eeea'


# def restart_program():
#     python = sys.executable
#     os.execl(python, python, * sys.argv)
#     client.sendText(receiver, 'Restarting Server Prosses..')


def waktu(secs):
    mins, secs = divmod(secs,60)
    hours, mins = divmod(mins,60)
    days, hours = divmod(hours,24)
    weeks, days = divmod(days,7)
    months, weeks = divmod(weeks,4)
    text = ""
    if months != 0: text += "%02d Bulan" % (months)
    if weeks != 0: text += " %02d Minggu" % (weeks)
    if days != 0: text += " %02d Hari" % (days)
    if hours !=  0: text +=  " %02d Jam" % (hours)
    if mins != 0: text += " %02d Menit" % (mins)
    if secs != 0: text += " %02d Detik" % (secs)
    if text[0] == " ":
		text = text[1:]
    return text


def logError(text):
    client.log("[ ERROR ] {}".format(str(text)))
    tz = pytz.timezone("Asia/Makassar")
    timeNow = datetime.now(tz=tz)
    timeHours = datetime.strftime(timeNow, "(%H:%M)")
    day = ["Sunday", "Monday", "Tuesday",
           "Wednesday", "Thursday", "Friday", "Saturday"]
    hari = ["Minggu", "Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"]
    bulan = ["Januari", "Februari", "Maret", "April", "Mei", "Juni",
             "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
    inihari = datetime.now(tz=tz)
    hr = inihari.strftime('%A')
    bln = inihari.strftime('%m')
    for i in range(len(day)):
        if hr == day[i]:
            hasil = hari[i]
    for k in range(0, len(bulan)):
        if bln == str(k):
            bln = bulan[k-1]
    time = "{}, {} - {} - {} | {}".format(str(hasil), str(inihari.strftime('%d')), str(
        bln), str(inihari.strftime('%Y')), str(inihari.strftime('%H:%M:%S')))
    with open("errorLog.txt", "a") as error:
        error.write("\n[{}] {}".format(str(time), text))



def bot(op):
        try :
            if op.type == 5:
                if wait["autoAdd"] == True:
                    #if op.param3 in k4MID:
                    client.findAndAddContactsByMid(op.param1)
                    client.sendMessage(op.param1, "MAKASIH UDAH DI ADD YA :v")

            if op.type == 13:
                if mid in op.param3:
                    if wait["autoJoin"] == True:
                        client.acceptGroupInvitation(op.param1)
                        client.sendMessage(op.param1, "Hallo kakak kakak semua.. \n Perkenalkan saya Cubot \n Terimakasih sudah diajak join ke grup nya :D")

            if op.type == 65:
                if wait['UnsendPesan'] == True:
                    try:
                        to = op.param1
                        sender = op.param2
                        if sender in msg_dict:
                            unsendTime = time.time()
                            sendTime = unsendTime - msg_dict[sender]["createdTime"]
                            sendTime = waktu(sendTime)
                            pelaku = client.getContact(msg_dict[sender]["pelaku"])
                            nama = pelaku.displayName
                            dia = "========> Detect Pesan Terhapus"
                            dia += "\n||---------------------------------------"
                            dia += "\n|| Pengirim : @! \n\n"
                            dia += "\n\n|| Kapan   : {} yang lalu".format(str(sendTime))
                            dia += "\n|| Pesannya : {}".format(str(msg_dict[sender]["rider"]))
                            dia += "\n||----------------------------------------"
                            client.sendMention(to, dia,[pelaku.mid])
                    except:
                        client.sendMessage(to, "Return")

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
                        if wait["UnsendPesan"] == True:
                            unsendTime = time.time()
                            msg_dict[msg_id] = {"rider": text, "pelaku": sender, "createdTime": unsendTime, "contentType": msg.contentType, "contentMetadata": msg.contentMetadata}

                        if msg.toType == 2:
                            client.sendChatChecked(receiver, msg_id)
                            contact = client.getContact(sender)
                            if text.lower() == 'me':
                                a = client.getContact(sender).mid
                                client.sendMessage(receiver, None, contentMetadata={'mid': sender}, contentType=13)
                                print(a)
                            elif text.lower() == 'speed':
                                start = time.time()
                                client.sendText(receiver, "Menghitung Kecepatan..")
                                elapsed_time = time.time() - start
                                client.sendText(receiver, "%sdetik" % (elapsed_time))
                            
                            elif text.lower().startswith("runtime"):
                                if sender in admin:
                                    eltime = time.time() - mulai                                
                                    opn = " "+waktu(eltime)
                                    client.sendText(receiver,"Bot Telah Aktif Selama\n" + opn)

                            elif text.lower().startswith("restart bot"):
                                if sender in admin:
                                    client.sendText(receiver, 'Restarting Server Prosses..')
                                    print ("Restarting Server")
                                    python = sys.executable
                                    os.execl(python, python, * sys.argv)
                                    client.sendText(receiver, 'Bot telah aktif..')
                            elif text.lower().startswith("grup info"):
                                if sender in admin:
                                    group = client.getGroup(receiver)
                                    try:
                                        gCreator = group.creator.displayName
                                    except:
                                        gCreator = "Tidak ditemukan"
                                    if group.invitee is None:
                                        gPending = "0"
                                    else:
                                        gPending = str(len(group.invitee))
                                
                                    cuki = "INFO GRUP"
                                    cuki += "\nNama Group : {}".format(str(group.name))
                                    cuki += "\nID Group :\n? {}".format(group.id)
                                    cuki += "\nPembuat : {}".format(str(gCreator))
                                    cuki += "\nJumlah Member : {}".format(str(len(group.members)))
                                    cuki += "\nJumlah Pending : {}".format(gPending)
                                    client.sendMessage(receiver, str(cuki))
                            # elif 'steal picture ' in text.lower():
                            #     try:
                            #         key = eval(msg.contentMetadata["MENTION"])
                            #         u = key["MENTIONEES"][0]["M"]
                            #         a = client.getContact(u).pictureStatus
                            #         client.sendImageWithURL(receiver, 'http://dl.profile.line.naver.jp/'+a)
                            #     except Exception as e:
                            #         client.sendText(receiver, str(e))

                            elif "Pp @" in msg.text:
                                if msg.toType == 2:
                                    cover = msg.text.replace("Pp @","")
                                    _nametarget = cover.rstrip('  ')
                                    gs = client.getGroup(msg.to)
                                    targets = []
                                    for g in gs.members:
                                        if _nametarget == g.displayName:
                                            targets.append(g.mid)
                                    if targets == []:
                                        client.sendText(msg.to,"Not found")
                                    else:
                                        for target in targets:
                                            try:
                                                h = client.getContact(target)
                                                client.sendImageWithURL(msg.to,"http://dl.profile.line-cdn.net/" + h.pictureStatus)
                                            except Exception as error:
                                                print error
                                                client.sendText(msg.to,"Upload image failed.")
                            elif 'steal cover ' in text.lower():
                                try:
                                    key = eval(msg.contentMetadata["MENTION"])
                                    u = key["MENTIONEES"][0]["M"]
                                    a = channel.getProfileCoverURL(mid=u)
                                    client.sendImageWithURL(receiver, a)
                                except Exception as e:
                                    client.sendText(receiver, str(e))


                            elif 'apakah ' in msg.text.lower():
                                try:
                                    txt = [
                                        'iya', 'tidak', 'bisa jadi', 'mungkin saja', 'tidak mungkin', 'au ah gelap']
                                    isi = random.choice(txt)
                                    tts = gTTS(text=isi, lang='id', slow=False)
                                    tts.save('temp2.mp3')
                                    client.sendAudio(receiver, 'temp2.mp3')
                                except Exception as e:
                                    client.sendText(receiver, str(e))
                            
                            elif 'kapan ' in msg.text.lower():
                                rnd = ["kapan kapan","besok","satu abad lagi","Hari ini","Tahun depan","Minggu depan","Bulan depan","Sebentar lagi","Tidak Akan Pernah"]
                                p = random.choice(rnd)
                                lang = 'id'
                                tts = gTTS(text=p, lang=lang,slow=False)
                                tts.save("hasil.mp3")
                                client.sendAudio(msg.to,"hasil.mp3")

                            elif (text.lower() == 'cubot') or (text.lower() == ' cubot'):
                                try:
                                    apa = ['iya ada apa kak ?', 'ada yang bisa cubot bantu ?']
                                    hasil = random.choice(apa)
                                    client.sendText(msg.to, str(hasil))
                                except Exception as e:
                                    client.sendText(receiver, str(e))
                            
                            elif ('terimakasih cubot' in msg.text.lower()) or (' terimakasih cubot' in msg.text.lower()) or ('makasih cubot ' in msg.text.lower()) or (' makasih cubot' in msg.text.lower()):
                                try:
                                    tm = ['Sama sama kak', 'Terimakasih doang ? Gift tikel dong','Douitashimashite senpai ^_^']
                                    rs = random.choice(tm)
                                    client.sendText(msg.to, str(rs))
                                except Exception as e:
                                    client.sendText(receiver, str(e))

                            elif (' cubot bisa apa ' in msg.text.lower()) or (' cubot bisa apa' in msg.text.lower()) or ('cubot bisa apa' in msg.text.lower()) or ('cubot bisa apa ' in msg.text.lower()):
                                client.sendMessage(msg.to,bisaApa)

                            elif (" reinvite " in msg.text.lower()) or ("reinvite" in msg.text.lower()):
                                ginfo = client.getGroup(msg.to)
                                for target in korban:
                                    try:
                                        client.findAndAddContactsByMid(target)
                                        client.inviteIntoGroup(msg.to,[target])
                                        client.sendText(msg.to, "Invite SUCCESS..")
                                        del korban[:]
                                        break
                                    except:
                                        client.sendText(msg.to, 'Contact error')
                                        break
                                    
                            
                            elif "korban" in msg.text.lower():
                                if korban.__len__() > 0 :
                                    for i in korban:
                                        client.sendMessage(msg.to, None, contentMetadata={'mid': i}, contentType=13)
                                else :
                                    client.sendMessage(msg.to,"Belom ada yang ke kick")

                            elif (" kick " in msg.text.lower()) or ("kick " in msg.text.lower()):
                                
                                person = eval(msg.contentMetadata['MENTION'])
                                u = person["MENTIONEES"][0]["M"] 
                                if 'MENTION' in msg.contentMetadata.keys()!= None:
                                    if admin == u:
                                        client.sendMessage(msg.to,"Maaf aku gabisa ngekick dia.. ")
                                    else :
                                        names = re.findall(r'@(\w+)', msg.text)
                                        mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                                        mentionees = mention['MENTIONEES']
                                        client.sendMessage(msg.to, "Maaf ya kak , Aku Terpaksa..")
                                        for mention in mentionees:
                                            client.kickoutFromGroup(msg.to,[mention['M']])
                                        korban.append(u)
                                        print (korban)
                            
                            elif ('anjing' in msg.text.lower()) or (' anjing' in msg.text.lower()) or ('anjing ' in msg.text.lower()) or (' anjing ' in msg.text.lower()):
                                contact = client.getContact(sender)
                                a = client.getContact(sender).mid
                                cName = contact.displayName
                                balas = ["Kamu telah berkata kasar " +
                                         cName + "\nAku Kick Kamu! Sorry, Byee!!!"]
                                ret_ = random.choice(balas)
                                name = re.findall(r'@(\w+)', msg.text)
                                client.sendText(msg.to, ret_)
                                client.kickoutFromGroup(msg.to, [sender])
                                korban.append(a)

                            elif('bangsat' in msg.text.lower()) or (' bangsat' in msg.text.lower()) or ('bangsat ' in msg.text.lower()) or (' bangsat ' in msg.text.lower()):
                                contact = client.getContact(sender)
                                a = client.getContact(sender).mid
                                cName = contact.displayName
                                balas = ["Kamu telah berkata kasar " +
                                         cName + "\nAku Kick Kamu! Sorry, Byee!!!"]
                                ret_ = random.choice(balas)
                                name = re.findall(r'@(\w+)', msg.text)
                                client.sendText(msg.to, ret_)
                                client.kickoutFromGroup(msg.to, [sender])
                                korban.append(a)

                            elif('tai' in msg.text.lower()) or (' tai' in msg.text.lower()) or ('tai ' in msg.text.lower()) or (' tai ' in msg.text.lower()):
                                contact = client.getContact(sender)
                                a = client.getContact(sender).mid
                                cName = contact.displayName
                                balas = ["Kamu telah berkata kasar " +
                                         cName + "\nAku Kick Kamu! Sorry, Byee!!!"]
                                ret_ = random.choice(balas)
                                name = re.findall(r'@(\w+)', msg.text)
                                client.sendText(msg.to, ret_)
                                client.kickoutFromGroup(msg.to, [sender])
                                korban.append(a)

                            elif('kimak' in msg.text.lower()) or (' kimak' in msg.text.lower()) or ('kimak ' in msg.text.lower()) or (' kimak ' in msg.text.lower()):
                                contact = client.getContact(sender)
                                a = client.getContact(sender).mid
                                cName = contact.displayName
                                balas = ["Kamu telah berkata kasar " +
                                         cName + "\nAku Kick Kamu! Sorry, Byee!!!"]
                                ret_ = random.choice(balas)
                                name = re.findall(r'@(\w+)', msg.text)
                                client.sendText(msg.to, ret_)
                                client.kickoutFromGroup(msg.to, [sender])
                                korban.append(a)

                            elif(' bangcat ' in msg.text.lower()) or (' tolol' in msg.text.lower()) or ('tolol ' in msg.text.lower()) or (' tolol ' in msg.text.lower()) or (' bangcat' in msg.text.lower()) or ('bangcat ' in msg.text.lower()) :
                                contact = client.getContact(sender)
                                a = client.getContact(sender).mid
                                cName = contact.displayName
                                balas = ["Kamu telah berkata kasar " +
                                         cName + "\nAku Kick Kamu! Sorry, Byee!!!"]
                                ret_ = random.choice(balas)
                                name = re.findall(r'@(\w+)', msg.text)
                                client.sendText(msg.to, ret_)
                                client.kickoutFromGroup(msg.to, [sender])
                                korban.append(a)
                                
                                

                            # elif 'MENTION' in msg.contentMetadata.keys() != None:
                            #     if wait["kickMention"] == True:
                            #         contact = client.getContact(msg.from_)
                            #         cName = contact.displayName
                            #         balas = ["Aku Bilang Jangan Ngetag Lagi " + cName + "\nAku Kick Kamu! Sorry, Byee!!!"]
                            #         ret_ = random.choice(balas)                     
                            #         name = re.findall(r'@(\w+)', msg.text)
                            #         mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                            #         mentionees = mention['MENTIONEES']
                            #         for mention in mentionees:
                            #             if mention['M'] in Bots:
                            #                     client.sendText(msg.to,ret_)
                            #                     client.kickoutFromGroup(msg.to,[msg.from_])
                            #                     break

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

                            elif ("  cek sider" in msg.text.lower()) or (" cek sider " in msg.text.lower()) or ("cek sider" in msg.text.lower()):
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
                                pref=['eh ada','hai kak','aloo..','nah']
                                client.sendText(op.param1, str(random.choice(pref))+' '+Name)
                        else:
                            pass
                    else:
                        pass
                except:
                    pass

            else:
                pass
            
            

        except Exception as error:
            logError(error)
            
def run():
    	while True:
            ops = poll.singleTrace(count=50)
            if ops != None:
                for op in ops:
                    try:
                        bot(op)
                    except Exception as error:
                        logError(error)
                    poll.setRevision(op.revision)

if __name__ == "__main__":
	run()
