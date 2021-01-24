from tinydb import TinyDB, where
import numpy as np
from sklearn.cluster import KMeans

class handler_ddbb:
	
	def agregar_datos(self, estampa, FC, VFC, sesion):
		db = TinyDB("ddbb.json")
		db.insert({"estampa":estampa, "FC":FC, "VFC":VFC, "sesion":sesion})
	
	def consultar_datos(self):
		db = TinyDB("ddbb.json")
		lista = db.all()
		
		cad = "<table border='2'>"
		for elem in lista:
			cad = cad + "<tr><td>Estampa</td><td>" + str(elem["estampa"]) + "</td></tr>"
			cad = cad + "<tr><td>FC</td><td>" + str(elem["FC"]) + "</td></tr>"
			cad = cad + "<tr><td>VFC</td><td>" + str(elem["VFC"]) + "</td></tr>"
			cad = cad + "<tr><td>Sesion</td><td>" + str(elem["sesion"]) + "</td></tr>"
		cad = cad+"</table>"
		return cad
	
	def consultar_sesion(self, sesion):
		db = TinyDB("ddbb.json")
		lista = db.search(where("sesion") == sesion)
		hr = 0
		rr = 0
		con = 0
		
		cad = "<table border='2'>"
		for elem in lista:
			cad = cad + "<tr><td>Estampa</td><td>" + str(elem["estampa"]) + "</td></tr>"
			cad = cad + "<tr><td>FC</td><td>" + str(elem["FC"]) + "</td></tr>"
			cad = cad + "<tr><td>VFC</td><td>" + str(elem["VFC"]) + "</td></tr>"
			cad = cad + "<tr><td>Sesion</td><td>" + str(elem["sesion"]) + "</td></tr>"
			cad = cad + "<tr><td> </td><td>" "</td></tr>"
			hr = hr + elem["FC"]
			rr = rr + elem["VFC"]
			con = con + 1
		
		cad = cad + "<tr><td>Promedio FC</td><td>" + str(hr/con)+ "</td></tr>"
		cad = cad + "<tr><td>Promedio VFC</td><td>" + str(rr/con)+ "</td></tr>"
		cad = cad + "<tr><td>Cantidad de datos</td><td>" + str(con)+ "</td></tr>"
		cad = cad + "</table>"
		return cad
		
	def consultar_estadistica(self, sesion):
		db = TinyDB("ddbb.json")
		lista = db.search(where("sesion") == sesion)
		cad = "<table border='2'>"
		hr = 0
		rr = 0
		con = 0
		maximoHr = 0
		minimoHr = 1000
		maximoRr = 0
		minimoRr = 1000
		estado = ""
		
		for elem in lista:
			FC = eval(elem["FC"])
			VFC = eval(elem["VFC"])			
			hr = hr + FC
			rr = rr + VFC
			con = con + 1
			if maximoHr<FC:
				maximoHr = FC
				
			if minimoHr>FC:
				minimoHr = FC
				
			if maximoRr<VFC:
				maximoRr = VFC
				
			if minimoRr>VFC:
				minimoRr = VFC
			
		if (hr/con)<750:
				estado = "Alto"
				
		if (hr/con)>900:
				estado = "Bajo"
				
		if ((hr/con)>750 and (hr/con)<900):
				etsado = "Moderado" 	
		
		cad = cad + "<tr><td>Sesion</td><td>" + sesion + "</td></tr>"
		cad = cad + "<tr><td> </td><td>" "</td></tr>"
		cad = cad + "<tr><td>promedio ritmo cardiaco</td><td>" + str(hr/con) + "</td></tr>"
		cad = cad + "<tr><td>promedio variabilidad ritmo cardiaco</td><td>" + str(rr/con) + "</td></tr>"
		cad = cad + "<tr><td>Hr+</td><td>" + str(maximoHr) + "</td></tr>"
		cad = cad + "<tr><td>Hr-</td><td>" + str(minimoHr) + "</td></tr>"
		cad = cad + "<tr><td>Rr+</td><td>" + str(maximoRr) + "</td></tr>"
		cad = cad + "<tr><td>Rr-</td><td>" + str(minimoRr) + "</td></tr>"
		cad = cad + "<tr><td>AvRRInterval</td><td>" + estado + "</td></tr>"
		cad = cad + "<tr><td>Cantidad de datos</td><td>" + str(con) + "</td></tr>"
		
		auxHr = []
		auxRr = []
		estado = ""
		
		for elem in lista:
			FC = eval(elem["FC"])
			VFC = eval(elem["VFC"])
			auxHr.append([FC])
			auxRr.append([VFC])
			if VFC < 25:
				estado = "Alto"
			if VFC > 40:
				estado = "Bajo"
			if (VFC>25 and VFC<40):
				estado = "Moderado"
		
		cad = cad + "<tr><td>Hr</td><td>" + str(np.std(auxHr)) + "</td></tr>"
		cad = cad + "<tr><td>Rr(SDRR)</td><td>" + str(np.std(auxRr)) + "</td></tr>"
		cad = cad + "<tr><td>SDRR</td><td>" + estado + "</td></tr>"
	
		cont = 0
		pr50 = 0.0
		nex = 0
		estado = ""
		
		for elem in lista:
			VFC = eval(elem["VFC"])
			if (abs(int(VFC) - nex ) > 50):
				cont = cont+1
			nex = int(VFC)
		
		pr50 = float(cont) /float(len(lista))*100
		
		if pr50 < 3:
			estado = "Alto"
		else:
			estado = "Bajo"
			
		cad = cad + "<tr><td>pRR50</td><td>" + str(pr50) + "</td><td>" + estado + "</td></tr>"
		cad = cad + "<tr><td>Numero de Intervalos </td><td>" + str(cont) + "</td></tr></table>"

		return cad

	def consultar_centroide(self, sesion):
		db = TinyDB("ddbb.json")
		lista = db.search(where("sesion") == sesion)
		aux = []
		
		for elem in lista:
			aux.append([elem["FC"], elem["VFC"]])
		
		kmeans = KMeans(n_clusters=2)
		kmeans.fit(aux)
		centroides=kmeans.cluster_centers_
			
		cad = "<table border='2'"
		cad = cad + "<tr><td><center>X</center></td><td><center>Y</center></td></tr>"
		
		for cen in centroides:
			cad = cad + "<tr><td>" + str(cen[0]) + "</td><td>" + str(cen[1]) + "</td></tr>"
		
		cad = cad + "</table>"
		
		return cad
