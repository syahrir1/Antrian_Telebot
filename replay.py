import requests
import time
from datetime import date
print('RUNNING REPLAY')
today = date.today()
token = '1933114045:AAHoOrHhzmLmvb27yD1yPgaxfgp1z9yjJp4'
data = [] 
lastFirstData = []

def send_msg(text,id):
    url_req = 'http://api.telegram.org/bot'+token+'/sendMessage?chat_id='+id+'&text='+text
    result = requests.get(url_req).text
    # print(result)

while(1):
    today = date.today()
    dateNow = today.strftime("%Y-%m-%d")
    datatable = requests.get('http://localhost/bpjshackathon/get_all_data.php').json()
    try:
        for x in datatable:
            if x['status'] == '0' and x['tanggal'] == dateNow:
                data.append(x)

        if data[0] != lastFirstData:
            lastFirstData = data[0]
            antrianNow = int(data[0]['antrian'])
        
            for x in datatable:
                if x['status'] == '0':
                    if int(x['antrian']) - antrianNow < 1:
                        send_msg('Silahkan maju ke Cutomer Service', str(x['chat_id']))
                    elif int(x['antrian']) - antrianNow <= int(x['notifikasi']):
                        send_msg(str(int(x['antrian']) - antrianNow) + ' antrian lagi sebelum Anda',str(x['chat_id']))


        data.clear()
    except:
        print('Tidak ada data')
    time.sleep(1)
