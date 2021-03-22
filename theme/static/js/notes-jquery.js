// GENERAL DROPDOWN
function toggle(id, display = "flex"){
    dropdown = document.getElementById(id).classList;

    if (dropdown.contains("hidden")) {
        dropdown.remove("hidden");
        dropdown.add(display);
    }else{
        dropdown.remove(display);
        dropdown.add("hidden");
    }
}

// ACCOUNT DROPDOWN
function hide(dropdown, btn){
    dropdown.remove("flex");
    dropdown.add("hidden");

    $("#drop_bg").remove();
}

/* When the user clicks on the button,
toggle between hiding and showing the dropdown content */
function toggle_account_dropdown() {
    dropdown = document.getElementById("account_dropdown").classList;
    
    if (dropdown.contains("hidden")) {
        $('#dropdown').append("<div id='drop_bg' class='bg-gray-800 opacity-20 fixed inset-0 z-10 w-screen h-screen'></div>");

        dropdown.remove("hidden");
        dropdown.add("flex");
    }
    else{
        hide(dropdown, btn)
    }
}

// Close the dropdown menu if the user clicks outside of it
window.addEventListener("click", function(event) {
    if (event.target.id == "drop_bg"){
        dropdown = document.getElementById("account_dropdown").classList
        btn = document.getElementById("btn_dropdown").classList
       
        hide(dropdown, btn)
    }
})  