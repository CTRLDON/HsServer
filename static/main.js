
const logout_btn = document.getElementById("log-out");
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