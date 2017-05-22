(function ($) {
    'use strict';

    $(window).on('load', function () {
        /* Preloader */
        $('#preloader').fadeOut( 400, function () {
            $(this).remove();
        });

        // Slider Revolution

        $("#slider1").revolution({
            sliderType: "standard",
            sliderLayout: "fullscreen",
            autoHeight: "on",
            delay: 9000,
            navigation: {
                keyboardNavigation: "on",
                keyboard_direction: "horizontal",
                mouseScrollNavigation: "off",
                onHoverStop: "on",
                touch: {
                    touchenabled: "on",
                    swipe_treshold: 75,
                    swipe_min_touches: 1,
                    drag_block_vertical: false,
                    swipe_direction: "horizontal"
                },
                arrows: {
                    style: "hades",
                    enable: true,
                    hide_onmobile: true,
                    hide_onleave: true,
                    tmp: '',
                    left: {
                        h_align: "left",
                        v_align: "center",
                        h_offset: 10,
                        v_offset: 0
                    },
                    right: {
                        h_align: "right",
                        v_align: "center",
                        h_offset: 10,
                        v_offset: 0
                    }
                },
                bullets: {
                    style: "",
                    enable: false,
                    hide_onmobile: true,
                    hide_onleave: true,
                    hide_delay: 200,
                    hide_delay_mobile: 1200,
                    hide_under: 0,
                    hide_over: 9999,
                    direction: "horizontal",
                    h_align: "center",
                    v_align: "bottom",
                    space: 7,
                    h_offset: 4,
                    v_offset: 40,
                    tmp: '<span class="tp-bullet-image"></span><span class="tp-bullet-title"></span>'
                }
            },
            parallax:{
                type:"scroll",
                levels:[5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85],
                origo:"enterpoint",
                speed:600,
                bgparallax:"on",
                disable_onmobile:"on"
            },

            lazyType: "smart",
            disableProgressBar: "on",
            responsiveLevels: [4096, 1024, 778, 480],
            gridwidth: [1140, 800, 750, 480],
            gridheight: [800, 600, 980, 700]
        });


        // About Video slider

        $("#slider4").revolution({
            sliderType: "standart",
            sliderLayout: "fullwidth",
            autoHeight: "off",
            delay: 9000,
            navigation: {
                keyboardNavigation: "on",
                keyboard_direction: "horizontal",
                mouseScrollNavigation: "off",
                onHoverStop: "on",
                touch: {
                    touchenabled: "on",
                    swipe_treshold: 75,
                    swipe_min_touches: 1,
                    drag_block_vertical: false,
                    swipe_direction: "horizontal"
                },
                arrows: {
                    style: "hades",
                    enable: false,
                    hide_onmobile: true,
                    hide_onleave: true,
                    tmp: '',
                    left: {
                        h_align: "left",
                        v_align: "center",
                        h_offset: 10,
                        v_offset: 0
                    },
                    right: {
                        h_align: "right",
                        v_align: "center",
                        h_offset: 10,
                        v_offset: 0
                    }
                },
                bullets: {
                    style: "",
                    enable: false,
                    hide_onmobile: true,
                    hide_onleave: true,
                    hide_delay: 200,
                    hide_delay_mobile: 1200,
                    hide_under: 0,
                    hide_over: 9999,
                    direction: "horizontal",
                    h_align: "center",
                    v_align: "bottom",
                    space: 7,
                    h_offset: 4,
                    v_offset: 40,
                    tmp: '<span class="tp-bullet-image"></span><span class="tp-bullet-title"></span>'
                }
            },
            parallax:{
                type:"scroll",
                levels:[5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85],
                origo:"enterpoint",
                speed:600,
                bgparallax:"on",
                disable_onmobile:"on"
            },

            lazyType: "smart",
            disableProgressBar: "on",
            responsiveLevels: [4096, 1024, 778, 480],
            gridwidth: [1140, 800, 750, 480],
            gridheight: [800, 600, 980, 700]
        });

        /* Image cache */
        $('.gallery-item').each(function() {
            var src = $(this).attr('href');
            var img = document.createElement('img');
            img.src = src;
            $('#image-cache').append(img);
        });


    });

    $(document).ready(function () {



        /* Isotope Portfolio */
        (function () {
            var grid = $('.grid').isotope({
                itemSelector: '.grid-item',
                percentPosition: true,
                masonry: {
                    // use outer width of grid-sizer for columnWidth
                    columnWidth: '.grid-sizer'
                }
            });

            grid.imagesLoaded(function () {
                grid.isotope();
            });

            grid.isotope({filter: '*'});

            // filter items on button click
            $('#isotope-filters').on('click', 'a', function () {
                var filterValue = $(this).attr('data-filter');
                grid.isotope({filter: filterValue});
            });

        })();
        

        // Sidebar
        $("#wrapper").on('click', '#menu-toggle', function(e) {
            e.preventDefault();
            $("#wrapper").toggleClass("toggled");
            $(".cbp-af-header").toggleClass("toggled");
            // resize isotope layout at 100ms after css transition (0.5s)
            setTimeout(function() {
                $('.grid').isotope('layout');
            }, 600);
        });
        

        // Parallax
        $('#insert').parallax("50%", 0.3);


        // Goal Progress
        $('#proto').goalProgress({
            goalAmount: 600,
            currentAmount: 436,
            textBefore: '',
            textAfter: ' projects'
        });
        $('#develop').goalProgress({
            goalAmount: 1000,
            currentAmount: 885,
            textBefore: '',
            textAfter: ' projects'
        });
        $('#design').goalProgress({
            goalAmount: 1000,
            currentAmount: 374,
            textBefore: '',
            textAfter: ' projects'
        });
        $('#testing').goalProgress({
            goalAmount: 1000,
            currentAmount: 672,
            textBefore: '',
            textAfter: ' projects'
        });

        /* Animated Counter */
        $('.count-container span').counterUp({
            delay: 10, // the delay time in ms
            time: 3000 // the speed time in ms
        });
        
        /* Magnific Popup */
        $('.gallery-item').magnificPopup({
            type: 'image',
            gallery: {
                enabled: true
            }
        });

        // Owl Carousel

        $('.owl-carousel').owlCarousel({
            items:1,
            loop:true,
            nav:true,
            navText: [
                "<i class='fa fa-angle-left' aria-hidden='true'></i>",
                "<i class='fa fa-angle-right' aria-hidden='true'></i>"
            ],
            dots: true,
            margin:10,
            autoplay: true,
            autoplayTimeout: 11000,
            autoplayHoverPause: true,
            autoplaySpeed: 1250,
            autoHeight:true
        });



        /* Contact Form */
        (function () {
            // Get the messages div.
            var formMessages = $('#form-messages');

            // Set up an event listener for the contact form.
            $('#feedback-block').on('submit', '#ajax-contact', function (e) {
                // Get the form.
                var $form = $(this);

                // Stop the browser from submitting the form.
                e.preventDefault();

                // Serialize the form data.
                var formData = $form.serialize();

                // Submit the form using AJAX.
                $.ajax({
                        type: 'POST',
                        url: $form.attr('action'),
                        data: formData
                    })
                    .done(function (response) {
                        // Make sure that the formMessages div has the 'success' class.
                        $(formMessages).removeClass('alert alert-danger');
                        $(formMessages).addClass('alert alert-success');

                        // Set the message text.
                        $(formMessages).text(response);

                        // Clear the form.
                        $('#name').val('');
                        $('#email').val('');
                        $('#message').val('');
                    })
                    .fail(function (data) {
                        // Make sure that the formMessages div has the 'error' class.
                        $(formMessages).removeClass('alert alert-success');
                        $(formMessages).addClass('alert alert-danger');

                        // Set the message text.
                        if (data.responseText !== '') {
                            $(formMessages).text(data.responseText);
                        } else {
                            $(formMessages).text('Oops! An error occured and your message could not be sent.');
                        }
                    });
            });

        })();
        


        /* Google map */
        (function () {
            if (!$('#google-map').length) {
                return false;
            }

            initGmap();

            function initGmap() {

                // Create an array of styles.
                var styles = [
                    {
                        stylers: [
                            {saturation: -100}
                        ]
                    }, {
                        featureType: "road",
                        elementType: "geometry",
                        stylers: [
                            {lightness: 100},
                            {visibility: "simplified"}
                        ]
                    }, {
                        featureType: "road",
                        elementType: "labels",
                        stylers: [
                            {visibility: "off"}
                        ]
                    }
                ];

                // Create a new StyledMapType object, passing it the array of styles,
                // as well as the name to be displayed on the map type control.
                var styledMap = new google.maps.StyledMapType(styles, {name: "Styled Map"});

                // Create a map object, and include the MapTypeId to add
                // to the map type control.
                var $latlng = new google.maps.LatLng(29.198351, -81.028046),
                    $mapOptions = {
                        zoom: 13,
                        center: $latlng,
                        panControl: false,
                        zoomControl: true,
                        scaleControl: false,
                        mapTypeControl: false,
                        scrollwheel: false,
                        mapTypeControlOptions: {
                            mapTypeIds: [google.maps.MapTypeId.ROADMAP, 'map_style']
                        }
                    };
                var map = new google.maps.Map(document.getElementById('google-map'), $mapOptions);

                google.maps.event.trigger(map, 'resize');

                //Associate the styled map with the MapTypeId and set it to display.
                map.mapTypes.set('map_style', styledMap);
                map.setMapTypeId('map_style');

                var marker = new google.maps.Marker({
                    position: $latlng,
                    map: map,
                    title: ""
                });

            }

        })();

        // Dropdown on Hover
        // $('.navbar .dropdown').hover(function() {
        //     $(this).find('.dropdown-menu').first().stop(true, true).slideDown(150);
        // }, function() {
        //     $(this).find('.dropdown-menu').first().stop(true, true).slideUp(105)
        // });


    });



    /* Google Analytics */
    (function (i, s, o, g, r, a, m) {
       i['GoogleAnalyticsObject'] = r;
       i[r] = i[r] || function () {(i[r].q = i[r].q || []).push(arguments)};
       i[r].l = 1 * new Date();
       a = s.createElement(o);
       m = s.getElementsByTagName(o)[0];
       a.async = 1;
       a.src = g;
       m.parentNode.insertBefore(a, m);
    })(window, document, 'script', '//www.google-analytics.com/analytics.js', 'ga');

    ga('create', 'UA-40696437-5', 'auto');
    ga('send', 'pageview');

})(jQuery);
