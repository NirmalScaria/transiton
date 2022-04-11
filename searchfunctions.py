import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "uwebsite.settings")
import django
django.setup()
from user.models import *
from django.utils import timezone
import pytz
import re
import datetime
from django.db import connection
from atpbar import atpbar
from operator import itemgetter
def singlesearch(fromid,toid,time):
    rawcommand="select * , ( CASE WHEN (fromgetoutt >= '"+time+"') THEN (togetint-'"+time+"') ELSE (togetint + make_interval(days => 1)-'"+time+"') END) as searchtoreach from user_connect where getinp_id = '"+str(fromid)+"' and getoutp_id = '"+str(toid)+"' order by ( CASE WHEN (fromgetoutt >= '"+time+"') THEN (togetint) ELSE (togetint + make_interval(days => 1)) END) limit 10;"

    pp=SingleSearchResult.objects.raw(rawcommand)
    return(pp)

def doublesearch(fromid,toid,time):
    rawcommand="""
    SELECT    


    thefirst.getinp_id as getinp1_id,
    thefirst.getoutp_id as getoutp1_id,
    thesecond.getinp_id as getinp2_id,
    thesecond.getoutp_id as getoutp2_id,
    thefirst.route_id as route1_id,
    thesecond.route_id as route2_id,
    thefirst.price as price1,
    thesecond.price as price2,
    thefirst.fromgetint as fromgetint1,
    thefirst.fromgetoutt as fromgetoutt1,
    thefirst.togetint as togetint1,
    thefirst.togetoutt as togetoutt1,
    thesecond.fromgetint as fromgetint2,
    thesecond.fromgetoutt as fromgetoutt2,
    thesecond.togetint as togetint2,
    thesecond.togetoutt as togetoutt2,
    thefirst.connectid as con1_id,
    thesecond.connectid as con2_id,
    1 as id,
    
    
    ( CASE WHEN 
        (thefirst.fromgetoutt >= '"""+time+"""') 
            THEN 
                (thefirst.togetint-'"""+time+"""') 
            ELSE 
                (thefirst.togetint + make_interval(days => 1)-'"""+time+"""') 
    END)  /* THIS GIVES TIME FROM SEARCH TO FIRST REACH */
    

    
    +

    ( CASE WHEN 
        (thesecond.fromgetoutt >= (CASE WHEN thefirst.togetint<= '1900-01-02 00:00:00+00:00' THEN thefirst.togetint ELSE thefirst.togetint - make_interval(days => 1) END)) 
            THEN 
                (thesecond.togetint-(CASE WHEN thefirst.togetint<= '1900-01-02 00:00:00+00:00' THEN thefirst.togetint ELSE thefirst.togetint - make_interval(days => 1) END)) 
            ELSE 
                (thesecond.togetint + make_interval(days => 1)-(CASE WHEN thefirst.togetint<= '1900-01-02 00:00:00+00:00' THEN thefirst.togetint ELSE thefirst.togetint - make_interval(days => 1) END)) 
    END)
    
   
    
    as searchtoreach
    
    FROM 
    user_connect as thefirst 
    INNER JOIN 
    user_connect as thesecond 

    ON 
    thefirst.getoutp_id=thesecond.getinp_id 
    AND 
    thefirst.getinp_id="""+str(fromid)+""" 
    AND 
    thesecond.getoutp_id="""+str(toid)+"""
    AND
    thefirst.route_id!=thesecond.route_id
    

    ORDER BY
    searchtoreach

    limit 1000;
    """
    pp=DoubleSearchResult.objects.raw(rawcommand)
    a=[]
    b=[]
    firstr=[]
    secondr=[]
    for item in pp:
        if(item.route1_id not in firstr):
            firstr+=[item.route1_id]
            a+=[item]
    for item in a:
        if(item.route2_id not in secondr):
            secondr+=[item.route2_id]
            b+=[item]

    a=[]
    for item in b:
        if(BusInStop.objects.filter(route_id=item.route1_id,place_id=toid).count()==0):
            if(BusInStop.objects.filter(route_id=item.route2_id,place_id=fromid).count()==0):
                a+=[item]
    return(a)
    




# doublesearch(666,55,"1900-01-01 10:30:00+00:00")


def nameformat(namee):
    return(re.sub("[\(\[].*?[\)\]]", "", namee).replace("BS","").title())


def formattedsearchres(fromid,toid,time):
    single=singlesearch(fromid,toid,time+"+00:00")
    double=doublesearch(fromid,toid,time+"+00:00")
    countsf=0
    countls=0
    countord=0
    countsl=0
    totalcount=len(double)+len(single)
    
    

    
    allroutes=[]
    for item in single:
        mycategorycode="ORD"
        if(item.route.bus.buscategory=="LSO"):
            countls+=1
            mycategorycode="LS"
        elif(item.route.bus.buscategory=="ORD"):
            countord+=1
            mycategorycode="ORD"
        elif(item.route.bus.buscategory=="LSFP"):
            countsf+=1
            mycategorycode="SF"
        elif(item.route.bus.buscategory=="UNK"):
            countord+=1
            mycategorycode="ORD"
        elif(item.route.bus.buscategory=="FP"):
            countsf+=1
            mycategorycode="SF"
        elif(item.route.bus.buscategory=="SF"):
            countsf+=1
            mycategorycode="SF"
        elif(item.route.bus.buscategory=="P2PFP"):
            countsf+=1
            mycategorycode="SF"
        else:
            countsl+=1
            mycategorycode="SL"
        indivroute={
                    "routetags" : "DIRECT",
                    "nbuses" : 1,
                    "searchtoreach": item.searchtoreach,
                    "b1getinp" : nameformat(item.getinp.placename),
                    "b1getint" : item.fromgetoutt.strftime("%I:%M %p"),
                    "b1getoutp" : nameformat(item.getoutp.placename),
                    "b1getoutt" : item.togetint.strftime("%I:%M %p"),
                    "b1name" : item.route.bus.name,
                    "b1orig" : nameformat(item.route.orig.placename),
                    "b1dest" : nameformat(item.route.dest.placename),
                    "b1category" : item.route.bus.categoryname,
                    "b1categorycode":mycategorycode,
                    "b1fare" : "₹ "+str(item.price),
                    "b1tags" : [{
                        "tagtext" : "Usually on time",
                        "tagicon" : "&#xe8b5;"
                    },
                    {
                        "tagtext" : "No realtime data",
                        "tagicon" : "&#xe8db;"
                    }
                    ],
                    "reachby" : item.togetint.strftime("%I:%M %p")
                }
        allroutes+=[indivroute]

    for item in double:
        mycategorycode1="ORD"
        mycategorycode2="ORD"
        if(item.route1.bus.buscategory=="LSO"):
            countls+=1
            mycategorycode1="LS"
        elif(item.route1.bus.buscategory=="ORD"):
            countord+=1
            mycategorycode1="ORD"
        elif(item.route1.bus.buscategory=="LSFP"):
            countsf+=1
            mycategorycode1="SF"
        elif(item.route1.bus.buscategory=="UNK"):
            countord+=1
            mycategorycode1="ORD"
        elif(item.route1.bus.buscategory=="FP"):
            countsf+=1
            mycategorycode1="SF"
        elif(item.route1.bus.buscategory=="SF"):
            countsf+=1
            mycategorycode1="SF"
        elif(item.route1.bus.buscategory=="P2PFP"):
            countsf+=1
            mycategorycode1="SF"
        else:
            countsl+=1
            mycategorycode1="SL"

        if(item.route2.bus.buscategory=="LSO"):
            countls+=1
            mycategorycode2="LS"
        elif(item.route2.bus.buscategory=="ORD"):
            countord+=1
            mycategorycode2="ORD"
        elif(item.route2.bus.buscategory=="LSFP"):
            countsf+=1
            mycategorycode2="SF"
        elif(item.route2.bus.buscategory=="UNK"):
            countord+=1
            mycategorycode2="ORD"
        elif(item.route2.bus.buscategory=="FP"):
            countsf+=1
            mycategorycode2="SF"
        elif(item.route2.bus.buscategory=="SF"):
            countsf+=1
            mycategorycode2="SF"
        elif(item.route2.bus.buscategory=="P2PFP"):
            countsf+=1
            mycategorycode2="SF"
        else:
            countsl+=1
            mycategorycode2="SL"
        seccs=(item.fromgetoutt2-item.togetint1).seconds
        hours, remainder = divmod(seccs, 3600)
        minutes, seconds = divmod(remainder, 60)
        waittext=""
        if(hours>0):
            if(hours>1):
                waittext+=str(hours)+" hours"
            else:
                waittext+=str(hours)+" hour"
            if(hours*minutes>0):
                waittext+=" and "
            if(minutes>0):
                if(minutes>1):
                    waittext+=str(minutes)+" minutes"
                else:
                    waittext+=str(minutes)+" minute"
        else:
            if(minutes>1):
                waittext+=str(minutes)+" minutes"
            else:
                if(minutes>0):
                    waittext+=str(minutes)+" minutes"
                else:
                    waittext+=" less than a minute"
        indivroute={
                "routetags" : "ONE LAYOVER",
                "nbuses" : 2,
                "searchtoreach": item.searchtoreach,
                "b1getinp" : nameformat(item.getinp1.placename),
                "b1getint" : item.fromgetoutt1.strftime("%I:%M %p"),
                "b1getoutp" : nameformat(item.getoutp1.placename),
                "b1getoutt" : item.togetint1.strftime("%I:%M %p"),
                "b1name" : item.route1.bus.name,
                "b1orig" : nameformat(item.route1.orig.placename),
                "b1dest" : nameformat(item.route1.dest.placename),
                "b1category" : item.route1.bus.categoryname,
                "b1fare" : "₹ "+str(item.price1),
                "b1categorycode":item.route1.bus.buscategory if(item.route1.bus.buscategory in ["LS","SF","ORD"]) else "SL",
                "b1tags" : [{
                    "tagtext" : "Usually on time",
                    "tagicon" : "&#xe8b5;"
                },
                {
                    "tagtext" : "No realtime data",
                    "tagicon" : "&#xe8db;"
                }
                ],
                "b12waitt":waittext,
                "b12ad" : "user/images/coffee.jpg",
                "b2getinp" : nameformat(item.getinp2.placename),
                "b2getint" : item.fromgetoutt2.strftime("%I:%M %p"),
                "b2getoutp" : nameformat(item.getoutp2.placename),
                "b2getoutt" : item.togetint2.strftime("%I:%M %p"),
                "b2name" : item.route2.bus.name,
                "b2orig" : nameformat(item.route2.orig.placename),
                "b2dest" : nameformat(item.route2.dest.placename),
                "b2category" : item.route2.bus.categoryname,
                "b2fare" : "₹ "+str(item.price2),
                "b2categorycode":item.route2.bus.buscategory if(item.route2.bus.buscategory in ["LS","SF","ORD"]) else "SL",
                "b2tags" : [{
                    "tagtext" : "Usually on time",
                    "tagicon" : "&#xe8b5;"
                },
                {
                    "tagtext" : "No realtime data",
                    "tagicon" : "&#xe8db;"
                }
                ],
                "reachby" : item.togetint2.strftime("%I:%M %p"),
            }
        allroutes+=[indivroute]

    demoresult = {
        "originname" : single[0].getinp,
        "destname" : single[0].getoutp,
        "searchtime" : datetime.datetime.strptime(time,"%Y-%m-%d %H:%M:%S").strftime("%I:%M %p"),
        "searchdate" : '18 AUG',
        "nbusesfound" : totalcount,
        "buscategories" : [
            {
            "category" : "Super Fast",
            "count" : countsf,
            "code":"SF"
            },
            {
            "category" : "Limited Stop",
            "count" : countls,
            "code":"LS"
            },
            {
            "category" : "Ordinary",
            "count" : countord,
            "code":"ORD"
            },
            {
            "category" : "Sleeper / AC",
            "count" : countsl,
            "code":"SL"
            },
        ],
        "bustypes"  : [
            {
                "type" : "KSRTC",
                "count" : "42"
            },
            {
                "type" : "Private",
                "count" : "3"
            },
        ],
        "routetypes" : [
            {
            "route" : "Direct only",
            "count" : "12"
            },
            {
            "route" : "One layover",
            "count" : "9"
            },
            {
            "route" : "Multiple layovers",
            "count" : "0"
            },
        ],
        "routes": [
            

            
        ]

    }
    allroutes=sorted(allroutes, key=itemgetter('searchtoreach'))
    allroutes[0]['routetags']+=" | REACH FIRST"
    demoresult['routes']=allroutes
    print(demoresult)
    return(demoresult)

# formattedsearchres(55,666,"1900-01-01 20:20:00+00:00")
#print(singlesearch(666,55,"1900-01-01 20:20:00+00:00"))
