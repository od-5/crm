/**
 * Created by alexy on 28.05.15.
 */
$(function() {

  var current_url = '/'+location.href.split('/')[3]+'/' + location.href.split('/')[4] + '/';
  $('header ul li a').each(function () {
    if($(this).attr('href') == current_url) $(this).parent('li').addClass('active');
  });

  $.validator.messages.required = "* поле обязательно для заполнения";

  // валидация админстраторской формы блока "почему реклама так эффективна"
  $('#js-block-effective-form').validate({
    rules: {
      text: {
        required: true
      }
    }
  });
  // валидация модераторской формы блока "почему реклама так эффективна"
  $( '#js-block-effective-form-moderator' ).validate({
    rules: {
      city: {
        required: true
      },
      text: {
        required: true
      }
    }
  });
  // валидация адмнистраторской формы блока "Примеры размещений"
  $( '#js-block-example-form' ).validate({
    rules: {
      name: {
        required: true
      }
    }
  });
  // валидация модераторской формы блока "Примеры размещений"
  $( '#js-block-example-form-moderator' ).validate({
    rules: {
      city: {
        required: true
      },
      name: {
        required: true
      }
    }
  });
  // валидация администраторской формы блока "Отзывы"
  $( '#js-block-review-form' ).validate({
    rules: {
      name: {
        required: true
      },
      description: {
        required: true
      },
      text: {
        required: true
      }
    }
  });
  // валидация модераторской формы блока "Отзывы"
  $( '#js-block-review-form-moderator' ).validate({
    rules: {
      city: {
        required: true
      },
      name: {
        required: true
      },
      description: {
        required: true
      },
      text: {
        required: true
      }
    }
  });


  // валидация формы авторизации
  $( '#js-sign-form' ).validate({
    rules: {
      username: {
        required: true
      },
      password: {
        required: true
      }
    }
  });

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
  //$('.js-form-administrator-change input[type=checkbox]').
  // валидация формы изменения администратора
  $( '.js-form-administrator-change' ).validate({
    rules: {
      email: {
        required: true
      }
    }
  });
  // валидация формы добавления оплаты
  $( '.js-modal-payment-add-form' ).validate({
    rules: {
      p_client: {
        required: true
      },
      p_clientjournal: {
        required: true
      },
      p_sum: {
        required: true,
        number: true
      }
    }
  });
  // форма добавления оплаты
  $('.js-payment-add-btn').fancybox({
    afterClose: function () {
      $('.js-modal-payment-add-form').resetForm();
    },
    beforeLoad: function() {
      var item_id = '#' + this.element[0].id;
      var item = $(item_id);
      var form = $('.js-modal-payment-add-form');
      console.log(item);
      console.log(item.data('client'));
      console.log(item.data('clientjournal'));
      form.find('#p_client').val(item.data('client'));
      form.find('#p_clientjournal').val(item.data('clientjournal'));
      console.log('client' + form.find('#p_client').val());
      console.log('clientjournal' + form.find('#p_clientjournal').val());
     }
  });
  $('.js-modal-payment-add-form').ajaxForm({
    success: function (data) {
      if (data.success) {
        $.notify('Оплата сохранена. Идёт пересчёт поступлений.', 'success');
        $.fancybox.close();
        location.reload();
      } else {
        $.notify('Произошла ошибка. Оплата не сохранена', 'error');
        $.fancybox.close();
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
        console.log($('#id_'+data.model+'_'+data.id));
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

  $(".js-gallery").fancybox({
    helpers: {
      overlay: {
        locked: false
      }
    }
  });

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

  // Редактирование заказа. Выбор поверхностей по району
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
          var surface_table = $('.js-surface-list tbody');
          for (var i = 0; i < surface_list.length; i++){
            surface_table.append(
              '<tr class="result">'+
              '<td><input type="checkbox" data-porch-count="'+surface_list[i]['porch_count']+'" name="chk_group[]" value="' +surface_list[i]['id'] +'"></td>'+
              '<td>'+surface_list[i]['street']+'</td>'+
              '<td>'+surface_list[i]['number']+'</td>'+
              '<td>'+surface_list[i]['porch_count']+'</td>'+
              '</tr>'
            )
          }


          $('#js-select-all').prop('checked', false);
          $('#js-select-all').on('click', function(){
            $('.js-surface-list tr.result input').prop('checked', $(this).prop('checked'));
          });
          // Редактирование заказа. Вывод количества стендов по выбранным поверхностям

          $('.js-surface-list input[type="checkbox"]').on('click', function(){
            var porch_count = 0;
            $('.js-surface-list tbody input[type="checkbox"]:checked').each(function(){
              porch_count += $(this).data('porch-count');
            });
            //porch_count = $('.js-surface-list tbody input[type="checkbox"]:checked').length;
            $('#js-selected-surface-porch-count').text(porch_count);
          });
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
  $('#js-client-journal-add-form').find('input[type=checkbox]').removeClass('form-control');
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
  var reassign_manager_form = $('#js-reassign-manager-form');
  var reassign_fancy_initial = function() {
    $('.js-reassign-manager').fancybox({
      afterClose: function () {
        $('.js-reassign-manager-form').resetForm();
      },
      beforeLoad: function () {
        var item_id = '#' + this.element[0].id;
        var item = $(item_id);
        var manager_name = item.parents('td').attr('data-manager-name');
        //var manager_name = item.prev('.js-manager-name').text();
        console.log('Сейчас менеджер: ' + manager_name);
        var manager_id = item.parents('td').attr('data-manager-id');
        var client = item.parents('tr').attr('data-id');
        reassign_manager_form.find('input[name=manager_name]').val(manager_name);
        reassign_manager_form.find('input[name=manager]').val(manager_id);
        reassign_manager_form.find('input[name=incomingclient]').val(client);
        $.ajax({
          type: "GET",
          data: {
            manager: item.parents('td').data('manager-id')
          },
          url: item.parents('td').data('url')
        }).done(function (data) {
          var manager_list = data.manager_list;
          var manager_list_selector = $('#js-manager-list');
          manager_list_selector.find('option').remove();
          manager_list_selector.append($("<option value selected='selected'>---------</option>"));
          for (var i = 0; i < manager_list.length; i++) {
            manager_list_selector.append($("<option/>", {
              value: manager_list[i]['id'],
              text: manager_list[i]['name']
            }));
          }
        });
        //$('#js-ajax-item-remove-id').val(item.parents('tr').data('id'));
        //$('#js-ajax-item-remove-name').text(item.parents('tr').data('name'));
        //$('#js-ajax-item-remove-model').val(item.parents('tr').data('model'));
      }
    });
  };
  $('.js-list').on('click', '.js-reassign-manager', function(){
    reassign_fancy_initial();
  });
  //reassign_manager_form.find('input[type="submit"]').click(function(){
  //  $.fancybox.close();
  //});
  reassign_manager_form.validate({
    rules: {
      manager: {
        required: true
      },
      new_manager: {
        required: true
      }
    }
  });
  reassign_manager_form.ajaxForm({
    success: function(data){
      if (data.success) {
        $.notify('Менеджер был переназначен', 'success');
        console.log('Старый менеджер' + data.old_id);
        console.log('новый менеджер' + data.id);
        console.log(data.name);
        var td_selector = $('tr[data-id="' + data.incomingclient_id +'"] td[data-manager-id="'+data.old_id+'"]');
        console.log(td_selector);
        td_selector.find('.js-manager-name').text(data.name);
        td_selector.attr('data-manager-id', data.id);
        td_selector.attr('data-manager-name', data.name);
        $.fancybox.close();
      } else {
        $.notify('Произошла ошибка. Возможно вы не выбрали нового менеджера', 'error');
      }
      reassign_manager_form.resetForm();
      //reassign_fancy_initial();
    }
  });

  //$('.js-show-incomingclient-contact').fancybox();
  $('.js-show-incomingclient-contact').fancybox({
      afterClose: function () {
        $('#js-incomingclient-contact-list').html('');
      },
      beforeLoad: function () {
        var item_id = '#' + this.element[0].id;
        var item = $(item_id);
        console.log(item.data('incomingclient'));

        $.ajax({
          type: "GET",
          url: item.data('url'),
          data: {
            incomingclient: item.data('incomingclient')
          }
        }).done(function (data) {
          if (data.contact_list) {
            var contact_list = data.contact_list;
            //var manager_list_selector = $('#js-manager-list');
            //manager_list_selector.find('option').remove();
            //manager_list_selector.append($("<option value selected='selected'>---------</option>"));
            for (var i = 0; i < contact_list.length; i++) {
              $('#js-incomingclient-contact-list').append(
                '<tr>' +
                '<td>' + contact_list[i]['name'] +
                '</td><td>' + contact_list[i]['function'] +
                '</td><td>' + contact_list[i]['phone'] +
                '</td><td>' + contact_list[i]['email'] +
                '</td>' +
                '</tr>'
              );
              console.log(contact_list[i]['name']);
              console.log(contact_list[i]['function']);
              console.log(contact_list[i]['phone']);
              console.log(contact_list[i]['email']);
            }
          } else {
            $('#js-incomingclient-contact-list').html('<tr><td colspan="4">Контактных лиц не найдено</td></tr>');
          }
        });
      }
    });

//  модальное окно формы создания задачи по клиенту
  $('.js-new-incomingtask-btn').fancybox({
    beforeLoad: function () {
      var item_id = '#' + this.element[0].id;
      var item = $(item_id);
      console.log(item.parents('tr').data('id'));
      $.ajax({
        type: "GET",
        url: item.data('url'),
        data: {
          incomingclient: item.parents('tr').data('id')
        }
      }).done(function (data) {
        console.log(data.id);
        console.log(data.type);
        console.log(data.name);
        var form = $('#js-incomingtask-modal-add-form');
        form.find('#id_incomingclient_type').text(data.type);
        form.find('#id_incomingclient_name').text(data.name);
        form.find('#id_incomingclient_id').val(data.id);
        var contact_list = data.contact_list;
        var contact_list_selector = form.find('#id_incomingclient_contact');
        contact_list_selector.find('option').remove();
        contact_list_selector.append($("<option value selected='selected'>---------</option>"));
        for (var i = 0; i < contact_list.length; i++) {
          contact_list_selector.append($("<option/>", {
            value: contact_list[i]['id'],
            text: contact_list[i]['name']
          }));
        }
      });
    }
  });
  $('#js-incomingtask-modal-add-form').ajaxForm({
    success: function(data){
      if (data.success) {
        $.notify('Задача по клиенту добавлена', 'success');
        $.fancybox.close();
      }
    }
  });
//  валидация модальной формы создания задачи
  $('#js-incomingtask-modal-add-form').validate({
    rules: {
      manager: {
        required: true
      },
      incomingclient: {
        required: true
      },
      incomingclient_contact: {
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

  // валидация формы редактирования задачи
  var validator = $('#js-incomingtask-modal-update-form').validate({
    rules: {
      incomingclient_contact: {
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
  // валидация формы редактирования задачи
  var client_modal_validator = $('#js-ajax-client-add').validate({
    rules: {
      email: {
        required: true
      },
      password: {
        required: true
      }
    }
  });
  //  модальное окно формы редактирования задачи по клиенту
  $('.js-change-incomingtask-btn').fancybox({
    afterClose: function () {
      validator.resetForm();
      client_modal_validator.resetForm();
    },
    beforeLoad: function () {
      var item_id = '#' + this.element[0].id;
      var item = $(item_id);
      console.log(item);
      console.log(item.parents('tr').data('id'));
      $.ajax({
        type: "GET",
        url: item.data('url'),
        data: {
          incomingtask: item.parents('tr').data('id')
        }
      }).done(function (data) {
        console.log('id задачи' + data.incomingtask_id);
        console.log('id клиента' + data.incomingclient_id);
        console.log('название клиента' + data.incomingclient_name);
        console.log('тип клиента' + data.incomingclient_type);
        console.log('id менеджера' + data.manager_id);
        console.log('список контактных лиц' + data.contact_list);
        var form = $('#js-incomingtask-modal-update-form');
        form.find('#id_incomingclient_type').text(data.incomingclient_type);
        form.find('#id_incomingclient_name').text(data.incomingclient_name);
        form.find('#id_incomingclient').val(data.incomingclient_id);
        form.find('#id_incomingtask').val(data.incomingtask_id);
        form.find('#id_manager').val(data.manager_id);
        var contact_list = data.contact_list;
          var contact_list_selector = form.find('#id_incomingclient_contact');
          contact_list_selector.find('option').remove();
          contact_list_selector.append($("<option value>---------</option>"));
          for (var i = 0; i < contact_list.length; i++) {
            contact_list_selector.append($("<option/>", {
              value: contact_list[i]['id'],
              text: contact_list[i]['name']
            }));
          }
      });
    }
  });
  // ajax форма редактирования задачи
  $('#js-incomingtask-modal-update-form').ajaxForm({
    success: function(data){
      if (data.success) {
        $.notify('Задача по клиенту обновлена', 'success');
        $.fancybox.close();
        location.reload();
      } else {
        $.notify('Произошла ошибка', 'error');
      }
    }
  });

  $('#js-ajax-sale-add').on('click', function(){
    console.log('ПРОДАЖА!');
    var form = $('#js-incomingtask-modal-update-form');
    var manager = form.find('#id_manager').val();
    console.log(manager);
    var incomingclient = form.find('#id_incomingclient').val();
    console.log(incomingclient);
    var comment = form.find('#id_comment').val();
    console.log(comment);
    var date = form.find('#id_date').val();
    console.log(date);
    var incomingcontact = form.find('#id_incomingclient_contact').val();
    console.log(incomingcontact);
    var incomingtask = form.find('#id_incomingtask').val();
    console.log(incomingtask);
    var incomingclient_type = form.find('#id_incomingclient_type').text();
    console.log(incomingclient_type);
    var incomingclient_name = form.find('#id_incomingclient_name').text();
    console.log(incomingclient_name);

    var c_form = $('#js-ajax-client-add');
    c_form.find('#id_incomingclient').val(incomingclient);
    c_form.find('#id_manager').val(manager);
    c_form.find('#id_incomingtask').val(incomingtask);
    c_form.find('#id_comment').val(comment);
    c_form.find('#id_date').val(date);
    c_form.find('#id_incomingcontact').val(incomingcontact);
    c_form.find('#id_client_name').text(incomingclient_name);
    c_form.find('#id_client_type').text(incomingclient_type);


    $('.client-modal-add-form').toggle();
    $('.incomingtask-modal-update-form').toggle();
    $('.incomingtask-modal-text').toggle();
    $('.client-modal-add-text').toggle();

  });
  $('#js-back-to-incomingtask-modal-update-form').on('click', function(){
    $('.client-modal-add-form').toggle();
    $('.incomingtask-modal-update-form').toggle();
    $('.incomingtask-modal-text').toggle();
    $('.client-modal-add-text').toggle();
  });
  // ajax форма редактирования задачи
  //$('#js-ajax-client-add').ajaxForm({
  //  success: function (data) {
  //    if (data.error) {
  //      $.notify('Клиент с таким e-mail уже зарегистрирован в системе', 'error');
  //      $.fancybox.close();
  //    }
  //  }
  //});
  var ia_form = $('#js-form-incomingtask-add');
  ia_form.find('#id_incomingclient').change(function(){
    var client = $(this).val();
    var url = $(this).parents('.form-group').data('url');
    console.log(url);
    var clientcontact_selector = ia_form.find('#id_incomingclientcontact');
    if (client) {
      console.log(client);
      clientcontact_selector.parents('.form-group').removeClass('hide');
      $.ajax({
        type: "GET",
        url: url,
        data: {
          incomingclient: client
        }
      }).done(function (data) {
        if (data.contact_list) {
          var contact_list = data.contact_list;
          console.log(contact_list);
          clientcontact_selector.find('option').remove();
          clientcontact_selector.append($("<option value selected='selected'>---------</option>"));
          for (var i = 0; i < contact_list.length; i++) {
            clientcontact_selector.append($("<option/>", {
              value: contact_list[i]['id'],
              text: contact_list[i]['name']
            }));
          }

        } else {
          clientcontact_selector.find('option').remove();
        }
      });
    } else {
      console.log('empty');
      clientcontact_selector.find('option').remove();
      clientcontact_selector.parents('.form-group').addClass('hide');
    }
  });
  $('#js-page-count').change(function(){
    console.log($(this).parents('form'));
    $('#id_page_count').val($(this).val());
    $(this).parents('form').submit();
  });
  $('.js-show-loader').click(function() {
    $('.loader').show();
  });
  $('.clientjournal-tr').hover(
    function(){
      $(this).find('.js-payment-add-btn').removeClass('hide');
    },
    function() {
      $(this).find('.js-payment-add-btn').addClass('hide')
    }
  );
  $('.js-show-order-list').click(function(){
    $(this).parents('td').find('.journal-order-list').toggleClass('hide');
    $(this).parents('td').find('.order-first').hide();
    $(this).hide();
  });
  $('.js-hide-order-list').click(function(){
    $(this).parents('.journal-order-list').toggleClass('hide');
    $(this).parents('td').find('.js-show-order-list').show();
    $(this).parents('td').find('.order-first').show();
  });

  var table_report = $('.js-table-report');
  table_report.find('#js-select-all');
  table_report.find('#js-select-all').on('click', function(){
      table_report.find('tbody input[type=checkbox]').prop('checked', $(this).prop('checked'));
  });

//  поворот фотографий
  $('.js-photo-rotate__button').click(function(){
    var block = $(this).parents('.photo-list-block');
    var image = block.find('img');
    var button = block.find('.js-photo-save__button');
    button.show();
    var angle = parseInt(button.attr('data-angle')) + 90;
    //console.log(angle);
    button.attr('data-angle', angle);
    image.css("transform", "rotate("+angle+"deg)");
  });
  $('.js-photo-save__button').click(function(){
    $('.rotate').show();
    //$(document).off("click.js-galley");
    var button = $(this);
    var link = button.parents('.photo-list-block').find('a');
    var img = link.find('img');
    //console.log($(this).attr('data-angle'));
    $.ajax({
      type: "POST",
      url: $(this).data('url'),
      data: {
        id: $(this).data('id'),
        angle: $(this).attr('data-angle')
      }
    }).done(function (data) {
      if (data.success) {
        $('.rotate').hide();
        link.attr('href', data.image);
        img.attr('src', data.image_resize);
        button.attr('data-angle', 0);
        img.css("transform", "rotate(0deg)");
      } else {
        alert('FAIL');
      }
    });
  });

});