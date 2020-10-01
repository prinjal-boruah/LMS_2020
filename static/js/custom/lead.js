var sid = "";

//  Alert box
toastr.options = {
    "closeButton": true,
    "debug": false,
    "progressBar": true,
    "positionClass": "toast-top-right",
    "onclick": null,
    "showDuration": "400",
    "hideDuration": "1000",
    "timeOut": "10000",
    "extendedTimeOut": "1000",
    "showEasing": "swing",
    "hideEasing": "linear",
    "showMethod": "fadeIn",
    "hideMethod": "fadeOut"
};


// Lead Table

var oTable = '';
jQuery(document).ready(function() {
    
    oTable = jQuery('#leadtable').dataTable({

      "ajax": {
       "url": '../',
       "type": 'POST',
       "data": function(d,start){

            return  $('#filter').serialize() + "&start=" + d.start + "&length=" + d.length + "&search=" + d.search.value + "&orderCol=" + d.order[0].column + "&orderDir=" + d.order[0].dir;
         }
     },
     "columnDefs":[{"targets":[3,4,5],"sortable":false}],
     "order":[[1,"desc"]],
     "bDeferRender": true,
     "pagingType": "full_numbers",
     "responsive": true,
     "processing": true,
     "searching": true,
     "serverSide": true,
    //  "dom": 'T<"clear">lfrtip',
     "tableTools": {
      "sSwfPath": "{% static '/js/plugins/dataTables/swf/copy_csv_xls_pdf.swf'%}"
    }
  });
  });

function reportfilter()
{
    oTable.api().ajax.reload();
}


var leadid = 0 // leadid for refrence

// edit option
function edit(id)
{
  leadid = id

  $.ajax({
        type:"GET",
        url:"/leadEdit/",
        data:"id="+id,
        success: function(msg){
            $('#formedit').html(msg),
            $('#filters').hide();
            $('#table').hide();
            $('.formtype').show();
        }

  });

}


// back or save lead
$('#Back_button').click(function(){

    if ($('#telephone_sid').val() == ""){
      location.reload();
    }
    else{
      toastr['warning']("Please select Save the lead after calling");
    }
});




$('#Save_button').click(function(){

  if($('#CallStatusSelect').val() ==""){
    toastr['warning']("Please select Call Status");
  }

  else if($('#leadStatusSelect').val() == "0"){
    toastr['warning']("Please select Lead Status");
  }

  else{  
  
    // console.log( $('#leadEditForm').serialize() +"&"+ $('#leadStatusForm').serialize() +"&sid=" + $('#telephone_sid').val());
    $.ajax({
         type:"POST",
         url:"/leadEdit/",
         data: $('#leadEditForm').serialize() +"&"+ $('#leadStatusForm').serialize() +"&sid=" + $('#telephone_sid').val(),
         success: function(msg11){
          toastr['success']("Lead Saved Successfully");
          //  sleep(5000);
          location.reload();
         }
    });
  }

});






function calling(id)
{

  if (sid == ""){
    // phone validation
    if ($('#visitor_phone_nu').val() != ""){
      $.ajax({
          type:"POST",
          url:"/telephone/call/",
          data: "phoneid=" +  $('#visitor_phone_nu').val() + "&leadid=" + id,
          success: function(msg){
            // msg = JSON.parse(msg11);
            if(msg.LMSstatus == 1){
              callflag = 1; // Telephone Status updation
              toastr['success'](msg.additional);
              $('#telephone_sid').val(msg.message);
              sid = msg.message;

            }
            else{
              toastr['error'](msg.additional);
              $('#telephone_sid').val('0'); // for identifcation porposse

            }
          }
      });
    }
    else{
      toastr['warning']("Please select Phone Number");
    }

  }
  else{
    toastr['warning']('Sorry muiltiple call per lead status is not possible');
  }
}








setInterval(function(){
  // if (sid != ""){
    if(sid != "")
    {
      $.ajax({
          type:"GET",
          url:"/notifcation/call/",
          data:"sid="+$('#telephone_sid').val(),
          success: function(msg11){
          $('#CallStatus').html(msg11);
          // // need to updated calltimer
          // if(msg11 == "ConnectingAgent"){
          //   calltimer --;
          // }
          // console.log(msg11);
          // if(((msg11 == "MissCallVisitor") || (msg11 == 'RejectedVisitor') ||(msg11 == 'AnsweredVisitor')) && (callstatusloadflag == 0)){
          //   callstatusloadflag = 1;
          // }
          // laststatus = msg11;
          }
      });
    }
  // }


}, 2000); // 1 sec repeated





function LoadLeadStatus()
{
          // alert(); 

  $.ajax({
         type:"GET",
         url:"/leadDataLoad/LeadStatus/",
         data:"callStatusSelected="+$('#CallStatusSelect').val()+"&leadid="+leadid,
         success: function(msg){
          callstatusloadflag = 2;
          var options = '';
          $('#leadStatusSelect').html('');
          $.each(msg.leadstatuslist, function (value) {
              options += '<option value="' + msg.leadstatuslist[value]['id'] + '">' + msg.leadstatuslist[value]['option'] + '</option>';
          });
          $('#leadStatusSelect').append(options);
         }
      });
}



function DisplayEnqueryDate(){
    var lss = $('#leadStatusSelect').val();
    $.ajax({
      type:"GET",
      url:"/leadDataLoad/leadStatusEnquiryDate/",
      data:"leadStatusSelect="+$('#leadStatusSelect').val(),
      success: function(msg){
        if (msg.Status){
          $('#LeadStatusEnquiryDate').show();
        }
        else{
          $('#LeadStatusEnquiryDate').hide();

        }
      }
   });
   
}




function editincommingcalllead(leadid,sida){
  edit(leadid);
  $('#telephone_sid').val(sida);
}