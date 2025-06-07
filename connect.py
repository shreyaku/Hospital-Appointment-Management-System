from flask import Flask, render_template, request, redirect, url_for, session,make_response
from flask_mysqldb import MySQL
from pytz import timezone
from datetime import datetime
from dateutil import parser
import pytz
import json
from json import JSONEncoder
from werkzeug.utils import secure_filename

from flask_cors import CORS


app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'hosapp'
CORS(app) 
 
app.secret_key = 'your secret key'
mysql = MySQL(app)
now_utc = datetime.now(timezone('UTC'))
now_asia = now_utc.astimezone(timezone('Asia/Kolkata'))

@app.route('/adminreg',methods=['GET', 'POST'])
def userreg():
    return render_template('adminregistration.html')

@app.route('/patient',methods=['GET', 'POST'])
def patient():
    return render_template('patient.html')

@app.route('/patientlogin',methods=['GET', 'POST'])
def patientlogin():
    return render_template('plogin.html')

import hashlib
@app.route('/register', methods=['GET','POST'])
def register():
    name=request.form.get('name')
    email=request.form.get('email')
    pwd=request.form.get('pwd')
    pno=request.form.get('pno')
    
    cursor=mysql.connection.cursor()
    #pwd = hashlib.md5(pwd.encode('utf-8')).digest()
    cursor.execute(''' INSERT INTO admin(name,password,email,phone_number) VALUES(%s,MD5(%s),%s,%s)''',(name,pwd,email,pno))
    mysql.connection.commit()
    cursor.close()
    return "success"

@app.route('/pregister', methods=['GET','POST'])
def pregister():
    pid=request.form.get('pid')
    pname=request.form.get('pname')
    pno=request.form.get('pno')
    paddr=request.form.get('paddr')
    ppass=request.form.get('ppass')
    
    cursor=mysql.connection.cursor()
    #pwd = hashlib.md5(pwd.encode('utf-8')).digest()
    cursor.execute(''' INSERT INTO patient(name,p_id,phone_no,address,ppass) VALUES(%s,%s,%s,%s,MD5(%s))''',(pname,pid,pno,paddr,ppass))
    mysql.connection.commit()
    cursor.close()
    return "success"

@app.route('/userlogin', methods=['GET', 'POST'])

def userlogin():
    uname=request.form.get('uname')
    pwd=request.form.get('pwd')
    cursor=mysql.connection.cursor()
    cursor.execute(''' SELECT * FROM user WHERE uname=%s and pwd=MD5(%s)''',(uname,pwd))
    row=cursor.fetchone()
    cursor.close()
    if row:
        
            return ("successfully logged")
        
        
    else:
        return "Failed to login"
    

@app.route('/plogin', methods=['GET', 'POST'])

def plogin():
    pid=request.form.get('pid')
    password=request.form.get('password')
    cursor=mysql.connection.cursor()
    cursor.execute(''' SELECT * FROM patient  WHERE p_id=%s and ppass=MD5(%s)''',(pid,password))
    row=cursor.fetchone()
    cursor.close()
    if row:
            response = make_response("successfully logged") # We can also render new page with render_template
            response.set_cookie('pid',pid)
            return response
        
            
        
        
    else:
        return "Failed to login"


@app.route('/login', methods=['GET','POST'])
def login():
    return render_template('login.html')

@app.route('/adminlogin', methods=['GET','POST'])
def adminlogin():
    email=request.form.get('email')
    password=request.form.get('password')
    cursor=mysql.connection.cursor()
    cursor.execute(''' SELECT * FROM admin WHERE email=%s and Password=MD5(%s)''',(email,password))
    row=cursor.fetchone()
    cursor.close()
    if row:
        
            return ("successfully logged")
        
        
    else:
        return "Failed to login"


@app.route('/appointment', methods=['GET'])
def appointment():
    return render_template('appointment.html')


@app.route('/admin', methods =['GET', 'POST'])
def admin():
    
    username = request.form.get('uname')
    password = request.form.get('psw')
    print(username, password)
    if username == 'admin' and password == 'ppp':
        #return redirect(url_for('adminlogin', username=username))
        return ('success')
    else:
        return ('Login failed')
    
@app.route('/binsert', methods =['GET', 'POST'])
def binsert():
    
    bid = request.form.get('bid')
    bname = request.form.get('bname')
    address = request.form.get('address')
    
    
    cursor = mysql.connection.cursor()
    cursor.execute(''' INSERT INTO branch(b_id,bname,address) VALUES(%s,%s,%s)''',(bid,bname,address))
    mysql.connection.commit()
    cursor.close()
    return "Inserted successfully"

@app.route('/makeappointment', methods =['GET', 'POST'])
def makeappointment():
    
    d_name = request.form.get('d_name')
    bdate= request.form.get('date')
    time = request.form.get('time')
    date_object = parser.parse(bdate)
    bdate = date_object.astimezone(pytz.timezone('Asia/Kolkata')) 
    p_id=request.cookies.get('pid')
    
    
    cursor = mysql.connection.cursor()
    cursor.execute(''' INSERT INTO appointment(date,time,p_id,d_id) VALUES(%s,%s,%s,%s)''',(bdate,time,p_id,d_name))
    mysql.connection.commit()
    last_id=cursor.lastrowid
    cursor.close()
    return "Your Appointment Number is: "+str(last_id)

@app.route('/ainsert', methods =['GET', 'POST'])
def ainsert():
    
    ap_id = request.form.get('ap_id')
    d_name = request.form.get('d_name')
    sdate = request.form.get('date')
    time = request.form.get('time')

    
    date_object = parser.parse(sdate)
    sdate = date_object.astimezone(pytz.timezone('Asia/Kolkata')) 
    #print(date_object)
    cursor = mysql.connection.cursor()
    cursor.execute(''' INSERT INTO appointment(ap_id,d_name,date,time) VALUES(%s,%s,%s,%s)''',(ap_id,d_name,sdate,time))
    mysql.connection.commit()
    cursor.close()
    return "Inserted successfully"


@app.route('/docinsert', methods =['GET', 'POST'])

def docinsert():
    docname=request.form.get('docname')
    ds=request.form.get('ds')
    brid=request.form.get('brid')
    docid=request.form.get('docid')
    print(docid)

    cursor=mysql.connection.cursor()
    cursor.execute(''' INSERT INTO doctors(d_id,name,specialization,b_id) VALUES(%s,%s,%s,%s)''',(docid,docname,ds,brid))
    mysql.connection.commit()
    cursor.close()
    return "Inserted successfully"

@app.route('/rinsert', methods =['GET', 'POST'])
def rinsert():
    
    
    rname = request.form.get('rname')
    rdes=request.form.get('rdes')
    rtid=request.form.get('rrtid')
    ravalue=request.form.get('ravalue')
    rstatus=request.form.get('rstatus')
    f = request.files['rfile']       
    filename = secure_filename(f.filename)
    now = datetime.now()
    dt_string = now.strftime("%d%m%Y%H%M%S")
    rimg=dt_string+"_"+filename
    f.save("static/resources/" + rimg)
    cursor = mysql.connection.cursor()
    cursor.execute(''' INSERT INTO resource(rname,rdesc,rtid,avalue,rimg,rstatus) VALUES(%s,%s,%s,%s,%s,%s)''',(rname,rdes,rtid,ravalue,rimg,rstatus))
    mysql.connection.commit()
    cursor.close()
    return "Inserted successfully"


@app.route('/bupdate', methods =['GET', 'POST'])
def bupdate():
    
    did=request.form.get('did')
    bname = request.form.get('bname')
    address = request.form.get('address')
    
    #print(date_object)
    cursor = mysql.connection.cursor()
    cursor.execute(''' UPDATE branch SET bname=%s,address=%s WHERE b_id=%s''',(bname,address,did))
    mysql.connection.commit()
    cursor.close()
    return "Updated successfully"

@app.route('/rtupdate', methods =['GET', 'POST'])
def rtupdate():
    
    rtid=request.form.get('rtid')
    rtype = request.form.get('rtname')
    rtdesc = request.form.get('rtdes')
    
    cursor = mysql.connection.cursor()
    cursor.execute(''' UPDATE resourcetype SET rtype=%s,rtdesc=%s WHERE rtid=%s''',(rtype,rtdesc,rtid))
    mysql.connection.commit()
    cursor.close()
    return "Updated successfully"


@app.route('/bdelete', methods =['GET', 'POST'])
def bdelete():
    
    did=request.form.get('did')
    cursor = mysql.connection.cursor()
    cursor.execute(''' DELETE FROM branch WHERE b_id=%s''',(did,))
    mysql.connection.commit()
    cursor.close()
    return "Deleted successfully"

@app.route('/appdelete', methods =['GET', 'POST'])
def appdelete():
    
    did=request.form.get('did')
    cursor = mysql.connection.cursor()
    cursor.execute(''' DELETE FROM appointment WHERE ap_id=%s''',(did,))
    mysql.connection.commit()
    cursor.close()
    return "Deleted successfully"


@app.route('/docdelete', methods =['GET', 'POST'])
def docdelete():
    
    rtid=request.form.get('rtid')
    cursor = mysql.connection.cursor()
    cursor.execute(''' DELETE FROM doctors WHERE d_id=%s''',(rtid,))
    mysql.connection.commit()
    cursor.close()
    return "Deleted successfully"

@app.route('/rdelete', methods =['GET', 'POST'])
def rdelete():
    
    rid=request.form.get('rid')
    cursor = mysql.connection.cursor()
    cursor.execute(''' DELETE FROM resource WHERE rid=%s''',(rid,))
    mysql.connection.commit()
    cursor.close()
    return "Deleted successfully"

@app.route('/getbranchnames', methods =['GET', 'POST'])

def getbranchnames():
    
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM branch")
    DBData = cursor.fetchall() 
    cursor.close()
    
    rtnames=''
    for result in DBData:
        print(result)
        rtnames+="<option value="+str(result[0])+">"+result[1]+"</option>"
    return rtnames    

@app.route('/getdoctornames', methods =['GET', 'POST'])

def getdoctornames():
    
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM doctors")
    DBData = cursor.fetchall() 
    cursor.close()
    
    rtnames=''
    for result in DBData:
        print(result)
        rtnames+="<option value="+str(result[0])+">"+result[1]+"</option>"
    return rtnames  

@app.route('/appshow', methods =['GET', 'POST'])
def appshow():
    
    cursor = mysql.connection.cursor()
    p_id=request.cookies.get('pid')
    cursor.execute("SELECT * FROM appointment where p_id=%s",(p_id,))
    row_headers=[x[0] for x in cursor.description] 
    DBData = cursor.fetchall() 
    cursor.close()
    json_data=[]
    rstr="<table border><tr>"
    for r in row_headers:
        rstr=rstr+"<th>"+r+"</th>"
    rstr=rstr+"<th>Delete</th></tr>"
    cnt=0
    did=-1
    for result in DBData:
        cnt=0
        ll=['A','B','C','D','E','F','G','H','I','J','K']
        for row in result:
            if cnt==0:
                did=row
                rstr=rstr+"<td>"+str(row)+"</td>" 
            elif cnt>=1:
                rstr=rstr+"<td>"+str(row)+"</td>" 
            else:
                rstr=rstr+"<td>"+"<input type=text id=AP"+str(ll[cnt])+str(did)+" value=\""+str(row)+"\"></td>"     
            cnt+=1
            
        
        rstr+="<td><a ><i class=\"fa fa-trash\" aria-hidden=\"true\" onclick=apdel("+str(did)+")></i></a></td>"
        
        rstr=rstr+"</tr>"
    
    rstr=rstr+"</table>"
    rstr=rstr+'''
    <script type=\"text/javascript\">
    
   
    function apdel(did)
    {
    $.ajax({
        url: \"/appdelete\",
        type: \"POST\",
        data: {did:did},
        success: function(data){
            alert(data);
            loadappointments();
        }
        });
    }
    function loadappointments(){

       $.ajax({
        url: 'http://127.0.0.1:5000/appshow',
        type: 'POST',
        success: function(data){
          $('#appshow').html(data);
        }
      });
    }
    
    
    </script>

'''
    return rstr

@app.route('/appallshow', methods =['GET', 'POST'])
def appallshow():
    
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM appointment")
    row_headers=[x[0] for x in cursor.description] 
    DBData = cursor.fetchall() 
    cursor.close()
    json_data=[]
    rstr="<table border><tr>"
    for r in row_headers:
        rstr=rstr+"<th>"+r+"</th>"
    rstr=rstr+"</tr>"
    cnt=0
    did=-1
    for result in DBData:
        cnt=0
        ll=['A','B','C','D','E','F','G','H','I','J','K']
        for row in result:
            if cnt==0:
                did=row
                rstr=rstr+"<td>"+str(row)+"</td>" 
            elif cnt>=1:
                rstr=rstr+"<td>"+str(row)+"</td>" 
            else:
                rstr=rstr+"<td>"+"<input type=text id=AP"+str(ll[cnt])+str(did)+" value=\""+str(row)+"\"></td>"     
            cnt+=1
            
        
        
        
        rstr=rstr+"</tr>"
    
    rstr=rstr+"</table>"
    rstr=rstr+'''
    

'''
    return rstr

@app.route('/bshow', methods =['GET', 'POST'])
def bshow():
    
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM branch")
    row_headers=[x[0] for x in cursor.description] 
    DBData = cursor.fetchall() 
    cursor.close()
    json_data=[]
    rstr="<table border><tr>"
    for r in row_headers:
        rstr=rstr+"<th>"+r+"</th>"
    rstr=rstr+"<th>Update</th><th>Delete</th></tr>"
    cnt=0
    did=-1
    for result in DBData:
        cnt=0
        ll=['A','B','C','D','E','F','G','H','I','J','K']
        for row in result:
            if cnt==0:
                did=row
                rstr=rstr+"<td>"+str(row)+"</td>" 
            elif cnt==3:
                rstr=rstr+"<td>"+"<input type=date id="+str(ll[cnt])+str(did)+" value="+str(row)+"></td>"  
            else:
                rstr=rstr+"<td>"+"<input type=text id=B"+str(ll[cnt])+str(did)+" value=\""+str(row)+"\"></td>"     
            cnt+=1
            
        rstr+="<td><a ><i class=\"fa fa-edit\" aria-hidden=\"true\" onclick=bupdate("+str(did)+")></i></a></td>"
        rstr+="<td><a ><i class=\"fa fa-trash\" aria-hidden=\"true\" onclick=bdel("+str(did)+")></i></a></td>"
        
        rstr=rstr+"</tr>"
    
    rstr=rstr+"</table>"
    rstr=rstr+'''
    <script type=\"text/javascript\">
    function bupdate(did)
    {
       bname=$("#BB"+did).val();
       address=$("#BC"+did).val();
      
       $.ajax({
        url: \"/bupdate\",
        type: \"POST\",
        data: {did:did,bname:bname,address:address},
        success: function(data){    
        alert(data);
        loadbranches();
        }
       });
    }
   
    function bdel(did)
    {
    $.ajax({
        url: \"/bdelete\",
        type: \"POST\",
        data: {did:did},
        success: function(data){
            alert(data);
            loadbranches();
        }
        });
    }
    function loadbranches(){

       $.ajax({
        url: 'http://127.0.0.1:5000/bshow',
        type: 'POST',
        success: function(data){
          $('#bshow').html(data);
        }
      });
    }
    
    
    </script>

'''
    return rstr


@app.route('/docshow', methods =['GET', 'POST'])
def docshow():
    
    cursor = mysql.connection.cursor()

    cursor.execute("SELECT * FROM doctors")
    row_headers=[x[0] for x in cursor.description] 
    DBData = cursor.fetchall() 
    cursor.close()
    json_data=[]
    rstr="<table border><tr>"
    for r in row_headers:
        rstr=rstr+"<th>"+r+"</th>"
    rstr=rstr+"<th>Update</th><th>Delete</th></tr>"
    cnt=0
    did=-1
    for result in DBData:
        cnt=0
        ll=['A','B','C','D','E','F','G','H','I','J','K']
        for row in result:
            if cnt==0:
                rtid=row
                rstr=rstr+"<td>"+str(row)+"</td>" 
           
            else:
                rstr=rstr+"<td>"+"<input type=text id=DOC"+str(ll[cnt])+str(rtid)+" value=\""+str(row)+"\"></td>"     
            cnt+=1
            
        rstr+="<td><a ><i class=\"fa fa-edit\" aria-hidden=\"true\" onclick=docupdate("+str(rtid)+")></i></a></td>"
        rstr+="<td><a ><i class=\"fa fa-trash\" aria-hidden=\"true\" onclick=docdel("+str(rtid)+")></i></a></td>"
        
        rstr=rstr+"</tr>"
    
    rstr=rstr+"</table>"
    rstr=rstr+'''
    <script type=\"text/javascript\">
    function docupdate(rtid)
    {
       //alert('aha no');
       docname=$("#DOCB"+rtid).val();
       ds=$("#DOCC"+rtid).val();
       $.ajax({
        url: \"/docupdate\",
        type: \"POST\",
        data: {rtid:rtid,docname:docname,ds:ds},
        success: function(data){
       
        alert(data);
        loaddoctors();
        }
       });
    }
   
    function docdel(rtid)
    {
    $.ajax({
        url: \"/docdelete\",
        type: \"POST\",
        data: {rtid:rtid},
        success: function(data){
        alert(data);
        loaddoctors();
        }
        });
    }
   
    function loaddoctors(){
       $.ajax({
        url: 'http://127.0.0.1:5000/docshow',
        type: 'POST',
        success: function(data){
          $('#docshow').html(data);
        }
      });
    }
    
    
    </script>

'''
    return rstr
@app.route('/docupdate', methods=['GET', 'POST'])

def docupdate():
    rtid=request.form.get('rtid')
    docname=request.form.get('docname')
    ds=request.form.get('ds')
    
    cursor = mysql.connection.cursor()
    cursor.execute(''' UPDATE doctors SET name=%s,specialization=%s WHERE d_id=%s''',(docname,ds,rtid))
    mysql.connection.commit()
    cursor.close()
    return "Updated successfully"
@app.route('/rshow', methods=['GET', 'POST'])

def rshow():
    cursor = mysql.connection.cursor()

    cursor.execute("SELECT * FROM resource")
    row_headers=[x[0] for x in cursor.description] 
    DBData = cursor.fetchall() 
    cursor.close()
    json_data=[]
    rstr="<table border><tr>"
    for r in row_headers:
        rstr=rstr+"<th>"+r+"</th>"
    rstr=rstr+"<th>Update</th><th>Delete</th></tr>"
    cnt=0
    did=-1
    for result in DBData:
        cnt=0
        ll=['A','B','C','D','E','F','G','H','I','J','K']
        for row in result:
            if cnt==0:
                rid=row
                rstr=rstr+"<td>"+str(row)+"</td>" 
            elif cnt==5:
                rfil="http://127.0.0.1:5000/static/resources/"+str(row)
                rstr=rstr+"<td>"+"<a href=\""+str(rfil)+"\" target=_blank>File</a></td>"
            else:
                rstr=rstr+"<td>"+"<input type=text id="+str(ll[cnt])+str(rid)+" value=\""+str(row)+"\"></td>"     
            cnt+=1
            
        rstr+="<td><a ><i class=\"fa fa-edit\" aria-hidden=\"true\" onclick=resupdate("+str(rid)+")></i></a></td>"
        rstr+="<td><a ><i class=\"fa fa-trash\" aria-hidden=\"true\" onclick=resdel("+str(rid)+")></i></a></td>"
        
        rstr=rstr+"</tr>"
    
    rstr=rstr+"</table>"
    rstr=rstr+'''
    <script type=\"text/javascript\">
    function resupdate(rid)
    {
       //alert('aha no');

       rname=$("#B"+rid).val();
       rdes=$("#C"+rid).val();
       rtid=$("#D"+rid).val();
       ravalue=$("#E"+rid).val();
       rstatus=$("#G"+rid).val();
       var fd=new FormData();
       fd.append('rname',rname);
       fd.append('rdes',rdes);
       fd.append('rtid',rtid);
       fd.append('ravalue',ravalue);
       fd.append('rstatus',rstatus);
       fd.append('rid',rid); 

       $.ajax({
        url: \"/rupdate\",
        type: \"POST\",
        data: fd,
        processData: false,
        contentType: false,
        success: function(data){
       
        alert(data);
        loadresources();
        }
       });
    }
   
    function resdel(rid)
    {
    $.ajax({
        url: \"/rdelete\",
        type: \"POST\",
        data: {rid:rid},
        success: function(data){
        alert(data);
        loadresources();
        }
        });
    }
   
    
    function loadresources(){
       $.ajax({
        url: 'http://127.0.0.1:5000/rshow',
        type: 'POST',
        success: function(data){
          $('#rshow').html(data);
        }
      });
    }
    
    
    </script>

'''
    return rstr


                              
@app.route('/adminav', methods =['GET', 'POST'])
def adminav():
    return render_template('adminnav.html')


if __name__ == '__main__':
    app.run(debug=True)