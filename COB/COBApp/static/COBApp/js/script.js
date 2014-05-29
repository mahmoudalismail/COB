
// Load the Visualization API and the piechart package.
google.load('visualization', '1.0', {'packages':['corechart']});

// Set a callback to run when the Google Visualization API is loaded.
google.setOnLoadCallback(plotGraph);

//list contains all the categories that we need
var categories = ["Avaliable Budget","Printing banners, booklets, roll ups", 
					"Supplies for events", "Giveaways", "Prizes", "Food, snacks, drinks",
					"Transportation", "Entrance Fees", "Rental Fee (bouncy castles, tents, other equipment)", 
					"Professional Fees (organizational dues)", 
					"Non-capital equipment (camera, rechargeable batteries, portable printer)"]

// Callback that creates and populates a data table, 
// instantiates the pie chart, passes in the data and
// draws it.

function plotGraph () {

	// Create the data table.
	var dataForGraph = new google.visualization.DataTable();
	
	// values is outside the AJAX request because 
	// it will be used later
	var values = new Array();
	
	// name of the club is fetch from the page, it's in a hidden div
	$.getJSON('/COBApp/getSpending/'+$('#clubID').html()+'/', null, function(data){
		console.log(data)
		$.each(data, function(i) {
			values.push([categories[i], data[i+1]])        
        })

	// all of the below happen inside the AJAX request because
	// of concurrency issues

	
	dataForGraph.addColumn('string', 'Category');
	dataForGraph.addColumn('number', 'Expenses');
	dataForGraph.addRows(values)
	
	// Set chart options
	var options = {'title':'The '+data[0]+'s Spending',
	             'width': 600,
	             'height': 300};

	// Instantiate and draw our chart, passing in some options.
	var chart = new google.visualization.PieChart(document.getElementById('chart_div'));
	chart.draw(dataForGraph, options);

  	}, "json");
};