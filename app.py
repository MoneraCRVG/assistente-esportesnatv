import flet as ft
import random

def main(page: ft.Page):
    page.title = "Assistente EsportesNaTV"
    global broadcasters
    broadcasters = ft.Column()

    def acao_drawer(e):
        match drawer.selected_index + 1:
            case 1:
                page.go("/football")
            case 2:
                page.go("/volleyball")
            case 3:
                page.go("/users")
            case 4:
                page.go("/config")
            case 5:
                page.go("/logs")

    drawer = ft.NavigationDrawer(
        on_change=acao_drawer,
        controls=[
            ft.NavigationDrawerDestination(
                label="Futebol",
                icon=ft.icons.SPORTS_SOCCER,
            ),
            ft.NavigationDrawerDestination(
                label="Vôlei",
                icon=ft.icons.SPORTS_VOLLEYBALL
            ),
            ft.NavigationDrawerDestination(
                label="Usuários",
                icon=ft.icons.PERSON
            ),
            ft.NavigationDrawerDestination(
                label="Configurações",
                icon=ft.icons.SETTINGS
            ),
            ft.NavigationDrawerDestination(
                label="Registros",
                icon=ft.icons.LOCK_CLOCK
            )
        ]
    )
    burger = ft.IconButton(icon=ft.icons.MENU, on_click=lambda e: page.open(drawer))
    appbar = ft.AppBar(leading=burger, title=ft.Text("Assistente EsportesNaTV"))

    def submit(e):
        print(
            f'Data: {date_field.value}\nCompetição:{tournament_field.value}\nHorário:{time_field.value}\n{home_team_field.value} x {away_team_field.value}\nEmissoras{broadcaster_list}')
        if form_modes.value != "date":
            date_field.value = ""  # Corrected to use assignment
        if form_modes.value != "tournament":
            tournament_field.value = ""  # Corrected to use assignment
        time_field.value = ""  # This line is not conditional, it's always reset
        if form_modes.value != "home_team":
            home_team_field.value = ""  # Corrected to use assignment
        if form_modes.value != "away_team":
            away_team_field.value = ""  # Corrected to use assignment

        broadcaster_list.clear()

    date_field = ft.TextField(
        label="Data",
        keyboard_type=ft.KeyboardType.DATETIME
    )

    tournament_field = ft.TextField(
        label="UUID da competição",
    )

    home_team_field = ft.TextField(
        label="UUID do time mandante",
    )

    time_field = ft.TextField(
        label="Horário",
        keyboard_type=ft.KeyboardType.DATETIME
    )
    home_team_logo = ft.Image(
        src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR2f_J-lquqYxGe9raI1Do5mFYpk6Q9IMBgVw&s", width=64,
        height=64)
    away_team_logo = ft.Image(src="https://pbs.twimg.com/media/FzRKILrXsAIx82s.png", width=64, height=64)

    away_team_field = ft.TextField(
        label="UUID do time visitante",
    )

    broadcaster_list = []

    def remove_broadcaster(e, broadcaster):
        broadcasters.controls.remove(broadcaster)
        page.update()

    def add_new_broadcaster(e):
        new_broadcaster = ft.Row([
            ft.TextField(autofocus=True),
            ft.ElevatedButton("Remover", on_click=lambda e: remove_broadcaster(e, new_broadcaster))
        ])
        broadcasters.controls.append(new_broadcaster)
        page.update()

    add_broadcaster_button = ft.ElevatedButton("Adicionar novo", on_click=add_new_broadcaster)
    broadcasters_field = ft.Column([ft.Text("Emissoras"), broadcasters, add_broadcaster_button])
    # region
    form_modes = ft.RadioGroup(
        content=ft.Row(
            [ft.Column([
                ft.Text("Cadastrar jogos por: "),
                ft.Radio(value="date", label="Data"),
                ft.Radio(value="tournament", label="Competição"),
                ft.Radio(value="home_team", label="Time mandante")

            ]),
                ft.Column([
                    ft.Row([
                        date_field,
                        time_field
                    ]),
                    tournament_field,
                ])
            ]
        )
    )

    # endregion

    def navigation(router):
        page.views.clear()
        if page.route == "/football":
            page.views.append(
                ft.View(
                    "/football",
                    [
                        ft.AppBar(title=ft.Text('Futebol')),
                        form_modes,
                        ft.Row([
                            home_team_logo,
                            home_team_field,
                            away_team_field,
                            away_team_logo
                        ]),
                        broadcasters_field,
                        ft.ElevatedButton(text="Enviar", on_click=submit)
                    ],
                    appbar=appbar,
                    drawer=drawer,
                )
            )
        if page.route == "/volleyball":
            page.views.append(
                ft.View(
                    "/volleyball",
                    [
                        ft.AppBar(title=ft.Text('Vôlei')),

                        form_modes,
                        ft.Row([

                            home_team_logo,
                            home_team_field,
                            away_team_field,
                            away_team_logo
                        ]),
                        broadcasters_field,
                    ],
                    appbar=appbar,
                    drawer=drawer,
                )
            )
        if page.route == "/users":
            page.views.append(
                ft.View(
                    "/users",
                    [
                        ft.AppBar(title=ft.Text('Usuários')),
                        ft.Row([
                            ft.Column([
                                ft.Text("Banco de dados", style=ft.TextDecoration.UNDERLINE),
                                ft.ListView(
                                    controls=[
                                        ft.Text("Eu"),
                                        ft.Text("DBO")
                                    ]
                                )
                            ]),
                            ft.Column([
                                ft.Text("Servidor", style=ft.TextDecoration.UNDERLINE),
                                ft.ListView(
                                    controls=[
                                        ft.Text("Eu"),
                                        ft.Text("root"),
                                        ft.Text("Gerente")
                                    ]
                                )
                            ])

                        ],
                        expand=True)
                    ],
                    appbar=appbar,
                    drawer=drawer
                )
            )
        if page.route == "/config":
            page.views.append(
                ft.View(
                    "/config",
                    [
                        ft.AppBar(title=ft.Text("Configurações")),
                        ft.ElevatedButton("Reiniciar servidor"),
                        ft.ElevatedButton("Fazer deploy"),
                        ft.ElevatedButton("Atualizar as partidas do dia"),
                        ft.ElevatedButton("Fazer Backup")
                    ],
                    appbar=appbar,
                    drawer=drawer,
                )
            )
        if page.route == "/logs":
            page.views.append(
                ft.View(
                    "/logs",
                    [
                        ft.AppBar(title=ft.Text("Registros")),
                        ft.Row([
                            ft.Column([
                                ft.Text("Logs do servidor"),
                                ft.ListView([
                                    ft.Text("00:03 Servidor rust iniciado"),
                                    ft.Text("00:02 Servidor next.js iniciado"),
                                    ft.Text("00:01 Banco de dados iniciado")
                                ])
                            ], expand=True),  # Ensure this column can expand
                            ft.Column([
                                ft.Text("Logs do banco de dados"),
                                ft.ListView([
                                    ft.Text("00:03 SELECT...[nicolas]"),
                                    ft.Text("00:02 GRANT PRIVILEGES...[root]"),
                                    ft.Text("00:01 ALTER SCHEMA...[nicolas]")
                                ])
                            ], expand=True),
                            ft.Column([
                                ft.Text(f"Usuários conectados simultaneamente: {random.randint(0,3000)}"),
                                ft.Text("Problemas reportados pelos usuários:"),
                                ft.ListView([
                                    ft.Text("Partida River Plate x Barcelona sem emissoras"),
                                    ft.Text("Não encontra o jogo do flamengo"),
                                    ft.Text("A ESPN não transmite o jogo do Inter Miami"),
                                    ft.Text("Horário errado pro jogo do Al Nassr e Al Hilal")
                                ])
                            ], expand=True)
                        ], expand=True)
                    ],
                    appbar=appbar,
                    drawer=drawer,
                )
            )
        page.update()

    page.on_route_change = navigation
    page.go("/football")


ft.app(main)
