import time
import requests
import paho.mqtt.client as mqtt
from datetime import date
print('RUNNING REMOTE')
client = mqtt.Client()
client.connect('broker.hivemq.com', 1883)
data = []
count = 0

def on_connect(client, userdata, flags, rc):
    print("Connected to a broker!")
    client.subscribe("testmajenesub")

def on_message(client, userdata, message):
    dataMqtt = message.payload.decode()
    print(dataMqtt)
    global count
    today = date.today()
    dateNow = today.strftime("%Y-%m-%d")
    datatable = requests.get('http://localhost/bpjshackathon/get_all_data.php').json()
    totalAntrianHariIni = len([x for x in datatable if x['tanggal'] == dateNow and x['status'] == '0'])
    client.publish("bpjshackathongreenscopetotal", 'Total Antrian: '+str(totalAntrianHariIni)+' Orang')


    if dataMqtt == 'admin':
        for x in datatable:
            if x['status'] == '0' and x['tanggal'] == dateNow:
                data.append(x)
        try:
            count = int(data[0]['antrian'])
            client.publish("bpjshackathongreenscope", str(count))
            print(count)
            
  
        except:
            print('tidak ada antrian')
            client.publish("bpjshackathongreenscopetotal", 'Tidak Ada Antrian')

        data.clear()
    
    if dataMqtt == 'next':
        print('woiiii')
        if count <= totalAntrianHariIni:
            requests.post('http://localhost/bpjshackathon/update_antrian.php?status=1&antrian='+str(count))
            count = count + 1
            print (count)
        client.publish("bpjshackathongreenscope", str(count))

while True:
    client.on_connect = on_connect
    client.on_message = on_message
    client.loop_forever()

# while(1):

#     today = date.today()
#     dateNow = today.strftime("%Y-%m-%d")

#     if message.chat.id == 1647430568:
#         datatable = requests.get('http://localhost/bpjshackathon/get_all_data.php').json()
#         totalAntrianHariIni = len([x for x in datatable if x['tanggal'] == dateNow and x['status'] == '0'])
        
#         if message.text == '/admin':
#             for x in datatable:
#                 if x['status'] == '0' and x['tanggal'] == dateNow:
#                     data.append(x)

#             try:
#                 count = int(data[0]['antrian'])
#                 insta_link = 'Mode Admin\nNomor Antrian: '+ str(count) +'\n\n1. /Next\n\n2. /Prev'
#                 bot.reply_to(message, insta_link)
                
#             except:
#                 insta_link = 'Tidak Ada Antrian!'
#                 bot.reply_to(message, insta_link)

#             data.clear()
            
#         if message.text == '/Next':
#             if count < totalAntrianHariIni:
#                 requests.post('http://localhost/bpjshackathon/update_antrian.php?status=1&antrian='+str(count))
#                 count = count + 1
#                 insta_link = 'Nomor Antrian: '+ str(count) +'\n\n1. /Next\n\n2. /Prev'
#                 bot.reply_to(message, insta_link)
#             else:
#                 insta_link = 'Tidak Ada Antrian!\n\n1. /Next\n\n2. /Prev'
#                 bot.reply_to(message, insta_link)
        
#         if message.text == '/Prev':
#             if count > 1:
#                 count = count - 1
#                 requests.post('http://localhost/bpjshackathon/update_antrian.php?status=0&antrian='+str(count))
#                 insta_link = 'Nomor Antrian: '+ str(count) +'\n\n1. /Next\n\n2. /Prev'
#                 bot.reply_to(message, insta_link)
#             else:
#                 insta_link = 'Nomor Antrian: '+ str(count) +'\n\n1. /Next\n\n2. /Prev'
#                 bot.reply_to(message, insta_link)