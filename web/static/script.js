//реагирование на изменение выбранного типа отчёта
function update_report_selector()
{
	var active_option = document.getElementById("select-report").value;
	console.log('Select '+ active_option + 'in report selector');
	if (active_option == 'country_category' || active_option == 'daypart_category')
	{
		document.getElementById('select-category').hidden = false;
	}
	else
	{
		document.getElementById('select-category').hidden = true;
	}
}

//отчистка визуализации отчёта
function destroy_repprt()
{
	document.getElementById('chart').innerHTML = '';
}

//запрос к серверу
function do_query()
{
	var active_option = document.getElementById("select-report").value;
	switch (active_option)
	{
		case 'events_per_country':
			events_per_country();
			break;
		case 'country_category':
			var category = document.getElementById("select-category").value;
			country_category(category);
			break;
		case 'daypart_category':
			var category = document.getElementById("select-category").value;
			daypart_category(category);
			break;
					
	}
}

//запрос на отчёт по действиям по странам
function events_per_country()
{
	var xhr = new XMLHttpRequest();
    xhr.open('GET', 'events_per_country');
    xhr.send();
    xhr.onreadystatechange = function () 
    {
    	 if(xhr.responseText !== '')
    	 {
    	 	var serverResponse = JSON.parse(xhr.responseText);
		    google.charts.load("current", {packages:["corechart"]});
		    google.charts.setOnLoadCallback(function()
		    {
		    	var max = 0;
		        var data = [["", ""]];
		        for (var i = serverResponse.length-1; i>=0; i--)
		        {
		        	if (serverResponse[i]['country']!='another')
		        	{
		        		if (max < serverResponse[i]['count'])
		        		{
		        			max = serverResponse[i]['count'];
		        		}
		        		data.push([serverResponse[i]['country'], serverResponse[i]['count']]);
		        	}
		        }
		        var dataTable = google.visualization.arrayToDataTable(data);
		        var options = {
		            title          : "",
		            chartArea      : {left: '5%', top: '5%', width: '95%'},
		            backgroundColor: 'transparent',
		            bar            : {groupWidth: "95%"},
		            legend: { position: 'none' },
		            colors : ['#00ccff'],
		            histogram: { lastBucketPercentile: 5 },
		    		vAxis: { scaleType: 'mirrorLog',
		    		minValue: 0,
		            maxValue: max },

		        };
		        var chart   = new google.visualization.ColumnChart(document.getElementById('chart'));
		        chart.draw(dataTable, options);
		       
		    });
		}

    }
}

//запрос на отчёт по распределению интересющихся данной катеогрией по странам
function country_category(category)
{
	var xhr = new XMLHttpRequest();
    xhr.open('POST', 'country_category');
    xhr.send(category);
    xhr.onreadystatechange = function () {
    	if (xhr.responseText !== '')
    	{
    		var serverResponse = JSON.parse(xhr.responseText);
		    google.charts.load("current", {packages:["corechart"]});
		    google.charts.setOnLoadCallback(function()
		    {
		    	var max = 0;
		        var data = [["", ""]];
		        for (var i = serverResponse.length-1; i>=0; i--)
		        {
		        	if (serverResponse[i]['country']!='another')
		        	{
		        		if (max < serverResponse[i]['count'])
		        		{
		        			max = serverResponse[i]['count'];
		        		}
		        		data.push([serverResponse[i]['country'], serverResponse[i]['count']]);
		        	}
		        }
		        var dataTable = google.visualization.arrayToDataTable(data);
		        var options = {
		            title          : "",
		            chartArea      : {left: '5%', top: '5%', width: '95%'},
		            backgroundColor: 'transparent',
		            bar            : {groupWidth: "95%"},
		            legend: { position: 'none' },
		            colors : ['#6600ff'],
		            histogram: { lastBucketPercentile: 5 },
		    		vAxis: { scaleType: 'mirrorLog',
		    		minValue: 0,
		            maxValue: max },

		        };
		        var chart   = new google.visualization.ColumnChart(document.getElementById('chart'));
		        chart.draw(dataTable, options);
		       
		    });
    	}
    }
}

//запрос на отчёт по интересу пользователей в определенный период дня
function daypart_category(category)
{
	var xhr = new XMLHttpRequest();
    xhr.open('POST', 'daypart_category');
    xhr.send(category);
    xhr.onreadystatechange = function () 
    {
    	if (xhr.responseText !== '')
    	{
    		console.log(xhr.responseText);
    		var serverResponse = JSON.parse(xhr.responseText);
		    google.charts.load("current", {packages:["corechart"]});
		    google.charts.setOnLoadCallback(function()
		    {
		    	var data = [["", ""]];
		        for (var i = serverResponse.length-1; i>=0; i--)
		        {
		        	data.push([serverResponse[i]['daypart'], serverResponse[i]['count']]);
		        }
		        var dataTable = google.visualization.arrayToDataTable(data);
		        var options = {
				   
				    pieHole: 0.6,
				    slices: {
				        0: { color: '#000066' },
				        1: { color: '#009999' },
				        2: { color: '#00ccff' },
				        3: { color: '#6600ff' }
				    }
				};
		        var chart   = new google.visualization.PieChart(document.getElementById('chart'));
		        chart.draw(dataTable, options);
		    });
    	}
    }
}