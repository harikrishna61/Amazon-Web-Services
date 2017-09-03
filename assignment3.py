""" Name: Bathala, Harikrishna
    ID: 1001415489
"""""
import boto3
from flask import Flask, render_template,request

conn = boto3.resource('s3',aws_access_key_id = "",

                    aws_secret_access_key = "")

app=Flask(__name__)

@app.route('/',methods=['POST','GET'])
def start():
    return render_template("index.html")
@app.route("/upload", methods=["POST","GET"])
def upload():
    type=request.form['ftype']
    f=request.files['file']
    mdat=request.form['md']
    fnam=f.filename
    fname_list=fnam.split('.')

    if type=='txt' and fname_list[1]=='txt':
        filecontents=f.stream.read()
        conn.Object('bucktxt', f.filename).put(Body=filecontents,Metadata={'dat':"%s"%mdat})
        return render_template("index.html",msg="File uploaded successfully")

    elif type=='others':
        filecontents = f.stream.read()
        conn.Object('buckothers', f.filename).put(Body=filecontents,Metadata={'dat':"%s"%mdat})
        return render_template("index.html",msg = "File uploaded successfully")


    else:

        return render_template("index.html",msg="Type Mismatch")

@app.route("/downloadfile", methods=["POST","GET"])
def download():
    BUCKET_NAME=request.form['bucketname']
    KEY =request.form['downloadingfile']
    bucket=conn.Bucket(BUCKET_NAME)
    bucket.download_file(KEY,KEY)
    return render_template("index.html")

@app.route("/delete",methods=["POST","GET"])
def deletefiles():
    BUCKET_NAME = request.form['bname']
    KEY = request.form['fname']
    conn.Object(BUCKET_NAME,KEY).delete()
    return render_template("index.html")
@app.route('/listfiles',methods=["POST","GET"])
def listfiles():
    BUCKET_NAME = request.form['buckname']
    fileslist=[]
    for bucket in conn.buckets.all():
        if  bucket.name==BUCKET_NAME :
            for k in bucket.objects.all():
                fileslist.append(k.key)
                fileslist.append(k.last_modified)
    return render_template("index.html",fileslist=fileslist)


if __name__=='__main__':
    # app.run(host='0.0.0.0', port=int(8080), threaded=True, debug=True)
    app.run(debug=True)



