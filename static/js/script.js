$(document).ready(function() {
    var getUrlParameter = function getUrlParameter(sParam) {
        var sPageURL = window.location.search.substring(1),
            sURLVariables = sPageURL.split('&'),
            sParameterName,
            i;
    
        for (i = 0; i < sURLVariables.length; i++) {
            sParameterName = sURLVariables[i].split('=');
    
            if (sParameterName[0] === sParam) {
                return typeof sParameterName[1] === undefined ? true : decodeURIComponent(sParameterName[1]);
            }
        }
        return false;
    };

    $("img").click(function(e){
        var x = e.pageX - this.offsetLeft + 1
        var y = e.pageY - this.offsetTop + 1
        var click_coordinate = "("+x+","+y+")"
        console.log("click "+click_coordinate)
        $("#information_image #container").remove()
        information = "<div id='container'><p> Point on "+click_coordinate+"</p></div>"
        $("#information_image").append(information)
    })

    $("#scene-select").on('change', function() {
        var url = "http://127.0.0.1:5000/home?img="+this.value;
        $(location).attr('href',url);
    });
    
    if ($('#scene-select').val() != "default"){
        var id = $('img').attr('src');
        var arr = id.split("/");
        image = $("#scene-select").val() + ".png"
        id = id.replace(arr[3],image)
        var t = $("#image p").text()
        var tab = t.split("x")
        var xMax = tab[0].split("(")[1]
        var yMax = tab[1].split(")")[0]

        coordinate_form = "<div id='coordinate_form'><form action='' method='get' class='form-example'>"
        coordinate_form += "<div class='form-example'>"
        coordinate_form +=  "<label for='X-coordinate'>Enter x coordinate : </label>"
        coordinate_form +=  "<input type='number' name='X-coordinate' id='X-coordinate' min='0' max='"+xMax+"' required></br>"
        coordinate_form += "<span id='x'></span></div>"
        coordinate_form += "<div class='form-example'>"
        coordinate_form += "<label for='Y-coordinate'>Enter y coordinate: </label>"
        coordinate_form += "<input type='number' name='Y-coordinate' id='Y-coordinate' min='0' max='"+yMax+"' required></br>"
        coordinate_form += "<span id='y'></span></div>"
        coordinate_form += "<div class='form-example'></div>"
        coordinate_form += "<input type='submit' value='get pixel stat'></div></form></div>"
        $("#information_image").append(coordinate_form)
    }

      $( "form" ).submit(function( event ) {
        event.preventDefault();
        alert($(location).attr('<search>'))
        var url = "http://127.0.0.1:5000/home?img="+getUrlParameter('img')+"&X-coordinate="+$("#X-coordinate").val()+"&Y-coordinate="+$("#Y-coordinate").val();
        $(location).attr('href',url);
        
      });
});