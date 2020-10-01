
var oTable = '';
jQuery(document).ready(function() {
    
    oTable = jQuery('#leadtable24').dataTable({

      "ajax": {
       "url": '',
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

// reportfilter();


function edit(page,id){
  // alert();
  leadid = id;
  $.ajax({
        type:"GET",
        url: "../" + page + "_edit/",
        data:"id="+id,
        success: function(msg){
            $('#formedit').html(msg);
            $('#table').hide();
            $('#formtype').show();
        }

  });
}
