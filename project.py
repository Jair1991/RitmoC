from flask import Flask, render_template, request
from handler_ddbb import handler_ddbb
import random
import time

app = Flask(__name__)
man = handler_ddbb()

@app.route("/")
def home():
	titulo = "TOMA DE DATOS"
	return render_template("index.html", titulo = titulo)
	
@app.route("/aleatorio")
def aleatorio():
	HR = random.randint(60,100)
	RR = 60000/HR
	estampa = time.time()*1000
	sesion = str(request.args["sesionU"])
	man.agregar_datos(estampa, RR, HR, sesion)
	return	"{\"HR\":"+str(HR)+",\"RR\":"+str(RR)+"}"

@app.route("/consultarT")
def consultarT():
	return man.consultar_datos()

@app.route("/consultarS")
def consultarS():
	sesion = str(request.args["sesionB"])
	return man.consultar_sesion(sesion)

@app.route("/estadistica")
def estadistica():
	sesion = str(request.args["sesionE"])
	return man.consultar_estadistica(sesion)

@app.route("/centroides")
def centroides():
	sesion = str(request.args["sesionC"])
	return man.consultar_centroide(sesion)

if __name__ == "__main__":
	app.run("0.0.0.0")
