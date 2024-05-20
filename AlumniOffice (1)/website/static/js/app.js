(function($) {
    $(document).ready(function() {
        // Плавная прокрутка страницы при нажатии на ссылки в навигационном меню
        $('.menu-item a').on('click', function(event) {
            if (this.hash !== '') {
                event.preventDefault();
                var hash = this.hash;
                $('html, body').animate({
                    scrollTop: $(hash).offset().top
                }, 800, function() {
                    window.location.hash = hash;
                });
            }
        });

        // Показ и скрытие мобильного меню при нажатии на кнопку "бургер"
        $('.toggle-menu').on('click', function() {
            $('body').toggleClass('menu-open');
        });

        // Поддержание активного состояния текущего пункта меню при прокрутке страницы
        $(window).on('scroll', function() {
            var scrollPosition = $(window).scrollTop();
            $('.menu-item a').each(function() {
                var anchor = $(this);
                var target = $(anchor.attr('href'));
                if (target.position().top <= scrollPosition && target.position().top + target.outerHeight() > scrollPosition) {
                    $('.menu-item').removeClass('current-menu-item');
                    anchor.parent().addClass('current-menu-item');
                } else {
                    anchor.parent().removeClass('current-menu-item');
                }
            });
        });
    });
})(jQuery);