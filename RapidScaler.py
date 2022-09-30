#Full Process Workflow

#Work in Progress!!!!! This is the list of elements and their status.
#
#1. Get XML Status Page- Complete
#2. Parse XML Status, write to PG DB- Complete
#3. Get VizQL Status- Complete
#4. Determin if VizQL needs to scale- In Progress
#5. Get Backgrounder Status- In Progress
#6. Determin if Backgrounder needs to scale- In Progress
#7. Execute VM Start/Terminate Commands- In Progress

#-----------requirements---------#
import requests
import tableauserverclient as TSC
from tableauserverclient import TableauAuth
import xml.etree.ElementTree as ET
import pandas as pd
from datetime import datetime as dt
import psycopg2

#-----------  Config -----------#

#Parameters for Geting Status xml. Admin account is needed.
BaseURL='https://tableau.example.com'
USERNAME = ""
PASSWORD = ""
FILE = 'systeminfo.xml'

# Repository DB Conn Config
repository = "RepositoryURL.exammple.com or IP Adress"
secert = ""


#VizQL Scaler Config
user_to_instance = 75
threshold = 90
wait_up = 0
wait_down = 0


#-----------Functions-----------#
#Create Tableau Server Auth Session
def create_tableau_connection(username, password):
    tableau_auth = TableauAuth(username, password)
    server = TSC.Server(BaseURL)
    server.add_http_options(options_dict={'verify': False})
    server.version = '3.11'
    return server, tableau_auth

#Get XML Status File for Tableau Server
def getxml(BaseURL, USERNAME, PASSWORD, FILE):
    server, tableau_auth = create_tableau_connection(USERNAME, PASSWORD)
    with server.auth.sign_in(tableau_auth):
        URL = BaseURL+"/admin/systeminfo.xml"
        response = requests.get(URL, verify=False)
        with open(FILE, 'wb') as file:
            file.write(response.content)

#Parse the status file and convert it to a dataframe
def parsexml(FILE):
    column_names = ["created", "machine_name", "external", "service", "worker", "status", "preferred"]
    rows =[]
    now = dt.now()

    mytree = ET.parse(FILE)
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

    return system_status

#get the vizql usage and save it as a dataframe
def getVizUsage(repository, secert):

  # Connect to your postgres DB
  conn = psycopg2.connect(dbname = "workgroup", user = "readonly", password = secret, host = repository, port = "8060")

  # Open a cursor to perform database operations
  cur = conn.cursor()

  # VizQL Query
  Query = "SELECT     date(created_at),     date_part('hour',created_at) as hour,     floor(date_part('minute',created_at)/15) as minute,     Min(created_at),     Max(Created_at),     Count(distinct Hist_Actor_User_ID) as users,     Count(distinct worker) as nodes From     Historical_Events Where     Hist_Actor_User_ID is not null     and worker is not null     and Created_At >= NOW() - INTERVAL '1 HOURS' group by     date,     hour,     minute;"

  # Execute a query
  cur.execute(Query)

  # Retrieve query results
  data = cur.fetchall()
  column_names = [desc[0] for desc in cur.description]

  viz_status = pd.DataFrame(data, columns=column_names)

  return viz_status

def scaleVizQL(system_status, viz_status):
    #Work in progress- Create function to count the viz instances currently ON
    activeVizql = system_status[(system_status['service']=='vizqlserver') & (system_status['status']=='Active')]
    vizcount = len(activeVizql)
    #Create Function to determine the number of viz processes needed
      # num of users in viz_status / user to intsance variable gets the needed instance count. 
      #determin server to to viz count and number of viz servers on vs available
    #Determine if the server count should Change
      #if needed is greater than current in any of the last 4, scale up, if it equal in any of last 4 do nothing, if less than in all 4 scale down
      #specify the nuber of servers that should be powered on 
      
#-----------RUN-----------#

getxml(BaseURL, USERNAME, PASSWORD, File)

system_status = parsexml(FILE)

viz_status = getVizUsage(repository, secert)
