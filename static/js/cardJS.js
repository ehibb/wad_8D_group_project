$(document).ready(function() {
    
    // When the page loads set the total number of cards display to the correct value
    $(function() {
        var numCards = $('.slider-inner').children().length;
        $('.slidenumbertotal').text(numCards);
    })


    // JQuery Code that adds a shadow to the Flash Card on Hover
    $(".flip").hover(function()
    {
        $(this).toggleClass('classShadow');
    });

    // When the card is pressed and the animation toggles, this code removes the shadow whist its flipping and adds it back half a second later
    $(".flip").click(function () {

        $(this).removeClass('classShadow')
        that = this;
        setTimeout(function() {
            $(that).addClass('classShadow')
        }, 440)
    });

    // Triggers the flip animation when you click on the Flash Card
    $(function(){
        $(".flip").flip({
        trigger: 'click'
        });
    });


    // Shadows for Forward and Backward Buttons
    $(".forward").hover(function()
    {
        $(this).toggleClass('classShadow');
    });

    $(".backward").hover(function()
    {
        $(this).toggleClass('classShadow');
    });


    // Code that shows the next Card when Forward/Backward button is hit. Also alters current Card number.
    $('.forward').click(function() {
        var curCard = $('.active');
        var nextCard = curCard.next();

        if (nextCard.length) {
            curCard.removeClass('active').css('z-index',-100);
            nextCard.addClass('active').css('z-index',100);

            var curCardNum = Number($('.slidenumbercurrent').text());
            curCardNum += 1;
            curCardNum = String(curCardNum);
            $('.slidenumbercurrent').text(curCardNum);
        }

    })

    $('.backward').click(function() {
        var curCard = $('.active');
        var previousCard = curCard.prev();

        if (previousCard.length) {
            curCard.removeClass('active').css('z-index',-100);
            previousCard.addClass('active').css('z-index',100);

            var curCardNum = Number($('.slidenumbercurrent').text());
            curCardNum += -1;
            curCardNum = String(curCardNum);
            $('.slidenumbercurrent').text(curCardNum);
        }
        
    })



});