//disabling the Date picker
let today = new Date();
var dd = String(today.getDate()).padStart(2, '0');
var mm = String(today.getMonth() + 1).padStart(2, '0');
var yyyy = today.getFullYear();
let time = yyyy + '-' + mm + '-' + dd;

// $('#date_picker').attr('min',time);
// $('#date_picker').attr('max',time);
let tomorrow=today.setDate(today.getDate() + 1);

//variable Declaration
const checkbox=document.getElementById('lunch-book');
// const submitBtn=document.querySelector('#submit');
const url="https://script.google.com/macros/s/AKfycbzXGlJqONdUdlVKmT2Q9KnxEqfRLRYCkrqOb_85ik1a0ivgszX_WOXxZrsdpPhZU8zm8g/exec";
const downloadSection=document.querySelector('#date-picker-container');
const downloadBtn=document.querySelector('.btn');
const statement=document.querySelector('#booking-statement');
let selectedDate=document.querySelector('#booking-date');
const regnum = document.getElementById("radio-1");
const dohs = document.getElementById("radio-2");
const regnum2= document.getElementById("radio-3");
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
downloadBtn.addEventListener('click',downloadData);

checkbox.addEventListener("change",postData);
regnum.addEventListener("change", verify_call);
dohs.addEventListener("change", verify_call);

reg_btn.addEventListener("click", (e) =>{
    e.preventDefault();
    // reg_btn.disabled = true;
    // reg_btn.css('pointer-events', 'none');
    var id = id_input.value;
    register(id, cookie_email, cookie_name);
});

function verify_call(e){
    if (checkbox.checked) {
        postData(e);
    }
}



function register(id,email,name){
    let regObj={id:id,email:email,name:name};
    console.log(regObj)
    let options={
        method:"POST",
    }
    let qs=new URLSearchParams(regObj);
    fetch(`${url}?${qs}`,options)
    .then(res => res.json())
    .then(resp =>{
        console.log(resp);
        reg_div.style.display = 'none';
        // window.location.reload();
        // book_container.style.display = 'block';
        check_email();
        // return resp;
    }).catch(err => {
        console.error(err);
        alert("registration failed");
        // reg_btn.disabled = false;
        // reg_btn.css('pointer-events', '');
    });

}

function downloadData(e){
    //date and location selection from input and get the data people who booked lunch
    // let selectedDate=document.getElementById('booking-date');
    let dates=selectedDate.innerHTML.split("/")
    let newDate=dates[1]+"/"+dates[0]+"/"+dates[2];
    let date=new Date(newDate);
    date=date.getDate();
    console.log(date)
    e.preventDefault();
    let lRegnum=regnum2.checked;
    const selectedLocation =lRegnum?"Regnum":"Regnum";
    //post request paraameters
    let lunchDict={download:'T',date:date,location:selectedLocation};
    let options={
        method:"POST",
    }
    //download reqeust from the database for a particular date and location
    let qs=new URLSearchParams(lunchDict);
    lunchData=fetch(`${url}?${qs}`,options)
    .then(res => res.json())
    .then(resp => {
        bookingData=[]
        let lunchData=resp['lunchData'];

        // table creation in html <can be ignored>//
        let ind=1;
        lunchData.forEach(element => {
            bookingData.push([ind,element['name'],element['email'],element['id'],""])
            ind+=1;
        });

        console.log(lunchData);
        generatePdf(bookingData, newDate);
        return resp
    })
    .catch(err => {
        console.error(err);
    });
}

//update data on the database as per request of the user
function postData(e){
    loader.style.display = 'block';
    e.preventDefault();
    //locatioin selection
    let lRegnum=regnum.checked;
    const selectedLocation =lRegnum?"Regnum":"Regnum";
    let status=checkbox.checked?"Y":"N";
    let dateDict={email:cookie_email,status:status,location:selectedLocation};
    // console.log(dateDict);
    let qs=new URLSearchParams(dateDict);
    let options={
        method: "POST"
    }
    fetch(`${url}?${qs}`,options)
        .then(res => res.json())
        .then(resp => {
            console.log(resp);
            // alert("booking status updated successfully");
            loader.style.display = 'none';
            tick_div.style.display = 'block';
            setTimeout(()=>tick_div.style.display = 'none', 2000)
            return resp;
        })
        .catch(err => {
            console.error(err);
            // alert("booking status update failed");
            cross_div.style.display = 'block';
            setTimeout(()=>cross_div.style.display = 'none', 2000)
            loader.style.display = 'none';
            checkbox.checked = !checkbox.checked;
        });
}


function check_email(){
    let dateCheck= fetch(url+"?email="+cookie_email)
    .then(r=>r.json())
    .then( r=>{
        r=JSON.parse(r)
        console.log(r);
        console.log(r['userType']);
        let userType=(r['userType']);

        if (r['email']=="N/A" ){
            book_container.style.display = 'none';
            reg_div.style.display = 'block';
            loader.style.display = 'none';
            landing_loader.style.display = 'none';
            return r
        }
        else{
            book_container.style.display = 'block';
            loader.style.display = 'none';
            landing_loader.style.display = 'none';
        }

        // return r;

        if (userType=="Admin"){
          downloadSection.style['display']='block';
          container_section.classList.remove("vertical-center");
        }
        else{
            downloadSection.style['display']='none';
            container_section.classList.add("vertical-center");
        }

        if (r['status']=="Y" ){
            // statement.innerHTML="Already Booked";
            // console.log(checkbox.value)
            checkbox.checked = true;

        }
        else {
            checkbox.checked = false;
        }
        if (r['location'] == "Regnum"){
            regnum.checked = true;
            dohs.checked = false;
        }
        else{
            // console.log("dsdsfdsgfsdgfasdgfasdgfvasDZ")
            regnum.checked = false;
            dohs.checked = true;
        }

        return r
    })
}

cookie_email?check_email():null;
    // var dateString = tomorrow.toLocaleDateString();
    // var dateElement = document.getElementById("date");
    // dateElement.innerHTML = dateString;
function generatePdf(elements, q_date){

    //Convert Table to PDF.
    var doc = new jsPDF("p","pt")
    // Supply data via script
    // var res = doc.autoTableHtmlToJson(document.getElementById("table"));
    // console.log(res);
    // generate auto table with body
    console.log(elements)
    var y = 10;
    doc.setLineWidth(2);
    doc.setFont("helvetica");
    doc.setFontType("bold");
    doc.setFontSize(20);
    let title="      Date: " + (new Date(q_date)).toDateString() + "                Total Bookings: " + elements.length;
    doc.text(10, y = y + 30, title);

    doc.autoTable({
        columns:["Sl","Name","Email","ID",""],
        body: elements,
        startY: 70,
        theme: 'grid',
        // styles: { fontSize: 20 }

    })
    // save the data to this file
    doc.save((new Date(q_date)).toDateString());
}

function get_booking_count() {
    let dateDict={date:dates[2].getDate(),totalBookings:1};
    // console.log(dateDict);
    let qs=new URLSearchParams(dateDict);
    let options={
        method: "POST"
    }

    fetch(`${url}?${qs}`,options)
        .then(res => res.json())
        .then(resp => {
            // console.log(resp);

            document.getElementById("total_booking").innerHTML = resp['total'];
        })
        .catch(err => {
            // console.error(err);
            // alert("booking status update failed");
            document.getElementById("total_booking").innerHTML = "n/a";
        });
}

get_booking_count();

const interval = setInterval(function() {
   get_booking_count();
 }, 1000);

// clearInterval(interval);
