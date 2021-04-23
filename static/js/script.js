$(document).ready(function() {
    
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
});