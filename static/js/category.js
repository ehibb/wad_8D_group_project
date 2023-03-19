$(document).ready(function () {

    $(function() {
        var catname;
        catname = $("#catName").attr('data-catname');

        $.get('/card/view_category/',
        {'name': catname},
        function (data) {
            $('#catViewCount').html(data);
        }
        )
    })

    $('#like').click(function () {
        var catName;
        catName = $("#catName").attr('data-catname');

        $.get('/card/like_category/',
        {'name': catName},
        function (data) {
            $("#catLikeCount").html(data);
            $('#like').prop('disabled',true);
            $('#like').css('background-color','rgb(106, 214, 2)');
            $('#like').css('cursor','default');
        }
        )
    })

})