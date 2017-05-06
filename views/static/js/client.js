$(document).ready(function() {
    $('section.splash').height($(window).height());

    $.stellar({
        horizontalScrolling: false,
    });

    $('section#parallax').localScroll({
        offset: {
            top: -80
        }
    });

    $('section:not(#parallax)').localScroll({
        offset: {
            top: -50
        }
    });

    setInterval(function() {
        if (size == 'small' && prevSize != 'small') {
            $('header a.logo').animate({
                top: '8px'
            }, 500);
            $('header a.logo img').animate({
                height: '30px'
            }, 500);
            $('header ul').animate({
                top: '14px'
            }, 500);
            $('header ul li a').animate({
                fontSize: '18px'
            }, 500);
            $('header').animate({
                height: '50px'
            }, 500);

            prevSize = 'small';
        } else if (size == 'big' && prevSize != 'big') {

            $('header a.logo').animate({
                top: '14px'
            }, 500);
            $('header a.logo img').animate({
                height: '50px'
            }, 500);
            $('header ul').animate({
                top: '26px'
            }, 500);
            $('header ul li a').animate({
                fontSize: '24px'
            }, 500);
            $('header').animate({
                height: '80px'
            }, 500);

            prevSize = 'big';
        }
    }, 1000);

    var prevSize = 'big';
    var size = 'big';
    $(window).scroll(function() {
        if ($(window).scrollTop() > ($(window).height() - 80)) {
            size = 'small';

        } else {
            size = 'big';

        }
    });

    $(window).resize(function() {
        $('section.splash').height($(window).height());

        if ($(window).scrollTop() > ($(window).height() - 80)) {
            size = 'small';

        } else {
            size = 'big';

        }
    });
});