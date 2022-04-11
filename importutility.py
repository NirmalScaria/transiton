def updatePlace():
    comm="select * from parakkumthalika.stops;"
    curr.execute(comm)
    ress=curr.fetchall()
    for x in ress:
        if(x[3]<13.852403):
            if(x[3]>7.579607):
                if(x[4]>74.018596):
                    if(x[4]<78.801515):
                        if(len(x[5])>10):
                            stoptypee = "STOP"
                            if x[7] > 2000:
                                stoptypee="STAND"
                            if x[7]>5000 :
                                stoptypee = "TERMINAL"
                            
                            newplace=Place(
                                placeid=x[0],
                                placename=x[1],
                                popularity = x[7],
                                lat= x[3],
                                lng=x[4],
                                stoptype=stoptypee,
                                gplaceid=x[5],
                                district = x[2],
                                state  = x[6]
                            )
                            newplace.save()
def addroute(a):
    # Take array [routeid , busid , originid , destid , nstops , stops[], getintimes[], getouttimes[], typeofbus(LS/O/SF/SL)]

    myrouteid=a[0]
    print("ADDING ROUTE: "+str(myrouteid))
    myorig=Place.objects.filter(placeid=a[2]).first()
    mydest=Place.objects.filter(placeid=a[3]).first()
    myorigt=a[6][0]
    mydestt=a[6][a[4]-1]
    mygetints=a[6]
    mygetoutts=a[7]
    mynstops=a[4]
    mystops=a[5]
    j=0
    origgcount=Place.objects.filter(placeid=mystops[0]).count()
    desttcount=Place.objects.filter(placeid=mystops[mynstops-1]).count()
    if(origgcount<1):
        print("FAILED. ORIGIN NOT ADDED")
        return(0)
    if(desttcount<1):
        print("FAILED. DEST NOT ADDED")
        return(0)
    for i in range(mynstops):
        ss=Place.objects.filter(placeid=mystops[i-j]).count()
        if(ss<1):
            print("DOESNT EXIST (REMOVED)")
            mystops.pop(i-j)
            mygetints.pop(i-j)
            mynstops-=1
            i+=1
            j+=1
        else:
            print(str(Place.objects.filter(placeid=mystops[i-j]).first())+" : "+mygetints[i-j].strftime("%Y-%m-%d %H:%M:%S"))
    if(a[1]==0):
        mybus=Bus.objects.filter(buscategory=a[8]).first()
    else:
        mybus=Bus.objects.filter(busid=a[1]).first()
    myconductor=Conductor.objects.filter(conductorid=a[9]).first()
    temproute=Route(
        orig=myorig,
        dest=mydest,
        origt=myorigt,
        destt=mydestt,
        getints=mygetints,
        getoutts=mygetoutts,
        bus=mybus,
        conductor=myconductor,
        routeid=myrouteid,
        nstops=mynstops
    )

    temproute.save()
    for j in range(mynstops):
        sstopid=mystops[j]
        smyplace=Place.objects.filter(placeid=sstopid).first()
        smyroute=temproute
        smygetint=mygetints[j]
        smygetoutt=mygetoutts[j]
        smyfinaldest=mydest
        smyfinaldestt=mydestt
        smyithstop=j
        smybusinstopid=str(smyroute.routeid)+"@"+str(smyplace.placeid)+"@"+smygetint.strftime("%H:%M:%S")
        tempBusinStop=BusInStop(
            businstopid=smybusinstopid,
            place=smyplace,
            route=smyroute,
            getint=smygetint,
            getoutt=smygetoutt,
            finaldest=smyfinaldest,
            finaldesttime=smyfinaldestt,
            ithstop=smyithstop
        )
        if(BusInStop.objects.filter(businstopid=smybusinstopid).count()<1):
            tempBusinStop.save()
        else:
            print("ROUTEINSTOP ALREADY EXISTS : "+smybusinstopid)
    for i in range(mynstops-1):
        for j in range(i+1,mynstops):
            myconnectid=str(myrouteid)+":"+str(mystops[i])+"->"+str(mystops[j])+"@"+mygetoutts[i].strftime("%H:%M:%S")
            tempConn=Connect(
                getinp=Place.objects.filter(placeid=mystops[i]).first(),
                getoutp=Place.objects.filter(placeid=mystops[j]).first(),
                fromgetint=mygetints[i],
                togetint=mygetints[j],
                fromgetoutt=mygetoutts[i],
                togetoutt=mygetoutts[j],
                route=temproute,
                connectid=myconnectid
            )
            if(Connect.objects.filter(connectid=myconnectid).count()<1):
                tempConn.save()
            else:
                print("CONNECT ALREADY EXISTS : "+myconnectid)




def importroutessfromserver(curr):
    comm = "select * from routes.routes;"
    curr.execute(comm)
    rows=curr.fetchall()
    for item in rows:
        routeid=item[0]
        busid=0
        originid=item[2]
        destid=item[3]
        nstops=item[4]
        stops=item[5].strip('][').split(", ")
        getintimes=item[6].strip(']["').split('", "')
        getouttimes=item[6].strip(']["').split('", "')
        getintimesnew=[datetime.datetime.strptime(getintimes[0], "%H:%M:%S")]
        extra=0
        for k in range(1,len(getintimes)):
            if(datetime.datetime.strptime(getintimes[k], "%H:%M:%S")<getintimesnew[k-1]):
                extra=1
                # print(item[0])
                # print("YOOOO")
                
            getintimesnew+=[datetime.datetime.strptime(getintimes[k], "%H:%M:%S")+datetime.timedelta(days=extra)]
        getintimes=[]
        for itemp in getintimesnew:
            getintimes+=[pytz.utc.localize(itemp)]
        getouttimes=getintimes
        
        typeofbus="UK"
        if(item[8].find("Ordinary")>-1):
            typeofbus="ORD"
        if(item[8].find("Super Fast")>-1):
            typeofbus="SF"
        if(item[8].find("Super Deluxe")>-1):
            typeofbus="SDLX"
        if(item[8].find("Super Express")>-1):
            typeofbus="SXP"
        if(item[8].find("Fast Passenger")>-1):
            typeofbus="FP"
        if(item[8].find("Ananthapuri Fast")>-1):
            typeofbus="AF"
        if(item[8].find("Garuda King")>-1):
            typeofbus="GRDKNG"
        if(item[8].find("Garuda Maha")>-1):
            typeofbus="GRDMRAJ"
        if(item[8].find("Limited Stop Ordinary")>-1):
            typeofbus="LSO"
        if(item[8].find("Limited Stop Fast Passenger")>-1):
            typeofbus="LSFP"
        if(item[8].find("Low Floor Non AC")>-1):
            typeofbus="LF"
        if(item[8].find("Town to Town Ordinary")>-1):
            typeofbus="T2T"
        if(item[8].find("Low Floor AC Volvo")>-1):
            typeofbus="LFAC"
        if(item[8].find("Point to Point")>-1):
            typeofbus="P2PFP"
        conductorid=0
        a=[routeid,busid,originid,destid,nstops,stops,getintimes,getouttimes,typeofbus,conductorid]
        print(a)
        addroute(a)
    #array [routeid , busid , originid , destid , nstops , stops[], getintimes[], getouttimes[], typeofbus(LS/O/SF/SL),conductorid]
    a=[4900,0,143,406,6,[143,5555,9999, 402, 45, 406],["10:30:00","23:59:00","23:59:00", "10:50:00", "11:30:00", "12:00:00"],["10:30:00","23:59:00","23:59:00", "10:50:00", "11:30:00", "12:00:00"],"LS",0]
    # addroute(a)
import os
import datetime
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "uwebsite.settings")
import django
django.setup()
# your imports, e.g. Django models
from user.models import *
from django.utils import timezone
import pytz
import mysql.connector
cnx = mysql.connector.connect(
    user='root', 
    password='Nirmal#21',
    host='34.93.225.93', 
    )
curr=cnx.cursor()


curr.close()
cnx.close()


