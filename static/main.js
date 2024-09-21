
const logout_btn = document.getElementById("logout-btn");
logout_btn.addEventListener("click",logout);


function logout(){
    const url = document.URL
    window.location.href = '/home'
    $.ajax({
        url : "/logout",
        type : "POST",
        contentType : "application/json",
        data : JSON.stringify({
            'uid' : url.substring(url.lastIndexOf('/')+1)
        }),
        success : function(response) {
            console.log("success")
        },
        error : function(error){
            console.log("Error:",error);
        }
    })

}

function toggleDropdown() {
    var dropdown = document.getElementById("dropdown-menu");
    // console.log(dropdown.style.display)
    if (dropdown.style.display === "block") {
        dropdown.style.display = "none";
    } else {
        dropdown.style.display = "block";
    }
}

// Close the dropdown if clicked outside
window.onclick = function(event) {
    const dropdown = document.getElementById("dropdown-menu");
    if(event.target.matches(".profile-icon") || event.target.matches(".welcome") || event.target.matches(".profile")) {
        toggleDropdown();
    }else{
        dropdown.style.display = "none";
    }
}