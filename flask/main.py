from flask import Flask, render_template, redirect,url_for, request, jsonify
import random, datetime,sqlite3,json,csv,pathlib,time
import Adafruit_DHT as dht
#import pandas as pd
#from pandas import ExcelWriter
from flask_bootstrap import Bootstrap
import RPi.GPIO as GPIO
from apscheduler.schedulers.background import BackgroundScheduler
#from openpyxl import load_workbook



app = Flask(__name__, static_url_path='/static')
Bootstrap(app)

conn = sqlite3.connect('Testdb.db', check_same_thread=False)
c = conn.cursor()


channel = 21

GPIO.setmode(GPIO.BCM)
GPIO.setup(channel, GPIO.OUT)
GPIO.setwarnings(False)

def fan_on(pin):
	GPIO.output(pin, GPIO.HIGH)
	
def fan_off(pin):
	GPIO.cleanup()


def create_sqltemp(t, h, d):
    conn = sqlite3.connect('Testdb.db', check_same_thread=False)
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS TempData (Datestamp TEXT, Temperature INTEGER, Humidity INTEGER)')
    c.execute("INSERT INTO TempData (Temperature, Humidity, Datestamp) VALUES  (?, ?, ?)", (t, h, d))
    conn.commit()
    c.close()
    conn.close()
    return



def data_sensor():
    date= datetime.datetime.now()
    datestamp = date.strftime('%Y-%m-%d %m %H:%M:%S')
    h,t = dht.read_retry(dht.DHT11, 4)
    Temp = int(t)
    Hum = int(h)
    return Temp, Hum, datestamp


def time_job():
    Temp, Hum, datestamp = data_sensor()
    create_sqltemp(Temp, Hum, datestamp)


#c.execute("INSERT INTO TempData ")

sched = BackgroundScheduler()
sched.add_job(time_job,'interval',minutes=2)
sched.start()


@app.route('/')
def home():
    Temp, Hum, datestamp=data_sensor()
    if Temp > 26 or Hum > 85:
        fan_on(channel)
    else:
        fan_off(channel)
    return render_template('home.html',Temp=Temp,Hum=Hum)

@app.route('/stock')
def warehouse():

    Temp, Hum, datetime = data_sensor()


    return render_template('stock.html', Temp=Temp, Hum=Hum)

@app.route('/viewstock')
def viewstock():

    c = conn.cursor()
    c.execute("SELECT * FROM Stock")
    data = c.fetchall()

    return render_template('viewstock.html', data=data)


@app.route('/delete/<id>')
def delete(id):
    conn = sqlite3.connect('Testdb.db', check_same_thread=False)
    c = conn.cursor()
    
    date= datetime.datetime.now()
    deletedate = date.strftime('%c')

    c.execute("SELECT * FROM Stock WHERE Id=?",(id,))
    deletedStock = str(c.fetchone()).strip("'' ()")

    labels = ["Id","Block","Added Time","Grain","Type","Weight","Deleted Time"]

    li = list(deletedStock.split(','))
    li.append(deletedate)
    file = pathlib.Path("test.csv")
    if file.exists ():
        with open('test.csv', 'a') as csvfile:
            filewriter = csv.writer(csvfile, delimiter=',',quoting=csv.QUOTE_ALL)
            filewriter.writerow(li)
    else:
        with open('test.csv', 'a') as csvfile:
            filewriter = csv.writer(csvfile, delimiter=',',quoting=csv.QUOTE_ALL)
            filewriter.writerow(labels)
            filewriter.writerow(li)




    #with open("copy.txt", "a") as file:
        #file.write(deletedStock)


    #book = load_workbook('test.xlsx')
    #writer = pd.ExcelWriter('test.xlsx', engine='openpyxl') 
    #writer.book = book
    #writer.sheets = dict((ws.title, ws) for ws in book.worksheets)

    #df.to_excel(writer, "Main" ,columns=["Id","Block","Added Time","Grain","Type","Weight"])

    #writer.save()

    c.execute("DELETE FROM Stock Where Id=?",(id,))
    conn.commit()
    c.close()
    conn.close()
    return redirect(url_for('viewstock'))



@app.route('/process', methods=['POST'])
def process():
    block = request.form['block']
    grain = request.form['grain']
    type = request.form['type']
    weight = request.form['weight']
    dates= datetime.datetime.now()
    datestock = dates.strftime('%c')
    if block and grain and type and weight:
        conn = sqlite3.connect('Testdb.db', check_same_thread=False)
        c = conn.cursor()
        c.execute('CREATE TABLE IF NOT EXISTS Stock (ID INTEGER PRIMARY KEY AUTOINCREMENT, Block TEXT, Date TEXT ,Grain TEXT, Type TEXT, Weight INTEGER)')
        c.execute("INSERT INTO Stock (Block, Date, Grain, Type, Weight) VALUES  (?,?, ?, ?, ?)", (block,datestock,grain, type, weight))
        conn.commit()
        c.close()
        conn.close()
        return render_template('stock.html')
    return jsonify({'error': 'Missing Data!'})


@app.route('/editprocess/<id>')
def editprocess(id):
    conn = sqlite3.connect('Testdb.db', check_same_thread=False)
    c = conn.cursor()
    c.execute("SELECT Block FROM Stock WHERE id=?",(id,))
    b=str(c.fetchone()).strip("(),''")
    c.execute("SELECT Grain FROM Stock WHERE id=?",(id,))
    g=str(c.fetchone()).strip("(),''")
    c.execute("SELECT Type FROM Stock WHERE id=?",(id,))
    t=str(c.fetchone()).strip("(),''")
    c.execute("SELECT Weight FROM Stock WHERE id=?",(id,))
    w=str(c.fetchone()).strip("(),''")
    conn.commit()
    c.close()
    conn.close()
    return render_template('edit.html',b=b,g=g,t=t,w=w,id=id)


@app.route('/edit',methods=['POST'])
def edit():

    id=request.form['id']
    block = request.form['block']
    grain = request.form['grain']
    type = request.form['type']
    weight = request.form['weight']
    dates= datetime.datetime.now()
    datestock = dates.strftime('%c')
    if block and grain and type and weight:
        conn = sqlite3.connect('Testdb.db', check_same_thread=False)
        c = conn.cursor()
        c.execute("UPDATE Stock SET Block = ?, Date = ?, Grain = ?, Type = ?, Weight = ? WHERE Id=?",(block,datestock,grain, type, weight,id))
        conn.commit()
        c.close()
        conn.close()
        return redirect(url_for('viewstock.html'))
    return jsonify({'error': 'Missing Data!'})


@app.route('/history')
def history():
    conn = sqlite3.connect('Testdb.db', check_same_thread=False)

    weeks=['Week1','Week2','Week3','Week4','week5','week6','Week7','Week8','Week9','Week10','week11','week12']
    data1=[24,29,20,19,28,28,24,24,29,20,19,28]
    data2=[40,50,66,48,44,65,64,40,50,66,40,50]


    conn.close()

    
    return render_template('history.html',weeks=json.dumps(weeks),data1=json.dumps(data1),data2=json.dumps(data2))


@app.route('/about')
def about():
    return render_template('about.html')



@app.route('/contact')
def contact():
    return render_template('contactus.html')

if __name__ == '__main__':
    app.run(debug=True)

STATIC_URL = '/static/'
