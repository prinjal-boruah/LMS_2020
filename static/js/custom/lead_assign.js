
var oTable = '';
jQuery(document).ready(function() {
    
    oTable = jQuery('#leadtable_agents_activity').dataTable({

      "ajax": {
       "url": '../lead_assign/',
       "type": 'POST',
       "data": function(d,start){
            return  $('#filter_agents_activity').serialize() + "&start=" + d.start + "&length=" + d.length + "&search=" + d.search.value + "&orderCol=" + d.order[0].column + "&orderDir=" + d.order[0].dir;
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

function assigntme(e)
{
    var obj = e;
    var parent = $(e).parents('tr');
    var tme = parent.find('select').val();
      // alert(tme);
      if(tme==''){ 
        parent.find('.error').show(); return false; 
      }
      else{
        parent.find('.error').hide();
        var id = $(e).attr('data-id');
        $.ajax({
          "type":"POST",
          "url":"../lead_assign_save/",
          "data":"id="+id+"&tme="+tme,
          success: function(msg)
          {
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
            toastr['success']("Tranfer successfully.");
            reportfilter();
          }
        });
      }
    }