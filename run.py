#import
from flask import Flask,render_template,request,redirect,url_for
import pymysql

#connect to DB
app = Flask(__name__)
conn = pymysql.connect('localhost','root','','memberdb')
conn1 = pymysql.connect('localhost','root','','fooddb')

#Homepage
@app.route("/")
def showpage():
    with conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM member")
        rows = cur.fetchall()
    return render_template('index.html',datas=rows)

#Delete data
@app.route("/delete/<string:id_data>",methods=['GET'])
def delete(id_data):
    with conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM member WHERE id=%s",(id_data))
        conn.commit()
    return redirect(url_for('showpage'))

#Update data
@app.route("/update",methods=['POST'])
def update():
    if request.method=="POST":
        id_update = request.form['id']
        fname = request.form['fname']
        lname = request.form['lname']
        phone = request.form['phone']
        with conn.cursor() as cursor:
            sql = "UPDATE member SET fname=%s,lname=%s,phone=%s WHERE id=%s"
            cursor.execute(sql,(fname,lname,phone,id_update))
            conn.commit()
        return redirect(url_for('showpage'))

#add data member page
@app.route("/member")
def addmember():
    return render_template('add_member.html',)

#Insert data
@app.route("/insert",methods=['POST'])
def insert():
    if request.method=="POST":
        fname = request.form['fname']
        lname = request.form['lname']
        phone = request.form['phone']
        with conn.cursor() as cursor:
            sql = "INSERT INTO `member` (`fname`,`lname`,`phone`) values(%s,%s,%s)"
            cursor.execute(sql,(fname,lname,phone))
            conn.commit()
        return redirect(url_for('showpage'))    

#Cal
@app.route("/cal")
def showdata():
    with conn1:
        cur = conn1.cursor()
        cur.execute("SELECT f.food_id, f.food_name,n1.ingredients_name,n2.ingredients_name,n3.ingredients_name FROM foods f INNER JOIN nutrients n1 ON f.ingredients_p = n1.ingredients_id INNER JOIN nutrients n2 ON f.ingredients_c = n2.ingredients_id INNER JOIN nutrients n3 ON f.ingredients_f = n3.ingredients_id")
        rows = cur.fetchall()
    return render_template('cal.html',data=rows)

#debug code
if __name__ == "__main__":
    app.run(debug=True)