#Checks the current user status of the vizql servers

import psycopg2

def getVizUsage(): 
  # DB Conn Config
  server = "RepositoryURL.exammple.com"
  secert = ""

  # Connect to your postgres DB
  conn = psycopg2.connect(dbname = "workgroup", user = "readonly", password = secret, host = server, port = "8060")

  # Open a cursor to perform database operations
  cur = conn.cursor()

  # VizQL Query
  Query = "SELECT     date(created_at),     date_part('hour',created_at) as hour,     floor(date_part('minute',created_at)/15) as minute,     Min(created_at),     Max(Created_at),     Count(distinct Hist_Actor_User_ID) as users,     Count(distinct worker) as nodes From     Historical_Events Where     Hist_Actor_User_ID is not null     and worker is not null     and Created_At >= NOW() - INTERVAL '24 HOURS' group by     date,     hour,     minute;"

  # Execute a query
  cur.execute(Query)

  # Retrieve query results
  data = cur.fetchall()
  column_names = [desc[0] for desc in cur.description]

  viz_status = pd.DataFrame(data, columns=column_names)
  
  return viz_status
