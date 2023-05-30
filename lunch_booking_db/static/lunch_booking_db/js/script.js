//disabling the Date picker
let today = new Date();
var dd = String(today.getDate()).padStart(2, '0');
var mm = String(today.getMonth() + 1).padStart(2, '0');
var yyyy = today.getFullYear();
let time = yyyy + '-' + mm + '-' + dd;

// $('#date_picker').attr('min',time);
// $('#date_picker').attr('max',time);
let tomorrow = today.setDate(today.getDate() + 1);

//variable Declaration
const checkbox = document.getElementById('lunch-book');
// const submitBtn=document.querySelector('#submit');
const url = "https://script.google.com/macros/s/AKfycbzXGlJqONdUdlVKmT2Q9KnxEqfRLRYCkrqOb_85ik1a0ivgszX_WOXxZrsdpPhZU8zm8g/exec";
const downloadSection = document.querySelector('#date-picker-container');
const downloadBtn = document.querySelector('.btn');
const statement = document.querySelector('#booking-statement');
let selectedDate = document.querySelector('#booking-date');
const regnum = document.getElementById("radio-1");
const dohs = document.getElementById("radio-2");
const regnum2 = document.getElementById("radio-3");
const container_section = document.getElementById("main_ele");
const loader = document.getElementById("loader")
const landing_loader = document.getElementById("loader_div")
const tick_div = document.getElementById("tick_mark_div")
const cross_div = document.getElementById("cross_mark_div")
const book_container = document.getElementById("book_container")
const reg_div = document.getElementById("reg_div")
const reg_btn = document.getElementById("reg_btn")
const id_input = document.getElementById("id_input")
// let tbody=document.getElementById('table-body');
// submitBtn.addEventListener('click',postData);
downloadBtn.addEventListener('click', downloadData);

checkbox.addEventListener("change", postData);
regnum.addEventListener("change", verify_call);
dohs.addEventListener("change", verify_call);

var registering = false;

reg_btn.addEventListener("click", (e) => {
  // e.preventDefault();
  // reg_btn.disabled = true;
  // reg_btn.css('pointer-events', 'none');
  reg_btn.classList.add("disable-click")

  let id = id_input.value;
  if (id.length === 6) {
    if (!registering) {
      registering = true;
      register(id);
    }
  } else {
    alert("Please enter a valid ID");
  }

});

function verify_call(e) {
  if (checkbox.checked) {
    postData(e);
  }
}


function register(id) {
  let regObj = {id: id};
  $.ajax({
    url: "ajax-register-office-id/",
    method: 'POST',
    data: regObj,
    headers: {'X-CSRFToken': csrf_token},
    success: function (response) {
      console.log(response);
      alert("Your response is stored successfully!!!")
      // reg_div.style.display = 'none';
      location.reload();
      check_email();
    },
    error: function (error) {
      console.log(error);
      console.log("error");
      alert("registration failed");
      registering = false;
    }
  });
}

function formatDate(date) {
    var d = new Date(date),
        month = '' + (d.getMonth() + 1),
        day = '' + d.getDate(),
        year = d.getFullYear();

    if (month.length < 2)
        month = '0' + month;
    if (day.length < 2)
        day = '0' + day;

    return [year, month, day].join('-');
}

function downloadData(e) {
  let dates = selectedDate.innerHTML.split("/")
  let newDate = dates[1] + "/" + dates[0] + "/" + dates[2];
  let date = new Date(newDate);
  date = formatDate(date);
  console.log(date);
  $.ajax({
    url: "serve-booking-list/",
    method: 'GET',
    data: {
      'date': date
    },
    headers: {'X-CSRFToken': csrf_token},
    success: function (response) {
      console.log(response);
      bookingData = []
      let lunchData = response['lunch_data'];

      // table creation in html <can be ignored>//
      let ind = 1;
      lunchData.forEach(element => {
        bookingData.push([ind, element['email'], element['name'], element['office_id'], ""])
        ind += 1;
      });

      // console.log(lunchData);
      generatePdf(bookingData, newDate);
      return response
    },
    error: function (error) {
      console.log(error);
      console.log("error");
    }
  });
}

//update data on the database as per request of the user
function postData(e) {
  loader.style.display = 'block';
  e.preventDefault();
  //locatioin selection
  // let lRegnum = regnum.checked;
  // const selectedLocation = lRegnum ? "Regnum" : "Regnum";
  let status = checkbox.checked ? "yes" : "no";

  $.ajax({
    url: "ajax-book-lunch/",
    method: 'POST',
    data: {
      'booking': status,
      'day': 1
    },
    headers: {'X-CSRFToken': csrf_token},
    success: function (response) {
      console.log(response);
      loader.style.display = 'none';
      tick_div.style.display = 'block';
      setTimeout(() => tick_div.style.display = 'none', 2000)
      load_calender();
      return response;
    },
    error: function (error) {
      console.log(error);
      console.log("error");
      cross_div.style.display = 'block';
      setTimeout(() => cross_div.style.display = 'none', 2000)
      loader.style.display = 'none';
      checkbox.checked = !checkbox.checked;
    }
  });
}


function check_email() {
  $.ajax({
    url: "ajax-check-office-id/",
    method: 'GET',
    headers: {'X-CSRFToken': csrf_token},
    success: function (response) {
      console.log(response)
      let ofc_id = response['office_id'];
      if (ofc_id === "n/a") {
        book_container.style.display = 'none';
        reg_div.style.display = 'block';
        loader.style.display = 'none';
        landing_loader.style.display = 'none';
        return response
      } else {
        book_container.style.display = 'block';
        loader.style.display = 'none';
        landing_loader.style.display = 'none';
      }

      if (response['user_type'] === "admin") {
        downloadSection.style['display'] = 'block';
        container_section.classList.remove("vertical-center");
        var time_today = (new Date()).getHours();

        if (time_today >= 8 && time_today < 20) {
          // console.log(time_today);
        } else {
          document.getElementById("no_time").style.display = 'block';
          // downloadSection.style['display'] = 'block';
          loadDashboard();
        }
      } else {
        loadDashboard();
        downloadSection.style['display'] = 'none';
        container_section.classList.add("vertical-center");
      }

      if (response['status'] === "Y") {

        // statement.innerHTML="Already Booked";
        // console.log(checkbox.value)
        checkbox.checked = true;

      } else {
        checkbox.checked = false;
      }

      regnum.checked = true;
      dohs.checked = false;

      return response
    },
    error: function (error) {
      console.log(error);
      console.log("error");
    }
  });
}

cookie_email ? check_email() : null;
console.log(cookie_email);
// var dateString = tomorrow.toLocaleDateString();
// var dateElement = document.getElementById("date");
// dateElement.innerHTML = dateString;
function generatePdf(elements, q_date) {

  //Convert Table to PDF.
  var doc = new jsPDF("p", "pt")
  // Supply data via script
  // var res = doc.autoTableHtmlToJson(document.getElementById("table"));
  // console.log(res);
  // generate auto table with body
  // console.log(elements)
  var y = 10;
  doc.setLineWidth(2);
  doc.setFont("helvetica");
  doc.setFontType("bold");
  doc.setFontSize(20);
  let title = "      Date: " + (new Date(q_date)).toDateString() + "                Total Bookings: " + elements.length;
  doc.text(10, y = y + 30, title);

  doc.autoTable({
    columns: ["Sl", "Email", "Name", "ID", "Tick"],
    body: elements,
    startY: 70,
    theme: 'grid',
    // styles: { fontSize: 20 }

  })
  // save the data to this file
  doc.save((new Date(q_date)).toDateString());
}

function get_booking_count() {
  $.ajax({
    url: "ajax-get-booking-count/",
    method: 'GET',
    headers: {'X-CSRFToken': csrf_token},
    success: function (response) {
      // console.log(response);
      document.getElementById("total_booking").innerHTML = response['count'];
    },
    error: function (error) {
      console.log(error);
      console.log("error");
      document.getElementById("total_booking").innerHTML = "n/a";
    }
  });
}

get_booking_count();

const interval = setInterval(function () {
  get_booking_count();
}, 1000);

// clearInterval(interval);

function load_calender(){
  $.ajax({
    url: "ajax-get-booking-of-date/",
    method: 'GET',
    headers: {'X-CSRFToken': csrf_token},
    success: function (response) {
      for (var i=0; i<response['status'].length; i++){
        let var_date = new Date();
        var_date.setDate(var_date.getDate() + i - 2);
        if (response['status'][i] === 'yes') {
          let id_b = `#cb_${i+1}`
          $(id_b).html(`
            <div class="calender_bubble" >
              <span class="calender_bubble_span booked">${var_date.getDate()}</span>
             </div>
             <span class="calender_day_span default_booked">${dow[var_date.getDay()]}</span>
          `)
        }
        else if (response['status'][i] === 'n/a' && i>3) {
          let id_b = `#cb_${i+1}`
          $(id_b).html(`
            <div class="calender_bubble" >
              <span class="calender_bubble_span default_booked">${var_date.getDate()}</span>
             </div>
             <span class="calender_day_span default_booked">${dow[var_date.getDay()]}</span>
          `)
        }
        else {
          let id_b = `#cb_${i+1}`
          $(id_b).html(`
            <div class="calender_bubble" >
              <span class="calender_bubble_span un_booked">${var_date.getDate()}</span>
             </div>
             <span class="calender_day_span default_booked">${dow[var_date.getDay()]}</span>
          `)
        }
      }
    },
    error: function (error) {
      console.log(error);
      console.log("error");
    }
  });

  // for (var i=-3; i<=3; i++){
  //   let var_date = new Date();
  //   var_date.setDate(var_date.getDate() + i);
  //   $.ajax({
  //     url: "ajax-get-booking-of-date/",
  //     method: 'GET',
  //     data: {
  //       'date': i
  //     },
  //     headers: {'X-CSRFToken': csrf_token},
  //     success: function (response) {
  //       console.log(response['status']);
  //       if (response['status'] === 'yes'){
  //         let id_b = `#cb_${i+4}`
  //         $(id_b).html(`<span class="booked">${var_date.getDate()}</span>`)
  //       }
  //       else {
  //         let id_b = `#cb_${i+4}`
  //         console.log(id_b);
  //         $(id_b).html(`<span class="un_booked">${var_date.getDate()}</span>`)
  //       }
  //     },
  //     error: function (error) {
  //       console.log(error);
  //       console.log("error");
  //     }
  //   });
  // }
}

load_calender();