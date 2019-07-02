$(function () {

    var $navLi = $(".news-nav .nav li"),
        $contaninLi = $(".news-nav .contain li"),
        first = 0;

    $navLi.click(function () {
        var x = $(this).index();
        $navLi.eq(first).removeClass("active");
        $contaninLi.eq(first).removeClass("show");
        first = x;
        $navLi.eq(first).addClass("active");
        $contaninLi.eq(first).addClass("show");
    })











})