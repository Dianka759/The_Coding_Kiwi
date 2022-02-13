// #######################
//  Getting Dad Jokes
// #######################
getDJ();

function getDJ() {
    // Ajax call to SW API  
    $.getJSON("https://icanhazdadjoke.com/", "Accept: application/json", function (json) {
        var data = JSON.parse(JSON.stringify(json));
        // console.log(data.joke);
        $(".joke").html(data.joke);
    });
}

$("button").on("click", getDJ);


// #########################
//  LECTURES NAV BAR
// #########################

function openTab(event, langauge) {
    var i, tabcontent, tablinks;
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
    document.getElementById(langauge).style.display = "block";
    event.currentTarget.className += " active";
}


function openNav(event, id) {
    var tablinks = document.getElementsByClassName("tablinks");
    for (var i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" bg-dark", "");
    }
    var x = document.getElementById(id).innerHTML;
    document.getElementById("inside_nav").innerHTML = x;
    event.currentTarget.className += " bg-dark";
}
