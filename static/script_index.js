$(document).ready(function(){
				
	var intevalId=null;
				
	function iniciarSesion(){
		if($('#sesionUser').val().length >= 1){
			var nUsuario = document.getElementById('sesionUser').value; 
			$.ajax({
				type: "GET",
				url: "/aleatorio",
				data:{
					"sesionU":nUsuario
				},
				success: function(data) {
					var obj=jQuery.parseJSON(data);
					var resp="<table border='2'><tr><td>Ritmo cardiaco</td><td>"+obj.RR+
					"</td></tr><tr><td>Variabilidad del ritmo cardiaco</td><td>"+obj.HR+"</table>";
					$("#datos").html(resp);
					actualizar(parseInt(obj.RR), parseInt(obj.HR));
				}
			});
			return true;
		}else{
			return false;
		}
	}
				
	var dps = [];
	var dps2 = [];
	var xVal = 0;
	var yVal = 100; 
	var updateInterval = 1000;
	var dataLength = 20;

	var chart = new CanvasJS.Chart("chartContainer", {
		title :{
			text: "SENSOR 1"
		},
		axisY: {
			includeZero: false
		},      
		data: [
			{
				type: "line",
				axisYType: "secondary",
				name: "HR",
				showInLegend: true,
				markerSize: 0,
				yValueFormatString: "$#,###k",
				dataPoints: dps
			},
			{
				type: "line",
				axisYType: "secondary",
				name: "RR",
				showInLegend: true,
				markerSize: 0,
				yValueFormatString: "$#,###k",
				dataPoints: dps2
			}
		]
	});
			
	function actualizar (num,num2) {
		dps2.push({
			x: xVal,
			y: num2
		});
					
		dps.push({
			x: xVal,
			y: num
		});
					
		xVal++;
				
		if (dps.length > dataLength) {
			dps.shift();
		}

		chart.render();
	}
    
	$('#consultar').click(function(){
		$.ajax({
			type: "GET",
			url: "/consultarT",
			success: function(data) {
				$("#mostrardatos").html(data);
			}
		});
	});
				
	$('#consultarsesion').click(function(){
		var nUsuario = document.getElementById('sesionBuscada').value;
		$.ajax({
			type: "GET",
			url: "/consultarS",
			data:{
				"sesionB":nUsuario
			},
			success: function(data) {
				$("#mostrarsesion").html(data);
			}
		});
	});
				
	$('#estadistica').click(function(){
		var nUsuario = document.getElementById('sesionestadistica').value;
		$.ajax({
			type: "GET",
			url: "/estadistica",
			data:{
				"sesionE":nUsuario
			},
			success: function(data) {
				$("#mostrarestadistica").html(data);
			}
		});
	});
	
	$('#centroide').click(function(){
		var nUsuario = document.getElementById('sesioncentroide').value;
		$.ajax({
			type: "GET",
			url: "/centroides",
			data:{
				"sesionC":nUsuario				
			},
			success: function(data) {
				$("#mostrarcentroide").html(data);
			}
		});
	});
			
	$('#iniciar').click(function(){
		if(iniciarSesion()==true){
			intervalId = setInterval(iniciarSesion,2000);	
		}else{
			alert("Digite la sesion:  ");
		}
	});
		
	$('#detener').click(function(){
		clearInterval(intervalId);
	});
});
