$(document).ready(function() {

    // The code to call the suggest URL to trigger the view to return a list of items based on the search bar input
    $("#search-input").keyup(function() {
        var query;
        query = $(this).val();

        $.get('/card/suggestcat/',
        {"suggestion":query},
        function(data) {
            $(".categories-listing").html(data);
        }
        )

        $.get('/card/suggestcard/',
        {"suggestion":query},
        function(data) {
            $(".cardset-listing").html(data);
        }
        )
    })

    // When the site reloads ensure the category radio button is checked
    $(function () {
        $("#catsearch").attr("checked",true)
        $("#cardsearch").attr("checked",false)
    })


    // Code to enable/disable the other search results depending on user choice
    $("#catsearch").click(function () {
        $(".categories-listing").css("display","block");
        $(".cardset-listing").css("display","none");
    })

    $("#cardsearch").click(function () {
        $(".categories-listing").css("display","none");
        $(".cardset-listing").css("display","block");
    })


})