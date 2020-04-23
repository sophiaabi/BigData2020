from flask import Flask, render_template
from flask_mysqldb import MySQL

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
    #cur.execute('''CREATE TABLE Candidates(id INTEGER, name VARCHAR(45), Total INTEGER, Positive INTEGER, Negative INTEGER) ''')
    #cur.execute('''INSERT INTO Candidates VALUES (1, 'Trump', 0, 0, 0)''')
    #cur.execute('''INSERT INTO Candidates VALUES (2, 'Biden', 0, 0, 0)''')
    #mysql.connection.commit()

    cur.execute('''SELECT * FROM Candidates''')
    results = cur.fetchall()
    print(results)
    return render_template('index.html', Trump_Positive = str(results[0]['Positive']), Trump_Negative = str(results[0]['Negative']),
                            Biden_Positive = str(results[1]['Positive']), Biden_Negative = str(results[1]['Negative']))

if __name__ == "__main__":
    app.run()
