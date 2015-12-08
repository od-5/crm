/**
 * Created by alexy on 28.05.15.
 */
$(function() {

  var current_url = '/'+location.href.split('/')[3]+'/';
  $('header ul li a').each(function () {
    if($(this).attr('href') == current_url) $(this).addClass('active');
  });

  $.validator.messages.required = "* поле обязательно для заполнения";


  $('#js-user-profile-form input[type="text"], #js-user-profile-form textarea').addClass('form-control');
//  Модальные окна
  $('#js-auth-button').fancybox();
  $('.js-ticket-button').fancybox({
    afterClose: function (e) {
      $('.ticket-modal-form').trigger('reset');
      $('.ticket-form').trigger('reset');
    }
  });
  $('a.documents-gallery').fancybox();
  $('a.photo-gallery').fancybox();
  $('a.js-page-gallery').fancybox();
  $('.review-slider').flexslider({
        animation: "slide",
        selector: ".review-slides > li",
        animationLoop: true,
        controlNav: false,
        //itemWidth: 800,
        itemMargin: 1,
        prevText: '<span class="glyphicon glyphicon-circle-arrow-left"></span>',
        nextText: '<span class="glyphicon glyphicon-circle-arrow-right"></span>'
    });

  // заполненяем поля модальной формы
  $('.js-ticket-button').on('click', function(e){
    var form = $(this).parent('form');

    if ($(this).data('excurse')){
      var excurse = $(this).data('excurse');
      //alert(group);
      //$('.ticket-modal-form__group').remove();
      $('.ticket-modal-form__excurse').val(excurse);
    }
    if ($(this).data('group')){
      var group = $(this).data('group');
      //alert(group);
      //$('.ticket-modal-form__excurse').remove();
      $('.ticket-modal-form__group').val(group);
    }

    if (form.length != 0) {
      var name = form.find('.ticket-form__name').val();
      var email = form.find('.ticket-form__email').val();
      $('.ticket-modal-form__name').val(name);
      $('.ticket-modal-form__email').val(email);
    }
  });

  $.validator.messages.required = "* поле обязательно для заполнения";

  // валидация формы на странице
  $( ".js-ticket-form" ).validate({
    rules: {
      name: {
        required: true
      },
      email: {
        required: true
      }
    },
    messages: {
      name: "Введите ваше имя",
      email: {
        required: "Введите ваш email для обратной связи",
        email: "e-mail должен быть вида name@domain.com"
      }
    },
    submitHandler: function(e) {
      $('.js-ticket-form').ajaxSubmit({
          success: function(data){
            console.log(data.success);
            $.notify(data.success, 'success');
            $('.js-ticket-form').trigger('reset');
          }
      });
    }
  });

  // валидация формы на странице
  $( ".js-modal-ticket-form").validate({
    rules: {
      name: {
        required: true
      },
      email: {
        required: true
      }
    },
    messages: {
      name: "Введите ваше имя",
      email: {
        required: "Введите ваш email для обратной связи",
        email: "e-mail должен быть вида name@domain.com"
      }
    },
    submitHandler: function(e) {
      $('.js-modal-ticket-form').ajaxSubmit({
          success: function(data){
            console.log(data.success);
            $.notify(data.success, 'success');
            $.fancybox.close();
            $('.js-modal-ticket-form').trigger('reset');
          }
      });
    }
  });

  // Валидация форм авторизации
  $( "#js-login-form" ).validate({
    rules: {
      username: {
        required: true
      },
      password: {
        required: true
      }
    },
    messages: {
      password: "Введите пароль",
      username: {
        required: "e-mail должен быть вида name@domain.com",
        email: "e-mail должен быть вида name@domain.com"
      }
    },
    submitHandler: function(e) {
      $('#js-login-form').ajaxSubmit({
          success: function(data){
            var error = data.error;
            if (error) {
              $('#js-login-form').trigger('reset');
              $.notify(error, 'error');
            } else {
              $.fancybox.close();
              location.reload(true);
            }
          }
      });
    }
  });

//  Валидация формы регитрации
  $( "#js-registration-form" ).validate({
    rules: {
      username: {
        required: true
      },
      password: {
        required: true
      }
    },
    messages: {
      password: "Введите пароль",
      username: {
        required: "e-mail должен быть вида name@domain.com",
        email: "e-mail должен быть вида name@domain.com"
      }
    },
    submitHandler: function(e) {
      $('#js-registration-form').ajaxSubmit({
          success: function(data){
            var error = data.error;
            if (error) {
              $('#js-registration-form').trigger('reset');
              $.notify(error, 'error');
            } else {
              $.notify(data.success, 'success');
              $.fancybox.close();
              location.reload(true);
            }
          }
      });
    }
  });

  // отправка формы комментария
  $( ".js-comment-form" ).validate({
    submitHandler: function(e) {
      $('.js-comment-form').ajaxSubmit({
          success: function(data){
            console.log(data.success);
            $.notify(data.success, 'success');
            $('.js-comment-form').trigger('reset');
            location.reload(true);
          }
      });
    }
  });


//  раскрытие текста блока "почему именно мы"
  $('.js-why-button__show').click(function(){
    $(this).parent().find('.why-ul-li__text').slideToggle();
    $(this).parent().find('.js-why-button__hide').toggle();
    $(this).toggle();
  });
  $('.js-why-button__hide').click(function(){
    $(this).parent().find('.why-ul-li__text').slideToggle();
    $(this).parent().find('.js-why-button__show').toggle();
    $(this).toggle();
  });

  $( "#slider-range" ).slider({
    range: true,
    min: $('.js-amount-button').data('min-price'),
    max: $('.js-amount-button').data('max-price'),
    values: [ $('.js-amount-button').data('min-price'), $('.js-amount-button').data('max-price') ],
    slide: function( event, ui ) {
      $("#amount").val( "$" + ui.values[ 0 ] + " - $" + ui.values[ 1 ] );
    },
    stop: function(event, ui) {
      $('.js-amount-button').attr('data-first', ui.values[0]);
      $('.js-amount-button').attr('data-second', ui.values[1]);
      var button_url = '?min=' + ui.values[0] + '&max=' + ui.values[1]
      $('.js-amount-button').attr('href', button_url);
    }
  });
  $("#amount").val( "$" + $( "#slider-range" ).slider( "values", 0 ) + " - $" + $( "#slider-range" ).slider( "values", 1 ) );
  if ($("#slider-range-days")){
    $( "#slider-range-days" ).slider({
      range: true,
      min: $('.js-amount-button').data('min-days'),
      max: $('.js-amount-button').data('max-days'),
      values: [ $('.js-amount-button').data('min-days'), $('.js-amount-button').data('max-days') ],
      slide: function( event, ui ) {
        $("#days").val( ui.values[ 0 ] + " - " + ui.values[ 1 ] );
      },
      stop: function(event, ui) {
        //$('.js-amount-button').attr('data-first', ui.values[0]);
        //$('.js-amount-button').attr('data-second', ui.values[1]);
        var button_url = '?dmin=' + ui.values[0] + '&dmax=' + ui.values[1]
        $('.js-amount-button').attr('href', button_url);
      }
    });
    $("#days").val( $( "#slider-range-days" ).slider( "values", 0 )+ " - " + $( "#slider-range-days" ).slider( "values", 1 ) );
  }

});