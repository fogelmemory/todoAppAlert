from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
from apscheduler.schedulers.background import BackgroundScheduler

from flaskext.mysql import MySQL
import urllib.request
import time
from datetime import datetime

import requests
app = Flask(__name__)


CORS(app)
mysql = MySQL()




app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'todo'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)


@app.route("/", methods=['GET', 'POST'])
def index():
     if request.form:
            data = request.form
            conn = mysql.get_db()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO tasks (task_name, task_content, date1 , status) VALUES (%s, %s, %s ,%s)", (data['name'], data['content'],data['date1'],'0'))
            conn.commit()
            cursor.close()


      
     return render_template('index.html')


@app.route('/api/tasks')
def tasks():
    cursor = mysql.connect().cursor()
    cursor.execute("SELECT * FROM tasks")
    data = cursor.fetchall()
    users = []
    for row in data:
        users.append({"id": row[0], "name": row[1], "content":row[2],"date":row[3],"status":row[4]})
    return jsonify(users)

@app.route('/api/delete/tasks/<id>')
def deleteTasks(id):
    conn = mysql.get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id ="+str(id))
    conn.commit()
    cursor.close()
    response = jsonify({'message': 'Task deleted successfully'})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response



@app.route('/api/update/tasks/<id>/<color>')
def updateTasks(id,color):
    conn = mysql.connect()
    cursor = conn.cursor()
    
    if color =="yellow": 
      cursor.execute("UPDATE tasks set status = 0 WHERE id ="+str(id))
    else:
         cursor.execute("UPDATE tasks set status = 1 WHERE id ="+str(id))
    conn.commit()

    # Close the cursor and connection
    cursor.close()
    conn.close()

    response = jsonify({'message': 'Task updated successfully'})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

  
if __name__ == '__main__':
    app.run(debug=True)
