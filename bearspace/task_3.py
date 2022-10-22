import pandas as pd
import psycopg2
from sqlalchemy import create_engine

conn_string = "postgresql://user:password@localhost:5432/heni"

db = create_engine(conn_string)
conn = db.connect()

for filename in ["airlines", "airports", "airlines", "flights", "weather"]:
    with open(f"data/{filename}.csv") as f:
        df = pd.read_csv(f)
        df.to_sql(filename, con=conn, if_exists="replace", index=False)

conn = psycopg2.connect(conn_string)
conn.autocommit = True
cursor = conn.cursor()

conn.close()

"""
select arr_time, origin, dest, airlines.name
from flights join airlines on flights.carrier = airlines.carrier

select * 
from flights join airlines on flights.carrier = airlines.carrier
where airlines.name like '%JetBlue%'

select origin, sum(flight)
from flights
group by origin
order by sum(flight) asc

select origin, sum(flight) as numFlights
from flights
group by flights.origin
having sum(flight) > 10000

"""
