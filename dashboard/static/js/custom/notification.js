
//  Alert box
// toastr.options = {
//     "closeButton": true,
//     "debug": false,
//     "progressBar": true,
//     "positionClass": "toast-bottom-right",
//     "onclick": null,
//     "showDuration": "4500",
//     "hideDuration": "100",
//     "timeOut": "4500",
//     "extendedTimeOut": "600",
//     "showEasing": "swing",
//     "hideEasing": "linear",
//     "showMethod": "fadeIn",
//     "hideMethod": "fadeOut",
//     'iconClasses': {
//         'error': 'fa fa-phone',
//         'info': 'fa fa-info',
//         'success': 'fa fa-info',
//         'warning': 'fa fa-info'
//     }
//   };



function alertclick(){
// alert
    $.ajax({
            type:"GET",
            url:"/notifcation/alert/",
            success: function(msg){
                $('#alertstatus').html('');
                $.each(msg.alertLeads, function (value) {
                    lsir = '<li> <div class="dropdown-messages-box"> <a class="pull-left"  href="#" onclick="edit('+msg.alertLeads[value]['leadid']+')">'+ msg.alertLeads[value]['name'] +'<br> <small >'+  msg.alertLeads[value]['time'] +'</small> </a>';
                    lsir = lsir + '<div class="media-body"> '+  msg.alertLeads[value]['status']  +' <br> <small class="text-muted">'+ msg.alertLeads[value]['datetime']  +'</small></div></div></li> <hr>';
                    $('#alertstatus').append(lsir);
                });
                $('#alertstatuscount').html(msg.count);
            }
    });
    
} 

function notificationclick(){
    $.ajax({
        type:"GET",
        url:"/notifcation/notification/",
        success: function(msg){
            $('#NewLeadCountTime').html(msg.newLeadsdatetimeofinfo);
            $('#NewLeadCount').html(msg.newLeads);
            $('#notificationcount').html(msg.newLeads);
        }
    });
}



function infoclick(){
    $.ajax({
        type:"GET",
        url:"/notifcation/info/",
        success: function(msg){
            $.each(msg, function (value) {
                if (value != "datetimeofinfo")
                { $('#'+value).html(msg[value]);}
            });
            $('.datetimeofinfo').html(msg.datetimeofinfo);
        }
    });
}




function incomingalert(){
    $.ajax({
    type:"GET",
    url:"/notifcation/incomingalert/",
    success: function(msg){
        $('#incommingcalllist').html('');
        $('#incommingcallshow').show();
        $.each(msg.listofsid, function (value) {
            lsir = '<li> <div class="dropdown-messages-box"> <a class="pull-left" href="#" onclick="editincommingcalllead('+msg.listofsid[value]['leadid']+','+msg.listofsid[value]['sid'] + ')">' + msg.listofsid[value]['name'] +'<br> <small class="text-danger">'+  msg.listofsid[value]['callstatus'] +'</small> </a>';
            lsir = lsir + '<div class="media-body"> '+  msg.listofsid[value]['leadstatus']  +' <br> <small class="text-muted">'+ msg.listofsid[value]['datetime']  +'</small></div></div></li><hr>';
            $('#incommingcalllist').append(lsir);
        });
        if(parseInt(msg.count) == 0){
            $('#incommingcallshow').hide();

            // toastr['error']("Incomming Call");
        }
        $('#incommingcallcount').html(msg.count);

    }
});
}

infoclick();
notificationclick();
alertclick();
incomingalert();


setInterval(function(){
    //  incomingalert();
}, 5000); // 3 sec repeated 





