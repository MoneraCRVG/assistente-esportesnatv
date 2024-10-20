import mysql.connector

conn = mysql.connector.connect(host='esportesnatv.com.br', user='nvmonera', password='115E9077A6AC68584FF7096FE4E7498C')

cursor = conn.cursor()
teste = int(input())
cursor.execute(f"INSERT INTO football.event_broadcasters (broadcasters_broadcaster_id, events_event_id) VALUES (1,%s)", (teste,))

conn.commit()

cursor.close()
conn.close()