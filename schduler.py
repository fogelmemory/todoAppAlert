from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import mysql.connector
import time

mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="todo"
)
def telegram():
    mycursor = mydb.cursor(buffered=True)
    now = datetime.now()
    print("now =", now)
    dt_string = now.strftime("%m-%d %H:%M")
    mycursor.execute("SELECT * FROM tasks")
    data = mycursor.fetchall()

    for row in data:

        x = row[3].split("T")
        x[0] = x[0][5:]
        time1 = x[0]+" "+x[1]
        print(time1)
        print(dt_string)
        if time1 == dt_string:
              TOKEN = "6198018759:AAFp7ihi91iZURC15QGn4cTB81qkXFYd62k"
              chat_id = "1983435776"
              message = row[1]+" "+row[2]
              url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={message}"
              print(requests.get(url).json())
              time.sleep(60)


sched = BackgroundScheduler(daemon=True)
sched.add_job(telegram,'interval',minutes=0.1)
sched.start()
