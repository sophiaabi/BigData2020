from flask import Flask, render_template, url_for
from flask_mysqldb import MySQL
import json

app = Flask(__name__)

app.config['MYSQL_USER'] = 'sql3334934'
app.config['MYSQL_PASSWORD'] = 'jkBKdZYJFs'
app.config['MYSQL_HOST'] = 'sql3.freemysqlhosting.net'
app.config['MYSQL_DB'] = 'sql3334934'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)


@app.route('/')
def index():
    cur = mysql.connection.cursor()

    # SQL For Candidates Table
    #cur.execute('''CREATE TABLE Candidates(id INTEGER, name VARCHAR(45), Total INTEGER, Positive INTEGER, Negative INTEGER) ''')
    #cur.execute('''INSERT INTO Candidates VALUES (1, 'Trump', 0, 0, 0)''')
    #cur.execute('''INSERT INTO Candidates VALUES (2, 'Biden', 0, 0, 0)''')

    # cur.execute('''CREATE TABLE States(State_id VARCHAR(45), Trump_Total INTEGER, Trump_Positive INTEGER, Trump_Negative INTEGER, Biden_Total INTEGER, Biden_Positive INTEGER, Biden_Negative INTEGER) ''')
    # cur.execute('''INSERT INTO States VALUES ('AL', 0, 0, 0, 0, 0, 0)''')
    # cur.execute('''INSERT INTO States VALUES ('AK', 0, 0, 0, 0, 0, 0)''')
    # cur.execute('''INSERT INTO States VALUES ('AZ', 0, 0, 0, 0, 0, 0)''')
    # cur.execute('''INSERT INTO States VALUES ('AR', 0, 0, 0, 0, 0, 0)''')
    # cur.execute('''INSERT INTO States VALUES ('CA', 0, 0, 0, 0, 0, 0)''')
    # cur.execute('''INSERT INTO States VALUES ('CO', 0, 0, 0, 0, 0, 0)''')
    # cur.execute('''INSERT INTO States VALUES ('CT', 0, 0, 0, 0, 0, 0)''')
    # cur.execute('''INSERT INTO States VALUES ('DE', 0, 0, 0, 0, 0, 0)''')
    # cur.execute('''INSERT INTO States VALUES ('FL', 0, 0, 0, 0, 0, 0)''')
    # cur.execute('''INSERT INTO States VALUES ('GA', 0, 0, 0, 0, 0, 0)''')
    # cur.execute('''INSERT INTO States VALUES ('HI', 0, 0, 0, 0, 0, 0)''')
    # cur.execute('''INSERT INTO States VALUES ('ID', 0, 0, 0, 0, 0, 0)''')
    # cur.execute('''INSERT INTO States VALUES ('IL', 0, 0, 0, 0, 0, 0)''')
    # cur.execute('''INSERT INTO States VALUES ('IN', 0, 0, 0, 0, 0, 0)''')
    # cur.execute('''INSERT INTO States VALUES ('IA', 0, 0, 0, 0, 0, 0)''')
    # cur.execute('''INSERT INTO States VALUES ('KS', 0, 0, 0, 0, 0, 0)''')
    # cur.execute('''INSERT INTO States VALUES ('KY', 0, 0, 0, 0, 0, 0)''')
    # cur.execute('''INSERT INTO States VALUES ('LA', 0, 0, 0, 0, 0, 0)''')
    # cur.execute('''INSERT INTO States VALUES ('ME', 0, 0, 0, 0, 0, 0)''')
    # cur.execute('''INSERT INTO States VALUES ('MD', 0, 0, 0, 0, 0, 0)''')
    # cur.execute('''INSERT INTO States VALUES ('MA', 0, 0, 0, 0, 0, 0)''')
    # cur.execute('''INSERT INTO States VALUES ('MI', 0, 0, 0, 0, 0, 0)''')
    # cur.execute('''INSERT INTO States VALUES ('MN', 0, 0, 0, 0, 0, 0)''')
    # cur.execute('''INSERT INTO States VALUES ('MS', 0, 0, 0, 0, 0, 0)''')
    # cur.execute('''INSERT INTO States VALUES ('MO', 0, 0, 0, 0, 0, 0)''')
    # cur.execute('''INSERT INTO States VALUES ('MT', 0, 0, 0, 0, 0, 0)''')
    # cur.execute('''INSERT INTO States VALUES ('NE', 0, 0, 0, 0, 0, 0)''')
    # cur.execute('''INSERT INTO States VALUES ('NV', 0, 0, 0, 0, 0, 0)''')
    # cur.execute('''INSERT INTO States VALUES ('NH', 0, 0, 0, 0, 0, 0)''')
    # cur.execute('''INSERT INTO States VALUES ('NJ', 0, 0, 0, 0, 0, 0)''')
    # cur.execute('''INSERT INTO States VALUES ('NM', 0, 0, 0, 0, 0, 0)''')
    # cur.execute('''INSERT INTO States VALUES ('NY', 0, 0, 0, 0, 0, 0)''')
    # cur.execute('''INSERT INTO States VALUES ('NC', 0, 0, 0, 0, 0, 0)''')
    # cur.execute('''INSERT INTO States VALUES ('ND', 0, 0, 0, 0, 0, 0)''')
    # cur.execute('''INSERT INTO States VALUES ('OH', 0, 0, 0, 0, 0, 0)''')
    # cur.execute('''INSERT INTO States VALUES ('OK', 0, 0, 0, 0, 0, 0)''')
    # cur.execute('''INSERT INTO States VALUES ('OR', 0, 0, 0, 0, 0, 0)''')
    # cur.execute('''INSERT INTO States VALUES ('PA', 0, 0, 0, 0, 0, 0)''')
    # cur.execute('''INSERT INTO States VALUES ('RI', 0, 0, 0, 0, 0, 0)''')
    # cur.execute('''INSERT INTO States VALUES ('SC', 0, 0, 0, 0, 0, 0)''')
    # cur.execute('''INSERT INTO States VALUES ('SD', 0, 0, 0, 0, 0, 0)''')
    # cur.execute('''INSERT INTO States VALUES ('TN', 0, 0, 0, 0, 0, 0)''')
    # cur.execute('''INSERT INTO States VALUES ('TX', 0, 0, 0, 0, 0, 0)''')
    # cur.execute('''INSERT INTO States VALUES ('UT', 0, 0, 0, 0, 0, 0)''')
    # cur.execute('''INSERT INTO States VALUES ('VT', 0, 0, 0, 0, 0, 0)''')
    # cur.execute('''INSERT INTO States VALUES ('VA', 0, 0, 0, 0, 0, 0)''')
    # cur.execute('''INSERT INTO States VALUES ('WA', 0, 0, 0, 0, 0, 0)''')
    # cur.execute('''INSERT INTO States VALUES ('WV', 0, 0, 0, 0, 0, 0)''')
    # cur.execute('''INSERT INTO States VALUES ('WI', 0, 0, 0, 0, 0, 0)''')
    # cur.execute('''INSERT INTO States VALUES ('WY', 0, 0, 0, 0, 0, 0)''')

    # cur.execute('''DROP TABLE States''')

    # mysql.connection.commit()


    cur.execute('''SELECT * FROM Candidates''')
    results = cur.fetchall()

    cur.execute('''SELECT * FROM States''')
    states = cur.fetchall()
    # print(states)
    return render_template('index.html', Trump_Positive = str(results[0]['Positive']), Trump_Negative = str(results[0]['Negative']),
                            Biden_Positive = str(results[1]['Positive']), Biden_Negative = str(results[1]['Negative']), states=json.dumps(states))

if __name__ == "__main__":
    app.run()
