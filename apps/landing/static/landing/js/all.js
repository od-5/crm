$(document).ready(function () {

  $('.styled').selectmenu();
  // fancybox
  $('.fancybox').fancybox();
  $(".input[name='phone']").mask("+7 (999) 999-99-99");
  $('form').each(function(){
    $(this).validate({
      rules: {
         name: {
           required: true
         },
         text: {
           required: true
         },
         mail: {
           required: true,
           email: true
         },
         phone: {
           required: true,
           minlength: 6
         },
         terms: {
           required: true
         }
      },
      messages: {
        name: false,
        phone: false,
        text: false,
        mail: false,
        terms: 'Вы не можете оставить заявку без согласия на обработку персональных данных'
      }
    });
  });
  // $('form').ajaxForm({
  //   success: function(data){
  //     var error = data.error;
  //     if (error) {
  //       $('form').resetForm();
  //       $.notify('Сообщение не было отправлено. Проверьте правильность ввода данных!', 'error');
  //       console.log(error);
  //     } else {
  //       $('form').resetForm();
  //       $('#mask, .window').hide();
  //       $.notify('Ваше сообщение успешно отправлено!', 'success');
  //       console.log('not error');
  //     }
  //   }
  // });

  // slider
  $('.slider').bxSlider({
    pause: 5000,
    auto: false,
    pager: false,
    prevText: '',
    nextText: '',
    adaptiveHeight: true,
    controls: true
    //autoHover: true
  });

  // city hidden
  $(document).on('click','.select-top',function(e){
    e.preventDefault();
    if($(this).hasClass('active')){
      $(this).removeClass('active');
      $(this).next('.select-hidden').slideUp();
    }else{
      $('.select-top').removeClass('active');
      $('.select-hidden').slideUp();
      $(this).addClass('active');
      $(this).next('.select-hidden').slideDown();
    }
  });

  // part hover
  $(document).on({
    mouseenter: function () {
      var part = $(this).attr('data-part');
      $('.'+part).addClass('hover');
    },
    mouseleave: function () {
      var part = $(this).attr('data-part');
      $('.'+part).removeClass('hover');
    }
  }, '.link a');

  // city hidden
  $(document).on('click','.city-button',function(e){
    e.preventDefault();
    if($(this).hasClass('active')){
      $(this).removeClass('active');
      $('.city-hidden').slideUp();
    }else{
      $(this).addClass('active');
      $('.city-hidden').slideDown();
    }
  });

  // gallery hidden
  $(document).on('click','.gallery-more',function(e){
    e.preventDefault();
    $(this).hide();
    $('.last').show();
    $('.gallery-hidden').show();
  });
  $(document).on('click','.gallery-hide',function(e){
    e.preventDefault();
    $('.last').hide();
    $('.gallery-more').show();
    $('.gallery-hidden').hide();
  });


  //Скрипт всплывающих окон
  $('.modal').click(function(e) {
    e.preventDefault();
    $('#mask, .window').hide();
    var id = $(this).attr('href');
    var maskHeight = $(document).height();
    var maskWidth = $(window).width();
    $('#mask').css({'height':maskHeight});
    $('#mask').fadeTo("slow",0.9);
    var winH = $(window).height();
    var winW = $(window).width();
    $(id).css('top',  winH/2-$(id).height()/2);
    $(id).css('left', winW/2-$(id).width()/2);
    $(id).fadeIn(1000);
  });
  $('.window .close').click(function (e) {
    e.preventDefault();
    $('#mask, .window').hide();
  });
  $('#mask').click(function () {
    $(this).hide();
    $('.window').hide();
  });
  //Скрипт всплывающих окон

  // animation trigger

    $(window).scroll( function(e){
      var document_top = $(document).scrollTop();
      var height = $(window).height();

      var tablet_offset = $('.video-tablet').offset().top - height + height/4;

      if (document_top > tablet_offset){
        $('.video-tablet').addClass('vis');
      };

    });

});


