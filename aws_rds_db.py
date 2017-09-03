""" Name: Bathala, Harikrishna
    ID: 1001415489
"""""
from flask import Flask, render_template, request, make_response, g
import pymysql.cursors
import csv
import base64
import io


conn = pymysql.connect(host='haridb.cwwvovyolyty.us-west-2.rds.amazonaws.com', user='hari', password='hari1234',
                       db='nationalpark', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor, local_infile=1)
cur = conn.cursor()

app = Flask(__name__)


@app.route('/', methods=["POST", "GET"])
def startdb():
    return render_template("db.html")


@app.route("/uploadcsv", methods=["POST", "GET"])
def uploadcsv():
    f = request.files['file']
    f.save('/home/ubuntu/flaskapp/quiz.csv')
    fo = open('/home/ubuntu/flaskapp/quiz.csv', "r")
    line = fo.readline()
    print("Read Line: %s" % (line))
    new_line = line.replace(',', ' VARCHAR(20),')
    gen_create = "CREATE TABLE quiz3 (" + new_line + "VARCHAR(20) )"
    print(gen_create)
    cur.execute(gen_create)
    conn.commit()

    insert_query = "LOAD DATA local INFILE '/home/ubuntu/flaskapp/earthquake.csv' INTO TABLE quiz3 FIELDS TERMINATED BY ',' IGNORE 1 LINES ; "

    cur.execute(insert_query)
    conn.commit()

    return render_template("db.html")


@app.route("/entries", methods=["POST", "GET"])
def countentries():
    cur.execute("SELECT count(*) FROM nationalpark.qui3table")
    data=[]
    for row in cur:
        # print(row['time'])
        # required_time = row['time']
        # print(now - required_time)

        data.append(row['count(*)'])
    return render_template("db.html",data=data)

@app.route("/state", methods=["POST", "GET"])
def state():
    stname=request.form['st']
    str_st=str(stname)

    cur.execute("SELECT count(*),STATE FROM nationalpark.qui3table where STATE = '%s' "%str_st )
    statename = cur.fetchall()
    # for row in cur:
    #     # print(row['time'])
    #     # required_time = row['time']
    #     # print(now - required_time)
    #
    #     data.append(row['count(*)'])
    return render_template("db.html", statename=statename)


@app.route("/latt", methods=["POST", "GET"])
def latt():
    lat=request.form['lati']
    long=request.form['longi']
    int_lat=float(lat)
    int_long=float(long)
    maxlat=int_lat+2.0
    maxlong=int_long+2.0
    minlat=int_lat-2.0
    minlong=int_long-2.0
    str_maxlat=str(maxlat)
    str_minlat=str(minlat)
    str_maxlong=str(maxlong)
    str_minlong=str(minlong)
    print("a")

    cur.execute("SELECT NAME FROM nationalpark.qui3table where (LATITUDE < '%s' OR LATITUDE >'%s') AND (LONGITUDE < '%s' OR"
                " LONGITUDE > '%s') " %(str_maxlat,str_minlat,str_maxlong,str_minlong))
    print(str_maxlat)
    univname=cur.fetchall()
    print("b")
    print(univname)
    return render_template("db.html",univname=univname)


@app.route("/delete", methods=["POST","GET"])
def delete():
    delyear=request.form['deleyear']
    int_delyeat=int(delyear)
    sql="UPDATE natlpark1 SET year=2017 where year>%s"%int_delyeat

@app.route("/upload", methods=["POST","GET"])
def uploaddata():
    parkname=request.form['parkname']
    parkstate=request.form['parkstate']
    parkyear=request.form['parkyear']
    parkarea=request.form['parkarea']
    intparkyear=int(parkyear)
    floatparkarea=float(parkarea)
    sql="INSERT INTO natlpark VALUES ('%s','%s','%d','%f')"%(parkname,parkstate,intparkyear,floatparkarea)
    cur.execute(sql)
    conn.commit()
    return render_template("db.html")



@app.route('/display',methods=['GET','POST'])
def displaydata():
    cur.execute("SELECT * FROM natlpark")

    data = cur.fetchall()

    name=data['name']
    print(name)
    print("Database version : %s " % data)

    return render_template("db.html",name=name)

@app.route('/uploadimage',methods=['GET','POST'])
def uploadimage():

    f=request.files['file']
    imid=request.form['imageid']
    int_imgid=int(imid)

    filecontents=f.stream.read()
    file_b64=base64.b64encode(filecontents)
    remo_b=file_b64.decode('UTF-8')
    print(remo_b)
    fnme=f.filename
    type_list=fnme.split('.')

    query="INSERT INTO images VALUES ('%d','%s','%s')"%(int_imgid,remo_b,type_list[1])

    cur.execute(query)
    conn.commit()

    return render_template("db.html")
@app.route('/downloaimage',methods=['GET','POST'])
def downloadimage():
    imgid=request.form['imgid']
    int_imgid=int(imgid)
    cur.execute("SELECT * FROM images where ID=%d;"%int_imgid)
    image=cur.fetchone()
    getimg=image['IMAGE']
    print(getimg)
    en_image=getimg.decode('UTF-8')
    print(en_image)
    act_image=base64.b64decode(en_image)
    print("done")


    ftype=image['filetype']
    print(ftype)
    response = make_response(act_image)
    response.headers["Content-Disposition"] = "attachment; filename=res.%s"%ftype
    print("done")
    return response


if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=int(8080), threaded=True, debug=True)
    app.run(debug=True)

