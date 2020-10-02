from flask import Flask, request, redirect, url_for, render_template
app = Flask(__name__)


def file():
    Lista = []
    archivo = open("equips.cfg", "r")
    for equip in archivo:
        Lista.append(equip.rstrip("\n"))
    return Lista


def CrearLiga():
    DiccL = {}
    for Local in Equipos:
        DiccL[Local] = {}
        for Visitante in Equipos:
            if Visitante == Local:
                DiccL[Local][Visitante] = "X"
            else:
                DiccL[Local][Visitante] = ""
    return DiccL


def CrearRanking():
    rankingD = {}
    for Local in Equipos:
        rankingD[Local] = 0
    return rankingD


def ModificacionLiga(Local, Visitante, GolesL, GolesV):
    liga[Local][Visitante] = GolesL
    liga[Visitante][Local] = GolesV


def ModificacionRanking():
    global ranking
    ranking = CrearRanking()
    equipos = []
    for Local in liga:
        for Visitante in liga[Local]:
            if liga[Local][Visitante] != "":
                if Local and Visitante not in equipos and Local != Visitante:
                    puntos = check_ranking_points(
                        liga[Local][Visitante], liga[Visitante][Local])
                    set_ranking_points(puntos, Local, Visitante)
        equipos.append(Local)


def check_ranking_points(Local, Visitante):
    if Local != "":
        if Local > Visitante:
            return Local
        elif Local == Visitante:
            return 1
        else:
            return 0
    else:
        return 0


def set_ranking_points(puntos, Local, Visitante):
    if puntos == 3:
        ranking[Local] += puntos
    elif puntos == 1:
        ranking[Local] += puntos
        ranking[Visitante] += puntos
    else:
        ranking[Local] += puntos
        ranking[Visitante] += 3


Equipos = file()
liga = CrearLiga()
ranking = CrearRanking()


@app.route('/')
def Menu():
    return render_template("Menu.html")


@ app.route('/Ligas')
def Ligas():
    return render_template("Ligas.html", liga=liga, Equipos=Equipos)


@ app.route('/Equipos')
def ListaEquipos():
    return render_template("Equipos.html", Equipos=Equipos)


@app.route('/Goles')
def Goles(error=None):
    return render_template("Goles.html", Equipos=Equipos, error=error)


@app.route('/ranking')
def Ranking(error=None):
    ModificacionRanking()
    return render_template("Ranking.html", ranking=sorted(ranking.items(), key=lambda x: x[1], reverse=True))


@app.route('/Goles', methods=["POST"])
def goals_input_post():
    Local = request.form["localTeam"]
    Visitante = request.form["visitantTeam"]
    GolesL = request.form["localTeamScore"]
    GolesV = request.form["visitantTeamScore"]
    if Local == Visitante:
        return goals_input("sameTeams")
    else:
        ModificacionLiga(Local, Visitante, GolesL, GolesV)
        return redirect(url_for("Ligas"))


if __name__ == '__main__':
    app.run()