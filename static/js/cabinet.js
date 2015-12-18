/**
 * Created by alexy on 28.05.15.
 */
$(function() {

  var current_url = '/'+location.href.split('/')[3]+'/' + location.href.split('/')[4] + '/';
  $('header ul li a').each(function () {
    if($(this).attr('href') == current_url) $(this).parent('li').addClass('active');
  });

  $.validator.messages.required = "* поле обязательно для заполнения";

  // валидация формы на странице
  $( '.js-form-password-change' ).validate({
    rules: {
      user_id: {
        required: true
      },
      password1: {
        required: true
      },
      password2: {
        required: true
      },
    },
    submitHandler: function(e) {
      $('.js-form-password-change').ajaxSubmit({
          success: function(data){
            if (data.success) {
              $.notify(data.success, 'success');
            } else {
              $.notify(data.error, 'error');
            }
            $('.js-form-password-change').trigger('reset');
          }
      });
    }
  });

  // валидация формы добвления клиента
  $( '.js-form-client-add' ).validate({
    rules: {
      city: {
        required: true
      },
      email: {
        required: true
      },
      password1: {
        required: true
      },
      password2: {
        required: true
      }
    }
  });

  $(".js-gallery").fancybox();

//  фильтрация по городам на странице поверхностей
  var get_url = '/'+location.href.split('/');
  console.log(get_url);
  console.log(get_url.length);
  //$('header ul li a').each(function () {
  //  if($(this).attr('href') == current_url) $(this).parent('li').addClass('active');
  //});



  $('#city_filter').change(function(){
    $('.search-form__city').val($(this).val());
    $('.search-form__area').val(0);
    $('.search-form__street').val(0);
    $('.search-form').submit();
  });
  $('#area_filter').change(function(){
    $('.search-form__area').val($(this).val());
    $('.search-form__street').val(0);
    $('.search-form').submit();
  });
  $('#street_filter').change(function(){
    $('.search-form__street').val($(this).val());
    $('.search-form').submit();
    console.log($(this).val());
  });
  //$('#house_number_filter').change(function(){
  //  $('.search-form__house_number').val($(this).val())
  //  console.log($(this).val());
  //});


  // валидация формы добвления поверхности
  $( '#js-surface-add-form' ).validate({
    rules: {
      city: {
        required: true
      },
      street: {
        required: true
      },
      house_number: {
        required: true
      }
    }
  });

  var surface_add_form = $('#js-surface-add-form');
  var surface_city = surface_add_form.find('select#id_city');
  var surface_street = surface_add_form.find('select#id_street');
  surface_city.change(function(){
    console.log($(this).val());
    if($(this).val() == ''){
      var city = 0
    } else {
      var city = $(this).val();
    }

    $.ajax({
      type: "GET",
      url: surface_add_form.data('ajax-url'),
      data: {
        city: city
      }
    }).done(function( msg ) {
      var street_list = msg.street_list;
      surface_street.find('option').remove();
      surface_street.append($("<option value selected='selected'>---------</option>"));
      for (var i = 0; i < street_list.length; i++) {
        surface_street.append($("<option/>", {
            value: street_list[i]['id'],
            text: street_list[i]['name']
        }));
      }
    });
  });

  $('.js-show-map').click(function(){
    $('.js-map').slideToggle();
  });


    // валидация формы добвления фотографии поверхности
  $( '#js-surface-photo-add-form' ).validate({
    rules: {
      porch: {
        required: true
      },
      date: {
        required: true
      },
      image: {
        required: true
      }
    }
  });

    // валидация формы добвления поверхности к клиенту
  $( '#js-client-add-surface-form' ).validate({
    rules: {
      surface: {
        required: true
      },
      date: {
        required: true
      }
    }
  });
    // валидация формы добвления клиента к поверхности
  $( '#js-client-add-surface-form' ).validate({
    rules: {
      client: {
        required: true
      },
      date: {
        required: true
      }
    }
  });

});