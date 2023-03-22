$(document).ready(function () {

    // Check the users inputs and change the page accordingly to their test results
    $(".scoreCheck").click(function () {


        var allAnswersDOM = $(".answer");
        var allAnswers = [];
        console.log(allAnswersDOM);
        $(allAnswersDOM).each(function () {
            allAnswers.push($(this).text());
        })

        var userAnswersDOM = $(".testInput");
        var userAnswers = [];

        $(userAnswersDOM).each(function () {
            userAnswers.push($(this).val());
            $(this).prop("disabled",true);
        })

        var questionBoxes = $(".testQuestion");
        var counter = 0;
        var score = 0;

        $(questionBoxes).each(function () {
            if (allAnswers[counter]==userAnswers[counter]) {
                $(this).css("background-color","rgb(44, 252, 3)");
                score += 1;
            } else {
                $(this).css("background-color","rgb(255, 30, 0)");
            }
            counter += 1;
        })

        $(".answerText").css("display","block");
        $(".resetTest").css("display","block");

        $("#score").text(score);
        $("#total").text(counter);

        $(".scoreSection").css("display","block");
        
    })


    // Resets the test page when the reset button is clicked
    $(".resetTest").click(function() {
        $(".scoreSection").css("display","none");
        $(".answerText").css("display","none");
        $(".resetTest").css("display","none");
        var questionBoxes = $(".testQuestion");
        $(questionBoxes).each(function () {
            $(this).css("background-color","lightcyan");
        })

        var userAnswersDOM = $(".testInput");

        $(userAnswersDOM).each(function () {
            $(this).prop("disabled",false);
        })
    })

})