""" Name: Bathala, Harikrishna
    ID: 1001415489
"""""
from flask import Flask, render_template, request
import pymysql.cursors
import hashlib
import datetime
import  random
# from pymemcache.client.hash import HashClient
import memcache
memche=memcache.Client(['sunday.84kn8l.0001.usw2.cache.amazonaws.com:11211'], debug=0)

memche.flush_all()
conn = pymysql.connect(host='haridb.cwwvovyolyty.us-west-2.rds.amazonaws.com', user='hari', password='hari1234',
                       db='nationalpark', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor, local_infile=1)

cur = conn.cursor()


app = Flask(__name__)

@app.route('/',methods=["GET","POST"])
def startmemcache():
    return render_template("cache_mem.html")


@app.route('/rdstime',methods=["GET","POST"])
def rds():
    iter_rds=request.form['iterno']
    sql_stname=request.form['statename']
    sql_leg=request.form['opera']
    sql_idval=request.form['idval']

    int_iter_rds=int(iter_rds)
    int_sql_idval=int(sql_idval)


    before_query_time = datetime.datetime.utcnow()
    # print(before_query_time)
    for id in range(0,int_iter_rds):
        # print("in loop:"+str(id))
        idrds=random.randint(129520,129526)

        sql="SELECT NAME FROM nationalpark.qui3table where STATE='%s' AND IPEDSID %s '%s';"%(sql_stname,sql_leg,int_sql_idval)
        cur.execute(sql)
        for row_rds in cur:
            data_rds = row_rds['NAME']
            # print("from rds"+data_rds)
    after_query_time=datetime.datetime.utcnow()
    differrnce=str(after_query_time-before_query_time)
    # print("diff"+differrnce)


    return render_template("cache_mem.html",differrnce=differrnce)


@app.route('/memcachetime',methods=["GET","POST"])
def memtime():
    iterations_memcache=request.form['iterations']
    int_iterationsmem=int(iterations_memcache)

    mem_stname = request.form['memstatename']
    mem_leg = request.form['memopera']
    mem_idval = request.form['memidval']

    int_mem_idval=int(mem_idval)


    before_query_time_memcache = datetime.datetime.utcnow()
    # print(before_query_time_memcache)

    for i in range(1,int_iterationsmem):

        idmem = random.randint(129520, 129526)

        query="SELECT NAME FROM nationalpark.qui3table where STATE='%s' AND IPEDSID %s '%s';"%(mem_stname,mem_leg,int_mem_idval)
        encoded_query = query.encode('utf-8')
        hash_query = hashlib.md5(encoded_query).hexdigest()

        query_in_cache=" "

        if  memche.get(hash_query) is not None:
            quer_result=memche.get(hash_query)
            # print(quer_result)

        else:
            cur.execute(query)
            name=" "
            for row in cur:
                name = row['NAME']
                print("from db"+name)
            memche.set(hash_query,name)

    after_query_time_memcacahe = datetime.datetime.utcnow()
    differrnce1 = str(after_query_time_memcacahe - before_query_time_memcache)

    return render_template("cache_mem.html",differrnce1=differrnce1)


@app.route('/results',methods=["GET","POST"])
def results():
    res_stname = request.form['resstatename']
    res_leg = request.form['resopera']
    res_idval = request.form['residval']

    int_res_idval = int(res_idval)
    query = "SELECT * FROM nationalpark.qui3table where STATE='%s' AND IPEDSID %s '%s' LIMIT 5;" % (res_stname, res_leg, int_res_idval)
    cur.execute(query)


    data=[]
    for row in cur :
        data.append(row['NAME']+" "+row['IPEDSID']+" ")

    return render_template("cache_mem.html", data=data)
if __name__ == '__main__':
    app.run(debug=True)
