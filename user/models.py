from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.utils.timezone import now
class Place(models.Model):
    gplaceid = models.CharField(max_length=500, default="0")
    placename = models.CharField(max_length=1000)
    popularity = models.IntegerField()
    lat = models.FloatField()
    lng = models.FloatField()
    stoptype = models.CharField(max_length=100)
    placeid = models.IntegerField(primary_key=True)
    district = models.CharField(max_length=200, default="UNKNOWN")
    state = models.CharField(max_length=200, default="Kerala")
    departadd=models.ManyToManyField('self', through='Connect',related_name="departadd")
    def __str__(self):
        return self.placename

class MKUser(models.Model):
    name = models.CharField(max_length=1000)
    uid = models.CharField(max_length = 200, primary_key=True)
    phone = models.CharField(max_length = 30)
    type = models.CharField(max_length = 10)
    logincreds = models.CharField(max_length = 1000)
    bookings = models.ManyToManyField('Booking')

class Booking(models.Model):
    user = models.ForeignKey(MKUser, on_delete=models.SET("DELETED"))
    origin = models.ForeignKey(Place, on_delete=models.SET("DELETED"), related_name = "bookingorigin")
    dest = models.ForeignKey(Place, on_delete=models.SET("DELETED"), related_name = "bookingdest")
    totalprice = models.IntegerField()
    nbuses = models.IntegerField()



class Conductor(models.Model):
    conductorid = models.IntegerField()
    name = models.CharField(max_length=1000)
    employer = models.ForeignKey("Owner", on_delete=models.SET("DELETED"))
    phone = models.CharField(max_length=30)
    passhash = models.CharField(max_length=1000)
    # assignedroutes = models.ManyToManyField("Route", related_name="conductorassignedrouteroute")
    presentbus = models.ManyToManyField("Bus",related_name="conductorpresentbus")
    def __str__(self):
        return(str(self.conductorid)+" : "+self.name)


class Route(models.Model):
    orig = models.ForeignKey(Place, on_delete=models.SET("DELETED"), related_name="routeorigplace")
    dest = models.ForeignKey(Place,  on_delete=models.SET("DELETED"),related_name="routedestplace")
    origt= models.DateTimeField()
    destt = models.DateTimeField()
    stopsadd = models.ManyToManyField(
        Place, 
        # related_name="routestopsplaces",
        through='BusInStop',
        through_fields=('route','place'),
    )
    nstops=models.IntegerField(default=1)
    getints = ArrayField(models.DateTimeField())
    getoutts = ArrayField(models.DateTimeField())
    bus = models.ForeignKey("Bus", on_delete=models.CASCADE,related_name="routes")
    routeid = models.IntegerField(primary_key=True)
    conductor = models.ForeignKey(Conductor, on_delete=models.SET("UNASSIGNED"))
    def __str__(self):
        return str(self.routeid)+" : "+self.orig.placename+" -> "+self.dest.placename

class Owner(models.Model):
    name = models.CharField(max_length=1000)
    phone = models.CharField(max_length=30)
    ownedbuses = models.ManyToManyField("Bus", related_name="ownerownedbusesbus")
    address = models.CharField(max_length=3000)
    passhash = models.CharField(max_length=1000)
    ownerid = models.IntegerField()
    def __str__(self):
        return(str(self.ownerid)+" : "+self.name)


class Bus(models.Model):
    name = models.CharField(max_length=1000)
    busid = models.IntegerField(primary_key=True)
    buscategory = models.CharField(max_length=100)
    bustype = models.CharField(max_length=100)
    owner = models.ForeignKey(Owner, on_delete=models.SET("DELETED"))
    # routes = models.ManyToManyField(Route, related_name="busroutesroute")
    regno = models.CharField(max_length=30)
    latideal = models.FloatField()
    lngideal = models.FloatField()
    affiliationlevel = models.CharField(max_length=100)
    havegps = models.IntegerField()
    latreal = models.FloatField()
    lngreal = models.FloatField()
    lastupdated = models.TimeField()
    presentconductor = models.ForeignKey(Conductor, on_delete=models.SET('UNASSIGNED'))
    categoryname = models.CharField(max_length=200, default="UNKNOWN")
    def __str__(self):
        return(str(self.busid)+" : "+self.name)
    
class BusInStop(models.Model):
    businstopid = models.CharField(max_length=200, default="1", primary_key=True)
    place = models.ForeignKey(Place,on_delete=models.CASCADE, related_name="routes")
    route = models.ForeignKey(Route,on_delete=models.CASCADE, related_name="stops")
    getint = models.DateTimeField()
    getoutt=models.DateTimeField()
    finaldest=models.ForeignKey(Place,on_delete=models.CASCADE,default=1, related_name="finaldest")
    finaldesttime=models.DateTimeField()
    ithstop=models.IntegerField()
    def __str__(self):
        return(self.place.placename)

class Connect(models.Model):
    getinp=models.ForeignKey(Place,related_name="departures", on_delete=models.CASCADE)
    getoutp=models.ForeignKey(Place,related_name="arrivals", on_delete=models.CASCADE)
    fromgetint=models.DateTimeField()
    togetint=models.DateTimeField()
    fromgetoutt=models.DateTimeField()
    togetoutt=models.DateTimeField()
    connectid=models.CharField(max_length=1000, primary_key=True)
    route=models.ForeignKey(Route, on_delete=models.CASCADE, related_name="connects")
    price=models.IntegerField(default=99)
    isgetinpstand=models.IntegerField(default=0)
    def __str__(self):
        return str(self.connectid)+" -> "+str(self.togetoutt.strftime("%H:%M"))



class SingleSearchResult(models.Model):
    getinp=models.ForeignKey(Place,related_name="departforisnglesearch", on_delete=models.CASCADE)
    getoutp=models.ForeignKey(Place,related_name="arriveforsinglesearch", on_delete=models.CASCADE)
    fromgetint=models.DateTimeField()
    togetint=models.DateTimeField()
    fromgetoutt=models.DateTimeField()
    togetoutt=models.DateTimeField()
    connectid=models.CharField(max_length=1000, primary_key=True)
    route=models.ForeignKey(Route, on_delete=models.CASCADE, related_name="routeforsinglesearch")
    price=models.IntegerField(default=99)
    isgetinpstand=models.IntegerField(default=0)
    searchtoreach=models.DateTimeField(default=now)
    def __str__(self):
        return str(self.connectid)+" -> "+str(self.togetoutt.strftime("%H:%M"))


class DoubleSearchResult(models.Model):
    getinp1=models.ForeignKey(Place,related_name="gi1d", on_delete=models.CASCADE)
    getoutp1=models.ForeignKey(Place,related_name="go1d", on_delete=models.CASCADE)
    getinp2=models.ForeignKey(Place,related_name="gi2d", on_delete=models.CASCADE)
    getoutp2=models.ForeignKey(Place,related_name="go2d", on_delete=models.CASCADE)
    route1=models.ForeignKey(Route, on_delete=models.CASCADE, related_name="r1d")
    route2=models.ForeignKey(Route, on_delete=models.CASCADE, related_name="r2d")
    price1=models.IntegerField(default=99)
    price2=models.IntegerField(default=99)
    fromgetint1=models.DateTimeField()
    togetint1=models.DateTimeField()
    fromgetoutt1=models.DateTimeField()
    togetoutt1=models.DateTimeField()
    fromgetint2=models.DateTimeField()
    togetint2=models.DateTimeField()
    fromgetoutt2=models.DateTimeField()
    togetoutt2=models.DateTimeField()
    con1=models.ForeignKey(Connect,on_delete=models.CASCADE,related_name="con1")
    con2=models.ForeignKey(Connect,on_delete=models.CASCADE,related_name="con2")
    id=models.IntegerField(primary_key=True,default=0)
    searchtoreach=models.DateTimeField(default=now)
    def __str__(self):
        return(str(self.con1)+" || "+ str(self.con2))