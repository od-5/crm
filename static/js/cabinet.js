/**
 * Created by alexy on 28.05.15.
 */
$(function() {

  var current_url = '/'+location.href.split('/')[3]+'/' + location.href.split('/')[4] + '/';
  $('header ul li a').each(function () {
    if($(this).attr('href') == current_url) $(this).parent('li').addClass('active');
  });

  $.validator.messages.required = "* поле обязательно для заполнения";

  // валидация формы добавления города
  $( '#js-city-form' ).validate({
    rules: {
      name: {
        required: true
      }
    }
  });

  // валидация формы добавления администратора
  $( '.js-form-administrator-add' ).validate({
    rules: {
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
  // валидация формы изменения администратора
  $( '.js-form-administrator-change' ).validate({
    rules: {
      email: {
        required: true
      }
    }
  });
  // ajax удаление объектов
  var fancy_initial = function(){
    $('.js-ajax-remove-btn').fancybox({
      afterClose: function () {
        $('.js-ajax-remove-item-form').resetForm();
      },
      beforeLoad: function() {
        var item_id = '#' + this.element[0].id;
        var item = $(item_id);
        $('#js-ajax-item-remove-id').val(item.parents('tr').data('id'));
        $('#js-ajax-item-remove-name').text(item.parents('tr').data('name'));
        $('#js-ajax-item-remove-model').val(item.parents('tr').data('model'));
       }
    });
  };
  $('.js-list').on('click', '.js-ajax-remove-btn', function(){
    fancy_initial();
  });

  $('.js-ajax-remove-item-form').ajaxForm({
    success: function(data){
      if (data.id) {
        $.notify('Объект был удалён', 'success');
        $('#id_'+data.model+'_'+data.id).remove();
        $.fancybox.close();
      } else {
        $.notify('Произошла ошибка. Объект не удалён', 'error');
        $.fancybox.close();
      }
      $('.js-ajax-remove-item-form').resetForm();
    }
  });
  $('.js-ajax-remove-item-form input[type="reset"]').click(function(){
    $.fancybox.close();
  });
  $('.js-ajax-remove-item-form input[type="submit"]').click(function(){
    $.fancybox.close();
  });
  // открытие модального окна подтверждения удаления эдемента

  //$('.js-remove-item-btn').click(function(){
  //  console.log($(this).data('id'));
  //  $('#js-modal-item-remove-id').val($(this).data('id'));
  //  $('#js-modal-item-remove-name').text($(this).data('email'));
  //});
  if ($('.js-area-list')) {
    $('.js-area-list').on('click', '.js-remove-item-btn', function(){
      console.log($(this).data('id'));
      $('#js-modal-item-remove-id').val($(this).data('id'));
      $('#js-modal-item-remove-name').text($(this).data('email'));
    });
  } else {
    $('.js-remove-item-btn').click(function(){
      console.log($(this).data('id'));
      $('#js-modal-item-remove-id').val($(this).data('id'));
      $('#js-modal-item-remove-name').text($(this).data('email'));
    });
  }

  $('.js-remove-item-btn').fancybox({
    afterClose: function () {
      $('.js-modal-remove-item-form').resetForm();
    }
  });
  $('.js-modal-remove-item-form input[type="reset"]').click(function(){
    $.fancybox.close();
  });
  $('.js-modal-remove-item-form input[type="submit"]').click(function(){
    $.fancybox.close();
  });
  $('.js-modal-remove-item-form').ajaxForm({
    success: function(data){
      if (data.success) {
        $.notify('Объект был удалён', 'success');
        console.log(data.success);
        $('tr[data-id='+data.success+']').remove();
      } else {
        $.notify('Произошла ошибка. Объект не удалён', 'error');
      }
      $('.js-modal-remove-item-form').resetForm();
    }
  });


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

  // валидация формы добавления клиента
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
  // валидация формы добавления монтажника
  $( '.js-form-adjuster-add' ).validate({
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
  // валидация формы редактирования монтажника
  $( '.js-form-adjuster-update' ).validate({
    rules: {
      city: {
        required: true
      },
      email: {
        required: true
      }
    }
  });

  $(".js-gallery").fancybox();

//  фильтрация по городам на странице поверхностей
  var get_url = '/'+location.href.split('/');
  //$('header ul li a').each(function () {
  //  if($(this).attr('href') == current_url) $(this).parent('li').addClass('active');
  //});

  //$('#client_city_filter').change(function(){
  //  $('.client-search-form__city').val($(this).val());
  //  $('.client-search-form').submit();
  //});



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
  $('.js-calendar-heading').click(function(){
    $('.js-calendar-body').slideToggle();
  });
  $('.js-map-task-heading').click(function(){
    $('.js-map-task-body').slideToggle();
  });


    // валидация формы добвления фотографии поверхности
  $('#js-surface-photo-add-form').validate({
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

    // валидация формы изменения фотографии поверхности
  $('#js-surface-photo-update-form').validate({
    rules: {
      porch: {
        required: true
      },
      date: {
        required: true
      }
    }
  });


  $('#cas_area').change(function(){
    if ($(this).val() != 0){
      $.ajax({
        type: "GET",
        url: $(this).data('ajax-url'),
        data: {
          area: $(this).val(),
          client: $('#hidden_client').val()
        }
      }).done(function( data ) {
        if (data.surface_list) {
          var surface_list = data.surface_list;
          $('.js-surface-list tr.result').remove();
          var surface_table = $('.js-surface-list thead');
          for (var i = 0; i < surface_list.length; i++){
            surface_table.append(
              '<tr class="result">'+
              '<td><input type="checkbox" name="chk_group[]" value="' +surface_list[i]['id'] +'"></td>'+
              '<td>'+surface_list[i]['street']+'</td>'+
              '<td>'+surface_list[i]['number']+'</td>'+
              '</tr>'
            )
          }
        }
        //var street_list = msg.surfa;
        //surface_street.find('option').remove();
        //surface_street.append($("<option value selected='selected'>---------</option>"));
        //for (var i = 0; i < street_list.length; i++) {
        //  surface_street.append($("<option/>", {
        //      value: street_list[i]['id'],
        //      text: street_list[i]['name']
        //  }));
        //}
      });
    }

  });
  //удаление поверхности клиента
  function removeClientSurface(){
    $('.js-remove-client-surface').submit(function() {
      $(this).ajaxSubmit({
        success: function (data) {
          if (data.success) {
            $.notify('Поверхность удалена', 'success');
          } else {
            $.notify('Произошла ошибка!', 'error');
          }
        }
      });
      $(this).parents('tr').remove();
      return false;
    });
  }
  removeClientSurface();
 //валидация формы добвления поверхности к клиенту

  $('#js-order-surface-add-form').validate({
    rules: {
      cos_client: {
        required: true
      },
      cos_area: {
        required: true
      }
    }
  });

  $('#id_cos_area').change(function(){
    if ($(this).val() != 0){
      $.ajax({
        type: "GET",
        url: $(this).data('ajax-url'),
        data: {
          order: $(this).data('client-order'),
          area: $(this).val()
        }
      }).done(function( data ) {
        if (data.surface_list) {
          var surface_list = data.surface_list;
          $('.js-surface-list tr.result').remove();
          var surface_table = $('.js-surface-list thead');
          for (var i = 0; i < surface_list.length; i++){
            surface_table.append(
              '<tr class="result">'+
              '<td><input type="checkbox" name="chk_group[]" value="' +surface_list[i]['id'] +'"></td>'+
              '<td>'+surface_list[i]['street']+'</td>'+
              '<td>'+surface_list[i]['number']+'</td>'+
              '</tr>'
            )
          }
          $('#js-select-all').prop('checked', false);
          $('#js-select-all').on('click', function(){
            $('.js-surface-list tr.result input').prop('checked', $(this).prop('checked'));
          })
        }
      });
    }

  });







  $('#js-client-add-surface-form').validate({
    rules: {
      area: {
        required: true
      },
      date_start: {
        required: true
      }
    },
    submitHandler: function(e) {
      $('#js-client-add-surface-form').ajaxSubmit({
          success: function(data){
            if (data.success) {
              $.notify(data.success, 'success');
              $('#cas_area').val(0);
              $('.js-surface-list tr.result').remove();
              //$('#js-client-add-surface-form').trigger('reset');
              if (data.surface_list){
                //$.notify(data.surface_list, 'success');
                $('tr.empty').remove();
                var surface_list = data.surface_list;
                for (var i = 0; i < surface_list.length; i++) {
                  $('.js-surface-list-tbody').prepend(
                    '<tr>' +
                    '<td>' + surface_list[i]['id'] + '</td>' +
                    '<td>' + surface_list[i]['area'] + '</td>' +
                    '<td><a href="/city/surface/' + surface_list[i]['surface_id'] + '">' + surface_list[i]['surface'] + '</a></td>' +
                    '<td>' + surface_list[i]['date_start'] + '</td>' +
                    '<td>' + surface_list[i]['date_end'] + '</td>' +
                    '<td>' +
                      '<form action="/client/surface-remove/" method="post" class="js-remove-client-surface" role="form">' +
                      '<input type="hidden" name="client_surface_id" value="' + surface_list[i]['id'] + '">' +
                      '<button type="submit" class="btn btn-warning"><span class="glyphicon glyphicon-remove"></span> Удалить</button>' +
                      '</form>' +
                    '</td>' +
                    '</tr>'
                  );
                }
                //hz
                removeClientSurface();
              //  hz

              }
            } else {
              $.notify(data.error, 'error');
            }

          }
      });
    }
  });


    // валидация формы добвления клиента к поверхности
  $( '#js-surface-add-client-form' ).validate({
    rules: {
      client: {
        required: true
      },
      date_start: {
        required: true
      }
    }
  });

  // валидация формы добвления макета клиента
  $('#js-client-add-maket-form').validate({
    rules: {
      name: {
        required: true
      },
      file: {
        required: true
      },
      date: {
        required: true
      }
    }
  });
    // валидация формы изменения макета клиента
  $('#js-client-update-maket-form').validate({
    rules: {
      name: {
        required: true
      },
      date: {
        required: true
      }
    }
  });
  // валидация формы добавления заказа клиента
  $('#js-client-add-order-form').validate({
    rules: {
      client: {
        required: true
      },
      date_start: {
        required: true
      },
      date_end: {
        required: true
      }
    }
  });
   // валидация формы изменения заказа клиента
  $('#js-client-update-order-form').validate({
    rules: {
      client: {
        required: true
      },
      date_start: {
        required: true
      }
    }
  });
  // валидация формы формирования покупки клиента
  $('#js-client-journal-add-form').validate({
    rules: {
      client: {
        required: true
      },
      clientorder: {
        required: true
      },
      cost: {
        required: true
      }
    }
  });
  // логика работы формы добавления задачи по клиенту
  var act_form = $('#js-adjuster-client_task-add-form');
  // валидация формы добавления задачи по клиенту
  act_form.validate({
    rules: {
      adjuster: {
        required: true
      },
      type: {
        required: true
      },
      date: {
        required: true
      },
      client: {
        required: true
      },
      clientorder: {
        required: true
      }
    }
  });
  act_form.find('#id_client').change(function(){
    if ($(this).val().length){
      act_form.find('#clientorder_group').removeClass('hide');
      $.ajax({
        type: "GET",
        url: $(this).parent('#client_group').data('url'),
        data: {
          client: $(this).val()
        }
      }).done(function( data ) {
        if (data.success) {
          var order_list = data.order_list;
          console.log(order_list);
          act_form.find('#id_clientorder').find('option').remove();
          act_form.find('#id_clientorder').append($("<option/>", {
              value: '',
              text: '---------'
          }));
          for (var i = 0; i < order_list.length; i++) {
            act_form.find('#id_clientorder').append($("<option/>", {
                value: order_list[i]['id'],
                text: order_list[i]['name']
            }));
          }
        }
      });
    } else {
      act_form.find('#clientorder_group').addClass('hide');
      act_form.find('#id_clientorder').find('option').remove();
    //  TODO: очистить список заказов

    }
  });

  act_form.find('#id_clientorder').change(function(){
    $('.js-task-surface-list tr.result').remove();
    console.log($(this).val());
    $.ajax({
      type: "GET",
      url: $(this).parents('#clientorder_group').data('url'),
      data: {
        clientorder: $(this).val()
      }
    }).done(function( data ) {
      if (data.surface_list) {
        var surface_list = data.surface_list;
        console.log(surface_list);

        var surface_table = $('.js-task-surface-list');
        console.log(surface_table);
        for (var i = 0; i < surface_list.length; i++){
          surface_table.append(
            '<tr class="result">'+
            '<td><input type="checkbox" name="chk_group[]" value="' +surface_list[i]['id'] +'"></td>'+
            '<td>'+surface_list[i]['city']+'</td>'+
            '<td>'+surface_list[i]['area']+'</td>'+
            '<td>'+surface_list[i]['street']+'</td>'+
            '<td>'+surface_list[i]['number']+'</td>'+
            '<td>'+surface_list[i]['porch']+'</td>'+
            '</tr>'
          )
        }
        $('#js-select-all').prop('checked', false);
        $('#js-select-all').on('click', function(){
            act_form.find('tr.result input').prop('checked', $(this).prop('checked'));
        })
      }
    });
  });
  // валидация формы редактирования задачи по клиенту
  $('#js-adjuster-client_task-update-form').validate({
    rules: {
      adjuster: {
        required: true
      },
      type: {
        required: true
      },
      date: {
        required: true
      }
    }
  });

  // валидация формы добавления задачи по району
  var atf = $('#js-adjuster-task-add-form');
  atf.validate({
    rules: {
      city: {
        required: true
      },
      adjuster: {
        required: true
      },
      type: {
        required: true
      },
      date: {
        required: true
      },
      area: {
        required: true
      }
    }
  });
  atf.find('#id_city').change(function() {
    if ($(this).val().length){


      console.log($(this).val());
      // запрос на получение списка монтажников выбранного города
      $.ajax({
        type: "GET",
        url: $(this).parents('#city_group').data('adjuster-url'),
        data: {
          city: $(this).val()
        }
      }).done(function( data ) {
        if (data.success) {
          var adjuster_list = data.adjuster_list;
          console.log(adjuster_list);
          atf.find('#id_adjuster').find('option').remove();
          atf.find('#id_adjuster').append($("<option/>", {
                value: '',
                text: '---------'
            }));
          for (var i = 0; i < adjuster_list.length; i++) {
            atf.find('#id_adjuster').append($("<option/>", {
                value: adjuster_list[i]['id'],
                text: adjuster_list[i]['name']
            }));
          }
          atf.find('#id_adjuster').parents('.form-group').removeClass('hide');
        }
      });
      // запрос на получение списка районов выбранного города
      $.ajax({
        type: "GET",
        url: $(this).parents('#city_group').data('area-url'),
        data: {
          city: $(this).val()
        }
      }).done(function(data) {
        if (data.area_list) {
          var area_list = data.area_list;
          console.log(area_list);
          atf.find('#id_area').find('option').remove();
          atf.find('#id_area').append($("<option/>", {
                value: '',
                text: '---------'
            }));
          for (var i = 0; i < area_list.length; i++) {
            atf.find('#id_area').append($("<option/>", {
                value: area_list[i]['id'],
                text: area_list[i]['name']
            }));
          }
          atf.find('#id_area').parents('.form-group').removeClass('hide');
        }
      });
    }
    else {
      atf.find('#id_adjuster').parents('.form-group').addClass('hide');
      atf.find('#id_area').parents('.form-group').addClass('hide');
      atf.find('#id_adjuster').find('option').remove();
      atf.find('#id_area').find('option').remove();
      $('.js-task-surface-list tr.result').remove();
    //  TODO: очистить список заказов

    }
  });
  atf.find('#id_area').change(function(){
    $('.js-task-surface-list tr.result').remove();
    $.ajax({
      type: "GET",
      url: $(this).parents('#area_group').data('surface-url'),
      data: {
        area: $(this).val(),
        damaged: $(this).parents('#area_group').data('damaged')
      }
    }).done(function( data ) {
      if (data.surface_list) {
        var surface_list = data.surface_list;
        var surface_table = $('.js-task-surface-list');
        for (var i = 0; i < surface_list.length; i++){
          surface_table.append(
            '<tr class="result">'+
            '<td><input type="checkbox" name="chk_group[]" value="' +surface_list[i]['id'] +'"></td>'+
            '<td>'+surface_list[i]['city']+'</td>'+
            '<td>'+surface_list[i]['area']+'</td>'+
            '<td>'+surface_list[i]['street']+'</td>'+
            '<td>'+surface_list[i]['number']+'</td>'+
            '<td>'+surface_list[i]['porch']+'</td>'+
            '</tr>'
          )
        }
        $('#js-select-all').prop('checked', false);
        $('#js-select-all').on('click', function(){
            atf.find('tr.result input').prop('checked', $(this).prop('checked'));
        })
      }
    });
  });

  // валидация формы добавления района
  $( '#js-area-add-form' ).validate({
    rules: {
      city: {
        required: true
      },
      name: {
        required: true
      }
    }
  });

//  модальная форма редактирования района
    $('.js-area-list').on('click', '.js-update-item-btn', function(){
      $('#js-modal-item-update-id').val($(this).parents('tr').data('id'));
      $('#js-modal-item-update-name').val($(this).parents('tr').data('name'));
      console.log($(this));
    });

  $('.js-update-item-btn').fancybox({
    afterClose: function () {
      $('.js-modal-update-item-form').resetForm();
    }
  });
  $('.js-modal-update-item-form input[type="reset"]').click(function(){
    $.fancybox.close();
  });
  $('.js-modal-update-item-form input[type="submit"]').click(function(){
    $.fancybox.close();
  });
  $('.js-modal-update-item-form').ajaxForm({
    success: function(data){
      if (data.success) {
        $.notify('Объект был сохранён', 'success');
        console.log(data.name);
        $('td[data-id='+data.id+']').text(data.name);
        $('tr[data-id='+data.id+']').attr('data-name', data.name);
      } else {
        $.notify('Название района не может быть пустым', 'error');
      }
      $('.js-modal-update-item-form').resetForm();
    }
  });
  // Валидация формы добавления улицы
  $( '#js-street-add-form' ).validate({
    rules: {
      city: {
        required: true
      },
      area: {
        required: true,
      },
      name: {
        required: true
      }
    }
  });

  //  модальная форма редактирования улицы
  $('.js-street-list').on('click', '.js-update-street-btn', function(){
    $('#js-modal-street-update-id').val($(this).parents('tr').data('id'));
    $('#js-modal-street-update-name').val($(this).parents('tr').data('name'));
    console.log($(this).parents('tr').data('id'));
    console.log($(this).parents('tr').data('name'));
  });
  $('.js-update-street-btn').fancybox({
    afterClose: function () {
      $('.js-modal-update-street-form').resetForm();
    }
  });
  $('.js-modal-update-street-form input[type="reset"]').click(function(){
    $.fancybox.close();
  });
  $('.js-modal-update-street-form input[type="submit"]').click(function(){
    $.fancybox.close();
  });
  $('.js-modal-update-street-form').ajaxForm({
    success: function(data){
      if (data.success) {
        $.notify('Название улицы было изменено', 'success');
        console.log(data.name);
        $('td[data-id='+data.id+']').text(data.name);
        $('tr[data-id='+data.id+']').attr('data-name', data.name);
      } else {
        $.notify('Название улицы не может быть пустым', 'error');
      }
      $('.js-modal-update-street-form').resetForm();
    }
  });

  // Валидация формы добавления подъезда
  $('#js-porch-add-form').validate({
    rules: {
      surface: {
        required: true
      },
      number: {
        required: true
      }
    }
  });

//  форма поиска фотографий поверхностей на странице "Города"
  var aff = $('#js-address-filter-form');
  // получение списка районов по выбранному городу
  aff.find('#id_a_city').change(function(){
    if ($(this).val().length){
      console.log($(this).val());
      $.ajax({
        type: "GET",
        url: $(this).data('ajax-url'),
        data: {
          city: $(this).val()
        }
      }).done(function(data) {
        if (data.area_list) {
          var area_list = data.area_list;
          console.log(area_list);
          aff.find('#id_a_area').find('option').remove();
          aff.find('#id_a_area').append($("<option/>", {
                value: '',
                text: 'Район'
            }));
          aff.find('#id_a_street').find('option').remove();
          aff.find('#id_a_street').append($("<option/>", {
              value: '',
              text: 'Улица'
          }));
          for (var i = 0; i < area_list.length; i++) {
            aff.find('#id_a_area').append($("<option/>", {
                value: area_list[i]['id'],
                text: area_list[i]['name']
            }));
          }
        }
      });
    } else {
      console.log('empty');
      aff.find('#id_a_area').find('option').remove();
      aff.find('#id_a_area').append($("<option/>", {
          value: '',
          text: 'Район'
      }));
      aff.find('#id_a_street').find('option').remove();
      aff.find('#id_a_street').append($("<option/>", {
          value: '',
          text: 'Улица'
      }));
    }
  });
  // получение списка улиц по выбранному району
  aff.find('#id_a_area').change(function(){
    if ($(this).val().length){
      console.log($(this).val());
      $.ajax({
        type: "GET",
        url: $(this).data('ajax-url'),
        data: {
          area: $(this).val()
        }
      }).done(function(data) {
        if (data.street_list) {
          var street_list = data.street_list;
          console.log(street_list);
          aff.find('#id_a_street').find('option').remove();
          aff.find('#id_a_street').append($("<option/>", {
                value: '',
                text: 'Улица'
            }));
          for (var i = 0; i < street_list.length; i++) {
            aff.find('#id_a_street').append($("<option/>", {
                value: street_list[i]['id'],
                text: street_list[i]['name']
            }));
          }
        }
      });
    } else {
      console.log('empty');
      aff.find('#id_a_street').find('option').remove();
      aff.find('#id_a_street').append($("<option/>", {
          value: '',
          text: 'Улица'
      }));
    }
  });
  $('#js-photo-map-button').click(function(){
    $('#js-photo-map-wrapper').slideToggle()
  });

   // Валидация формы добавления подъезда
  $('#js-management-company-form').validate({
    rules: {
      city: {
        required: true
      },
      name: {
        required: true
      }
    }
  });

  // Валидация формы добавления задачи по входящему клиенту
  $('#js-form-incomingtask-add').validate({
    rules: {
      manager: {
        required: true
      },
      incomingclient: {
        required: true
      },
      type: {
        required: true
      },
      date: {
        required: true
      }
    }
  });
  // Валидация формы редактирования задачи по входящему клиенту
  $('#js-form-incomingtask-update').validate({
    rules: {
      manager: {
        required: true
      },
      incomingclient: {
        required: true
      },
      type: {
        required: true
      },
      date: {
        required: true
      }
    }
  });

  // Валидация формы дбавления менеджера
  $('#js-form-manager-add').validate({
    rules: {
      moderator: {
        required: true
      },
      email: {
        required: true
      },
      last_name: {
        required: true
      },
      first_name: {
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
  // Валидация формы редактирования менеджера
  $('#js-form-manager-update').validate({
    rules: {
      moderator: {
        required: true
      },
      email: {
        required: true
      },
      last_name: {
        required: true
      },
      first_name: {
        required: true
      }
    }
  });

//  модальное окно переназначения менеджера в crm
  $('#js-reassign-manager').fancybox();

  $('#js-reassign-manager').find('input[type="submit"]').click(function(){
    $.fancybox.close();
  });
  $('.js-modal-update-street-form').ajaxForm({
    success: function(data){
      if (data.success) {
        $.notify('Название улицы было изменено', 'success');
        console.log(data.name);
        $('td[data-id='+data.id+']').text(data.name);
        $('tr[data-id='+data.id+']').attr('data-name', data.name);
      } else {
        $.notify('Название улицы не может быть пустым', 'error');
      }
      $('.js-modal-update-street-form').resetForm();
    }
  });

});