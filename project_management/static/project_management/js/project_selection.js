
function project_selection(target, proj_id, req_url){
    let proj_s = document.getElementsByClassName('msg');
    for (let i = 0; i < proj_s.length; i++) {
        let item = proj_s[i];
        if (item === target) {
            item.classList.add("selected-bg")
        }
        else {
            item.classList.remove("selected-bg")
        }
    }

    $.ajax({
        url: req_url.replace('0', proj_id),
        method: 'GET',
        success: function (response) {
            console.log(response)
        },
        error: function (error) {
            console.log(error);
            console.log("error");
        }
    });
}