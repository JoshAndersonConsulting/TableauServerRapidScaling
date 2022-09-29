#Parses XML Status into Dataframe that can be instered into PG Database

import psycopg2
import xml.etree.ElementTree as ET
import pandas as pd
from datetime import datetime as dt

column_names = ["created", "machine_name", "external", "service", "worker", "status", "preferred"]
rows =[]
now = dt.now()

mytree = ET.parse('systeminfo.xml')
myroot = mytree.getroot()

for machine in myroot.find('machines'):
    name = machine.attrib['name']
    external = machine.attrib['external']

    for services in machine:
        #print(services.tag, services.attrib)
        service = services.tag
        worker = services.attrib['worker']
        status = services.attrib['status']
        try:
            preferred = services.attrib['preferred']
        except:
            preferred = ""

        row = [now, name, external, service, worker, status, preferred]
        rows.append(row)

system_status = pd.DataFrame(rows, columns=column_names)
