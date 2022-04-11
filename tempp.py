import os
import datetime
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "uwebsite.settings")
import django
django.setup()
# your imports, e.g. Django models
from user.models import *

import mysql.connector
cnx = mysql.connector.connect(
    user='root', 
    password='Nirmal#21',
    host='34.93.225.93', 
    )
curr=cnx.cursor()


owner=Owner.objects.first()
conductor=Conductor.objects.first()
newBus=Bus(
    name="KSRTC GRDMRAJ",
    busid=14,
    buscategory="GRDMRAJ",
    bustype="KSRTC",
    owner=owner,
    regno="KL150000",
    latideal=1,
    lngideal=1,
    affiliationlevel="NIL",
    havegps=0,
    latreal=1,
    lngreal=1,
    lastupdated="00:00:01",
    presentconductor=conductor
)
newBus.save()