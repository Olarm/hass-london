import subprocess
import telegram
import time
import yaml


with open("/config/secrets.yaml") as f:
    file = yaml.full_load(f)
api_key = file["telegram_api_key"]
user_1 = file["chat_id_1"]
user_2 = file["chat_id_2"]
pi = file["tripoli"]

take_picture = f"ssh -i /config/.ssh/tripoli {pi} raspistill -o test1.jpg"
#flip_picture = f"ssh -i /config/.ssh/tripoli {tripoli} mogrify -rotate -180 test1.jpg"
copy_picture = f"scp -i /config/.ssh/tripoli {pi}:test1.jpg /config/include/photos/"
delete_picture = f"ssh -i /config/.ssh/tripoli {pi} rm test1.jpg"

p1 = subprocess.Popen(take_picture.split(), stdout=subprocess.PIPE)
p1.wait()
time.sleep(1)
#p2 = subprocess.Popen(flip_picture.split(), stdout=subprocess.PIPE)
#p2.wait()
p3 = subprocess.Popen(copy_picture.split(), stdout=subprocess.PIPE)
p3.wait()
p4 = subprocess.Popen(delete_picture.split(), stdout=subprocess.PIPE)
p4.wait()

bot = telegram.Bot(token=api_key)
bot.send_message(chat_id=user_1, text="Sending photo.")
bot.send_photo(chat_id=user_1, timeout=100, photo=open('/config/include/photos/test1.jpg', 'rb'))
bot.send_photo(chat_id=user_2, timeout=100, photo=open('/config/include/photos/test1.jpg', 'rb'))
