axios.defaults.xsrfCookieName = 'csrftoken'
axios.defaults.xsrfHeaderName = 'X-CSRFToken'

function fileUpload(blobInfo, success, failure) {
  console.log("called(1)");
  axios.post('/emailx/', {})
  .then(function (response) {
    console.log(response);
  })
  .catch(function (error) {
    console.log(error);
  });
}


// function style_editor() {
//   console.log(document.getElementById("mceu_16"));
//   if (document.getElementById("mceu_16") == null) {
//     window.setTimeout("style_editor()", 100);
//     console.log("here");
//   }
//   else {
//     if ($("#mceu_16").css("margin-left") == "0px" || $("#mceu_16").css("margin-left") == undefined) {
//         console.log("yes", $("#mceu_16").css("margin-left"))
//         $("#mceu_16").css("margin-left", "10vw");
//         console.log("yes-2", $("#mceu_16").css("margin-left"))
//     }
//     else {
//       console.log("no", $("#mceu_16").css("margin-left"))
//     }
//   }
// }
$("#id_emailx_formx").on("submit", function( event ) {
    event.preventDefault();
    console.log($(this).serialize());
});

function submit_emailx() {
  var formdata = $("#id_emailx_formx").serialize();
  var mailbody = tinyMCE.activeEditor.getContent();
  formdata = formdata.replace(
    "message_content=&",
    `message_content=${mailbody}&`);

  axios.post("/emailx/composer/", formdata)
  .then(function (response) {
    if (response.data.success != undefined) {
      $('#emailcompose').modal('hide');
      toastr.options = {
          "closeButton": true,
          "debug": false,
          "progressBar": true,
          "positionClass": "toast-top-right",
          "onclick": null,
          "showDuration": "400",
          "hideDuration": "1000",
          "timeOut": "2000",
          "extendedTimeOut": "1000",
          "showEasing": "swing",
          "hideEasing": "linear",
          "showMethod": "fadeIn",
          "hideMethod": "fadeOut"
        };
      toastr['success']("Mail Sent Successfully.");
          }
    }
  })
  .catch(function (error) {
    console.log(error);
  });

}



 // function load_editor() {
 //   if (document.getElementById("id_message_content") == null ) {
 //     console.log("null");
 //     window.setTimeout("load_editor()", 100);
 //   }
 //   else {
 //     console.log("null");
 //      tinymce.init({
 //        selector: '#id_message_content',
 //        images_upload_url: '/emailx/',
 //        height: 500,
 //        width: "95%",
 //        theme: 'modern',
 //        plugins: 'print preview fullpage searchreplace autolink directionality visualblocks visualchars fullscreen image link media table charmap hr pagebreak nonbreaking anchor toc insertdatetime advlist lists textcolor imagetools contextmenu colorpicker textpattern',
 //        toolbar1: 'formatselect | bold italic strikethrough forecolor backcolor | link | alignleft aligncenter alignright alignjustify  | numlist bullist outdent indent  | removeformat',
 //        image_advtab: true,
 //        relative_urls: false,
 //        content_css: [
 //          '//fonts.googleapis.com/css?family=Lato:300,300i,400,400i',
 //          '//www.tinymce.com/css/codepen.min.css'
 //        ]
 //      }
 //      );
 //   }
 // }