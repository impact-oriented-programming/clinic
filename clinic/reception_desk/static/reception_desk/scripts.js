


// Used to alert success messages, assumes the input is of type success
function alert_msg(msg){
                swal({
                  title: "Success!",
                  text: `${msg}`,
                  type: "success",
                  confirmButtonColor: '#28a745'
                })}

// Removes letters after # in url
function remove_id_name(){
                var hash = location.hash.replace('#','');
                if(hash != ''){
                    localStorage.setItem("scroll", window.pageYOffset);
                    location.hash = '';
                }
                $(window).bind('hashchange',function(event){
                var hash = location.hash.replace('#','');
                if(hash == '') {
                window.scrollTo(0, parseInt(localStorage.getItem("scroll")));
                localStorage.removeItem("scroll");}
            });
            };

function set_arrived_click(appointment_id,patient,path){
        swal({
          title: `Are you sure?`,
          text: `Check in ${patient}?
           Action can not be reverted!`,
          type: "info",
          showCancelButton: true,
          confirmButtonColor: '#28a745',
          cancelButtonColor: '#dc3545',
          confirmButtonText: 'Yes',
          cancelButtonText: 'No',
          reverseButtons: true
        })
        .then((result) => {
            if (result.value) {
            post(`${path}`,
            {'arrived':appointment_id});
          }
          else{}
        })
       };

// Creates and sends a post form from params, sends to path
function post(path, params) {
              const form = document.createElement('form');
              form.method = 'post';
              form.action = path;

              var hiddenField1 = document.createElement("input");
              hiddenField1.setAttribute("type", "hidden");
              hiddenField1.setAttribute("name", 'csrfmiddlewaretoken');
              hiddenField1.setAttribute("value", getCookie('csrftoken'));
              form.appendChild(hiddenField1);

              for (const key in params) {
                if (params.hasOwnProperty(key)) {
                  const hiddenField = document.createElement('input');
                  hiddenField.type = 'hidden';
                  hiddenField.name = key;
                  hiddenField.value = params[key];

                  form.appendChild(hiddenField);
                }
              }

              document.body.appendChild(form);
              form.submit();
            }

// Returns a CSRF token
function getCookie(name) {
            var cookieValue = null;
            if (document.cookie && document.cookie != '') {
                    var cookies = document.cookie.split(';');
                    for (var i = 0; i < cookies.length; i++) {
                            var cookie = jQuery.trim(cookies[i]);
                            // Does this cookie string begin with the name we want?
                            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                                    break;
                            }
                    }
            }
            return cookieValue;
            }

// Pop up for cancel appointment
function remove_patient_click(id,patient,path){
            swal({
              title: "Are you sure?",
              text: `Cancel appointment for ${patient}?`,
              type: "warning",
              showCancelButton: true,
              confirmButtonColor: '#dc3545',
              cancelButtonColor: '#6c757d',
              confirmButtonText: 'Yes',
              cancelButtonText: 'No',
              reverseButtons: true
            })
            .then((result) => {
                if (result.value) {
                post(`${path}`,
                {'remove_id':id});
              }
            })
           };

function startTime(hour,minute, id) {
  var arrived = new Date(0, 0, 0, hour, minute, 0);
  var today = new Date();
  var h = today.getHours() - arrived.getHours();
  var m = today.getMinutes() - arrived.getMinutes();
  if (m<0){
   h -= 1;
   m += 60;
  }
  var s = today.getSeconds();
  document.getElementById(id).innerHTML =
  h*60 + m + " Minutes";
  setTimeout(startTime.bind(null, hour, minute, id), 500);
}
function checkTime(i) {
  if (i < 10) {i = "0" + i};  // add zero in front of numbers < 10
  return i;
}