import mysql.connector
import os
import random

def execute_query(cursor, query, params=None):
    try:
        cursor.execute(query, params)
        return cursor.fetchall()
    except Exception as e:
        print(f"Error executing query: {e}")
        return []

def get_data_from_table(cursor, table, fields):
    query = f"SELECT {', '.join(fields)} FROM {table}"
    return execute_query(cursor, query)

def get_id_by_uuid(cursor, table, uuid_field, uuid_value, id_field):
    query = f"SELECT {id_field} FROM {table} WHERE {uuid_field} = %s"
    result = execute_query(cursor, query, (uuid_value,))
    return result[0][0] if result else None

def get_broadcasters_id(cursor, broadcasters_uuid):
    broadcasters_list = [item.strip() for item in broadcasters_uuid.split(",")]
    broadcasters_id = []
    for uuid in broadcasters_list:
        broadcaster_id = get_id_by_uuid(cursor, 'assets.broadcasters', 'broadcaster_uuid', uuid, 'broadcaster_id')
        if broadcaster_id:
            broadcasters_id.append(broadcaster_id)
    return broadcasters_id

def insert_event(cursor, date, event_uuid, time, venue, status, tournament_stage, tournament_id, home_team_id, away_team_id):
    sql_query = """
        INSERT INTO football.events (date, event_uuid, time, venue, status, tournament_stage, tournaments_tournament_id, home_team_id, away_team_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(sql_query, (date, event_uuid, time, venue, status, tournament_stage, tournament_id, home_team_id, away_team_id))

def insert_event_broadcasters(cursor, event_id, broadcasters_id):
    sql_query = "INSERT INTO football.event_broadcasters (events_event_id, broadcasters_broadcaster_id) VALUES (%s, %s)"
    for broadcaster_id in broadcasters_id:
        cursor.execute(sql_query, (event_id, broadcaster_id))

def football_form(conn, cursor, date=None, tournament=None, team=None):
    tournaments = get_data_from_table(cursor, 'football.tournaments', ['name', 'tournament_id'])
    teams = get_data_from_table(cursor, 'football.teams', ['name', 'team_uuid', 'team_id'])

    while True:
        if not date or not team:
            date = input("Data: ")

        time = input("Horário: ")
        venue = input("Estádio: ")
        status = 'upcoming'
        tournament_stage = input("Fase da competição: ")
        if not tournament:
            tournament = input("UUID da competição: ")
        home_team_uuid = input("UUID do time mandante: ") if not team else team
        away_team_uuid = input("UUID do time visitante: ")
        broadcasters_uuid = input("UUID das emissoras: ")

        tournament_id = get_id_by_uuid(cursor, 'football.tournaments', 'tournament_uuid', tournament, 'tournament_id')
        home_team_id = get_id_by_uuid(cursor, 'football.teams', 'team_uuid', home_team_uuid, 'team_id')
        away_team_id = get_id_by_uuid(cursor, 'football.teams', 'team_uuid', away_team_uuid, 'team_id')
        broadcasters_id = get_broadcasters_id(cursor, broadcasters_uuid)

        event_uuid = f"{home_team_uuid}-x-{away_team_uuid}-{random.randint(0, 99999)}"

        try:
            insert_event(cursor, date, event_uuid, time, venue, status, tournament_stage, tournament_id, home_team_id, away_team_id)
            conn.commit()

            event_id = get_id_by_uuid(cursor, 'football.events', 'event_uuid', event_uuid, 'event_id')
            insert_event_broadcasters(cursor, event_id, broadcasters_id)

            conn.commit()
        except Exception as e:
            print(f"Error: {e}")
        
        os.system("cls")

def main():
    conn = mysql.connector.connect(host='esportesnatv.com.br', user='nvmonera', password='115E9077A6AC68584FF7096FE4E7498C')
    cursor = conn.cursor()

    def escolher_esporte(date=None, tournament=None, team=None):
        sport = input("Digite o nome do esporte (schema): ")
        if sport == 'football':
            football_form(conn, cursor, date=date, tournament=tournament, team=team)
        else:
            print("Esporte inválido!")

    modos = ['Adicionar por data', 'Adicionar por campeonato', 'Adicionar por clube mandante']
    for index, item in enumerate(modos):
        print(f"{index+1}. {item}")
    modo = int(input("Escolha um modo: "))

    match modo:
        case 1:
            data = input("Digite a data: ")
            escolher_esporte(date=data)
        case 2:
            campeonato = input("Digite o UUID do campeonato: ")
            escolher_esporte(tournament=campeonato)
        case 3:
            clube = input("Digite o UUID do clube: ")
            escolher_esporte(team=clube)
        case _:
            raise ValueError("Opção inválida!")

    cursor.close()
    conn.close()

if __name__ == '__main__':
    main()
