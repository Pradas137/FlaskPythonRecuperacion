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
                DiccL[Local][Visitante] = "G"
            else:
                DiccL[Local][Visitante] = ""
    return DiccL


def CrearRanking():
    rankingD = {}
    for Local in Equipos:
        rankingD[Local] = 0
    return rankingD

def PuntosRanking(Local, Visitante):
    """Check how many points did the local team win."""
    if Local != "":
        if Local > Visitante:
            return 3
        elif Local == Visitante:
            return 1
        else:
            return 0
    else:
        return 0

def ModificacionLiga(Local, Visitante, GolesL, GolesV):
    liga[Local][Visitante] = GolesL
    liga[Visitante][Local] = GolesV


Equipos = file()
liga = CrearLiga()
Ranking = CrearRanking()


@app.route('/')
def Menu():
    return render_template("Menu.html")


@ app.route('/Ligas')
def Ligas():
    return render_template("Ligas.html", liga=liga, Equipos=Equipos)


@ app.route('/Equipos')
def ListaEquipos():
    return render_template("Equipos.html", Equipos=Equipos)

@app.route('/Ranking')
def TablaRanking():
    #update_ranking()
    return render_template("Ranking.html", Ranking=sorted(Ranking.items(), key=lambda x: x[1], reverse=True))

@app.route('/Equipos', methods=["POST"])
def GolesPost():
    Local = request.form["Local"]
    Visitante = request.form["Visitante"]
    GolesL = request.form["GolesL"]
    GolesV = request.form["GolesV"]
    if Local == Visitante:
        return GolesPost("sameTeams")
    else:
        ModificacionLiga(Local, Visitante, GolesL, GolesV)
        return redirect(url_for("Ligas"))


if __name__ == '__main__':
    app.run()
