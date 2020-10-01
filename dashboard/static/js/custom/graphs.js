
function graph()
{
	 // myNewChart.destroy();
	 var XAxisList = [];
	 var TotalLeadList = [];
	 var NewLeadList = [];
	 var FolloUpLeadList = [];
	 var CompletedLeadList = [];
	 var NonProspectLeadlist = [];

	 $.ajax({
	  type:"POST",
	  url:"../chartajax/",
	  data:$('#filtergraph').serialize(),
	  success: function(msg){
	  	// var json = $.parseJSON(msg);
	    // console.log(msg['NewLeadList']);
	
	    XAxisList = msg['XAxisList'];
	    TotalLeadList = msg['TotalLeadList'];
	    NewLeadList =msg['NewLeadList'];
	    FolloUpLeadList =msg['FolloUpLeadList'];
		CompletedLeadList = msg['CompletedLeadList'];
		NonProspectLeadlist = msg['NonProspectLeadlist'];


    	var lineData = {
    		labels: XAxisList,
    		datasets: [
			{
				label: "NonProspect Lead",
				fillColor: "rgb(244, 66, 83)",
				strokeColor: "rgb(242, 96, 110)",
				pointColor: "rgb(242, 96, 110)",
				pointStrokeColor: "#fff",
				pointHighlightFill: "#fff",
				pointHighlightStroke: "rgba(26,179,148,1)",
				data: NonProspectLeadlist,
			},
    		{
    			label: "Total Leads",
    		    fillColor: "rgb(129, 129, 241)",
    			strokeColor: "rgb(130, 145, 242)",
    			pointColor: "rgb(130, 145, 242)",
    			pointStrokeColor: "#fff",
    			pointHighlightFill: "#fff",
    			pointHighlightStroke: "rgba(26,179,148,1)",
    			data: TotalLeadList,
    		},
    		{
    			label: "New Lead",
    			fillColor: "rgb(226, 213, 61)",
    			strokeColor: "rgb(226, 215, 81)",
    			pointColor: "rgb(226, 215, 81)",
    			pointStrokeColor: "#fff",
    			pointHighlightFill: "#fff",
    			pointHighlightStroke: "rgba(26,179,148,1)",
    			data: NewLeadList,
    		},
    		{
    			label: "FolloUp Lead",
    			fillColor: "rgb(224, 149, 44)",
    			strokeColor: "rgb(239, 194, 131)",
    			pointColor: "rgb(239, 194, 131)",
    			pointStrokeColor: "#fff",
    			pointHighlightFill: "#fff",
    			pointHighlightStroke: "rgba(26,179,148,1)",
    			data: FolloUpLeadList,
    		},
    		{
    			label: "Completed Lead",
    			fillColor: "rgb(115, 237, 71)",
    			strokeColor: "rgb(140, 226, 108)",
    			pointColor: "rgb(140, 226, 108)",
    			pointStrokeColor: "#fff",
    			pointHighlightFill: "#fff",
    			pointHighlightStroke: "rgba(26,179,148,1)",
    			data: CompletedLeadList,
    		}
    		]
    	};

    	var lineOptions = {
    		scaleShowGridLines: true,
    		scaleGridLineColor: "rgba(0,0,0,.05)",
    		scaleGridLineWidth: 1,
    		bezierCurve: true,
    		bezierCurveTension: 0.4,
    		pointDot: true,
    		pointDotRadius: 4,
    		pointDotStrokeWidth: 1,
    		pointHitDetectionRadius: 20,
    		datasetStroke: true,
    		datasetStrokeWidth: 2,
    		datasetFill: true,
    		responsive: true,
    		multiTooltipTemplate:"<%= value %> <%= datasetLabel %>"
    	};


		$('#lineChart2').hide();
		$('#lineChart2').show();
		var ctx = document.getElementById("lineChart2").getContext("2d");

    	// if($('#vise').val() == "m")
    	// {
    	// 	$('#lineChart').hide();
    	// 	$('#lineChart2').show();
    	// 	$('#lineChart3').hide();
    	// }
    	// else if($('#vise').val() == "y")
    	// {
    	// 	$('#lineChart').hide();
    	// 	$('#lineChart2').hide();
    	// 	$('#lineChart3').show();
    	// 	var ctx = document.getElementById("lineChart3").getContext("2d");
    	// }
    	// else
    	// {
    	// 	$('#lineChart').show();
    	// 	$('#lineChart3').hide();
    	// 	var ctx = document.getElementById("lineChart").getContext("2d");
    	// }

    	// $('#lineChart').show();
    	// var ctx = document.getElementById("lineChart").getContext("2d");
    	var myNewChart = new Chart(ctx).Line(lineData, lineOptions);
	  }
	  
	});

}






graph()
