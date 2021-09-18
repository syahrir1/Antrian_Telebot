import telebot
import requests
from datetime import date

TOKEN = "1933114045:AAHoOrHhzmLmvb27yD1yPgaxfgp1z9yjJp4"
bot = telebot.TeleBot(token=TOKEN)
antrian = 1
jumlahNotif = ''
today = date.today()
data = []
count = 0

@bot.message_handler(commands = ['start'])
def at_converter(message):
    insta_link = "Selamat datang, "+str(message.chat.first_name)+". Anda menggunakan chatbot antrian BPJS. Untuk bantuan klik: /help"
    bot.reply_to(message, insta_link)

@bot.message_handler(commands = ['help'])
def at_converter(message):
    insta_link = "/start untuk memulai bot\n/help info bantuan ini\n/daftar untuk registrasi\n/notifikasi untuk mendapatkan notifikasi jumlah antrian sebelumnya"
    bot.reply_to(message, insta_link)
    
@bot.message_handler(commands = ['daftar'])
def at_converter(message):
    global antrian
    today = date.today()
    dateNow = today.strftime("%Y-%m-%d")
    datatable = requests.get('http://localhost/bpjshackathon/get_all_data.php').json()

    checkID = [x for x in datatable if x['tanggal'] == dateNow and x['status'] == '0' and x['chat_id'] == str(message.chat.id)]
    print(checkID)
    if checkID:
        insta_link = 'Anda Sudah Melakukan pendaftaran antrian hari ini.\n\nNomor Antrian Anda: '+checkID[0]['antrian']
        bot.reply_to(message, insta_link)
    
    else:
        if dateNow ==  datatable[len(datatable)-1]['tanggal']: 
            antrian = int(datatable[len(datatable)-1]['antrian']) + 1
            datatable = requests.post('http://localhost/bpjshackathon/input_nama.php?&chat_id='+str(message.chat.id)+'&antrian='+str(antrian)+'&datetime='+dateNow+'&notifikasi=3&status=0').json()
       
        else:
            datatable = requests.post('http://localhost/bpjshackathon/input_nama.php?&chat_id='+str(message.chat.id)+'&antrian=1&datetime='+dateNow+'&notifikasi=3&status=0').json()
        
        totalAntrianHariIni = len([x for x in datatable if x['tanggal'] == dateNow and x['status'] == '0'])
        insta_link = str(message.chat.first_name)+', Selamat Anda Telah Terdaftar dengan nomor Antrian: '+str(antrian) + '\n\nTotal antrian hari ini: '+str(totalAntrianHariIni)
        bot.reply_to(message, insta_link)
       
        if totalAntrianHariIni == 1:
            insta_link = 'Silahkan maju ke Cutomer Service'
            bot.reply_to(message, insta_link)
       
        if totalAntrianHariIni == 2:
            insta_link = '1 Antrian lagi sebelum Anda'
            bot.reply_to(message, insta_link)
        
        if totalAntrianHariIni == 3:
            insta_link = '2 Antrian lagi sebelum Anda'
            bot.reply_to(message, insta_link)

@bot.message_handler(commands = ['notifikasi'])
def at_converter(message):
    dateNow = today.strftime("%Y-%m-%d")
    global jumlahNotif
   
    if message.text == '/notifikasi':
        insta_link = 'Untuk mengatur Notifikasi, Silahkan masukkan jumlah Notifikasi yang anda inginkan\n\n(Cth: /notifikasi <spasi> 5)'
        bot.reply_to(message, insta_link)
   
    else:
        datatable = requests.get('http://localhost/bpjshackathon/get_all_data.php').json()
        buff = [x for x in datatable if x['tanggal'] == dateNow and x['status'] == '0' and x['chat_id'] == str(message.chat.id)]
        
        if buff:
            jumlahNotif = message.text.split()
            datatable = requests.post('http://localhost/bpjshackathon/update_notifikasi.php?notifikasi='+jumlahNotif[1]+'&antrian='+buff[0]['antrian'])
            insta_link = 'Berhasil! Notifikasi Antrian telah diubah.'
            bot.reply_to(message, insta_link)

        else:
            insta_link = 'Mohon Maaf Anda Belum Melakukan Pendaftaran Antrian! Untuk bantuan ketik: /help.'
            bot.reply_to(message, insta_link)



@bot.message_handler(commands = ['admin','Next', 'Prev'])
def at_converter(message):
    global count
    today = date.today()
    dateNow = today.strftime("%Y-%m-%d")

    if message.chat.id == 1647430568:
        datatable = requests.get('http://localhost/bpjshackathon/get_all_data.php').json()
        totalAntrianHariIni = len([x for x in datatable if x['tanggal'] == dateNow and x['status'] == '0'])
        
        if message.text == '/admin':
            for x in datatable:
                if x['status'] == '0' and x['tanggal'] == dateNow:
                    data.append(x)

            try:
                count = int(data[0]['antrian'])
                insta_link = 'Mode Admin\nNomor Antrian: '+ str(count) +'\n\n1. /Next\n\n2. /Prev'
                bot.reply_to(message, insta_link)
                
            except:
                insta_link = 'Tidak Ada Antrian!'
                bot.reply_to(message, insta_link)

            data.clear()
            
        if message.text == '/Next':
            if count < totalAntrianHariIni:
                requests.post('http://localhost/bpjshackathon/update_antrian.php?status=1&antrian='+str(count))
                count = count + 1
                insta_link = 'Nomor Antrian: '+ str(count) +'\n\n1. /Next\n\n2. /Prev'
                bot.reply_to(message, insta_link)
            else:
                insta_link = 'Tidak Ada Antrian!\n\n1. /Next\n\n2. /Prev'
                bot.reply_to(message, insta_link)
        
        if message.text == '/Prev':
            if count > 1:
                count = count - 1
                requests.post('http://localhost/bpjshackathon/update_antrian.php?status=0&antrian='+str(count))
                insta_link = 'Nomor Antrian: '+ str(count) +'\n\n1. /Next\n\n2. /Prev'
                bot.reply_to(message, insta_link)
            else:
                insta_link = 'Nomor Antrian: '+ str(count) +'\n\n1. /Next\n\n2. /Prev'
                bot.reply_to(message, insta_link)


        
bot.polling(none_stop=True)