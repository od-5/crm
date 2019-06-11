/**
 * Created by alexy on 24.02.16.
 */
$(function() {

  //  Добавление задачи для монтажника по клиенту
  var atc_form = $('#js-adjustertask-client-add');
  atc_form.validate({
    rules: {
      client: {
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
      clientorder: {
        required: true
      }
    }
  });
  // получение актуального списка монтажников и заказов в зависимости от выбранного клиента
  atc_form.find('#id_client').change(function(){
    var client = $(this).val();
    var ajax_url = $(this).parents('.form-group').data('ajax-url');
    console.log(ajax_url);
    if (client == '') {
      atc_form.find('#id_adjuster').parents('.form-group').addClass('hide');
      atc_form.find('#id_clientorder').parents('.form-group').addClass('hide');
    } else {
      atc_form.find('#id_adjuster').parents('.form-group').removeClass('hide');
      atc_form.find('#id_clientorder').parents('.form-group').removeClass('hide');
      $.ajax({
        type: "GET",
        url: ajax_url,
        data: {
          client: client
        }
      }).done(function(data) {
        // заполняем список монтажников
        console.log(data.adjuster_list);
        console.log(data.clientorder_list);
        var adjuster_selector = atc_form.find('#id_adjuster');
        adjuster_selector.find('option').remove();
        adjuster_selector.append($("<option value selected='selected'>--------</option>"));
        for (var i = 0; i < data.adjuster_list.length; i++) {
            adjuster_selector.append($("<option/>", {
            value: data.adjuster_list[i]['id'],
            text: data.adjuster_list[i]['name']
          }));
        }
        // заполняем список заказов
        var clientorder_selector = atc_form.find('#id_clientorder');
        clientorder_selector.find('option').remove();
        clientorder_selector.append($("<option value selected='selected'>--------</option>"));
        for (var j = 0; j < data.clientorder_list.length; j++) {
            clientorder_selector.append($("<option/>", {
            value: data.clientorder_list[j]['id'],
            text: data.clientorder_list[j]['name']
          }));
        }
      });
    }
  });
//  получение списка поверхностей по заказу клиента
  var get_order_client_surface_list = function() {
    $.ajax({
      type: "GET",
      url: atc_form.find('#id_clientorder').parents('.form-group').data('url'),
      data: {
        date: atc_form.find('#id_date').val(),
        clientorder: atc_form.find('#id_clientorder').val()
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
            '<td>'+surface_list[i]['intact_porch']+'</td>'+
            '<td>'+surface_list[i]['broken_porch']+'</td>'+
            '</tr>'
          )
        }
        var select_all_selector = $('#js-select-all');
        select_all_selector.prop('checked', false);
        select_all_selector.on('click', function(){
            atc_form.find('tr.result input').prop('checked', $(this).prop('checked'));
        })
      }
    });
  };
  atc_form.find('#id_clientorder').change(function(){
    $('.js-task-surface-list tr.result').remove();
    console.log($(this).val());
    get_order_client_surface_list();
  });
  atc_form.find('#id_date').change(function(){
    $('.js-task-surface-list tr.result').remove();
    console.log($(this).val());
    get_order_client_surface_list();
  });



  // валидация формы добавления задачи по району
  var ata_form = $('#js-adjustertask-area-add');
  console.log(ata_form);
  ata_form.validate({
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
  // получение и заполнение списков монтажников и районов
  ata_form.find('#id_city').change(function() {
    var city = $(this).val();
    var ajax_url = $(this).parents('.form-group').data('ajax-url');
    console.log(ajax_url);
    if (city == '') {
      ata_form.find('#id_adjuster').parents('.form-group').addClass('hide');
      ata_form.find('#id_area').parents('.form-group').addClass('hide');
    } else {
      ata_form.find('#id_adjuster').parents('.form-group').removeClass('hide');
      ata_form.find('#id_area').parents('.form-group').removeClass('hide');
      $.ajax({
        type: "GET",
        url: ajax_url,
        data: {
          city: city
        }
      }).done(function (data) {
        // заполняем список монтажников
        console.log(data.adjuster_list);
        console.log(data.area_list);
        var adjuster_selector = ata_form.find('#id_adjuster');
        adjuster_selector.find('option').remove();
        adjuster_selector.append($("<option value selected='selected'>--------</option>"));
        for (var i = 0; i < data.adjuster_list.length; i++) {
          adjuster_selector.append($("<option/>", {
            value: data.adjuster_list[i]['id'],
            text: data.adjuster_list[i]['name']
          }));
        }
        // заполняем список районов
        var area_selector = ata_form.find('#id_area');
        area_selector.find('option').remove();
        area_selector.append($("<option value selected='selected'>--------</option>"));
        for (var j = 0; j < data.area_list.length; j++) {
          area_selector.append($("<option/>", {
            value: data.area_list[j]['id'],
            text: data.area_list[j]['name']
          }));
        }
      });
    }
  });
//  получение списка поверхностей района города
  var get_area_surface_list = function() {
    $.ajax({
      type: "GET",
      url: ata_form.find('#id_area').parents('.form-group').data('surface-url'),
      data: {
        date: ata_form.find('#id_date').val(),
        area: ata_form.find('#id_area').val(),
        type: ata_form.find('#id_type').val()
      }
    }).done(function( data ) {
      if (data.surface_list) {
        var surface_list = data.surface_list;
        console.log(surface_list);
        var surface_table = $('.js-task-surface-list');
        console.log(surface_table);
        for (var i = 0; i < surface_list.length; i++){
          if (surface_list[i]['porch_id']){
                surface_table.append(
                '<tr class="result">'+
                '<td><input type="checkbox" name="chk_group2[]" value="' +surface_list[i]['porch_id'] +'"></td>'+
                '<td>'+surface_list[i]['city']+'</td>'+
                '<td>'+surface_list[i]['area']+'</td>'+
                '<td>'+surface_list[i]['street']+'</td>'+
                '<td>'+surface_list[i]['number']+'</td>'+
                '<td>'+surface_list[i]['porch']+'</td>'+
                '<td>'+surface_list[i]['intact_porch']+'</td>'+
                '<td>'+surface_list[i]['broken_porch']+'</td>'+
                '</tr>'
              )
          }
          else {
              surface_table.append(
                '<tr class="result">'+
                '<td><input type="checkbox" name="chk_group[]" value="' +surface_list[i]['id'] +'"></td>'+
                '<td>'+surface_list[i]['city']+'</td>'+
                '<td>'+surface_list[i]['area']+'</td>'+
                '<td>'+surface_list[i]['street']+'</td>'+
                '<td>'+surface_list[i]['number']+'</td>'+
                '<td>'+surface_list[i]['porch']+'</td>'+
                '<td>'+surface_list[i]['intact_porch']+'</td>'+
                '<td>'+surface_list[i]['broken_porch']+'</td>'+
                '</tr>'
              )
          }
        }
        var select_all_selector = $('#js-select-all');
        select_all_selector.prop('checked', false);
        select_all_selector.on('click', function(){
            ata_form.find('tr.result input').prop('checked', $(this).prop('checked'));
        })
      }
    });
  };

  ata_form.find('#id_area').change(function(){
    $('.js-task-surface-list tr.result').remove();
    console.log(ata_form.find('#id_area').val());
    console.log(ata_form.find('#id_date').val());
    get_area_surface_list();
  });
  ata_form.find('#id_date').change(function(){
    $('.js-task-surface-list tr.result').remove();
    console.log(ata_form.find('#id_area').val());
    console.log(ata_form.find('#id_date').val());
    get_area_surface_list();
  });

  // валидация формы добавления задачи на ремонт
  var atr_form = $('#js-adjustertask-repair-add');
  console.log(atr_form);
  atr_form.validate({
    rules: {
      city: {
        required: true
      },
      adjuster: {
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
  // получение и заполнение списков монтажников и районов
  atr_form.find('#id_city').change(function() {
    var city = $(this).val();
    $('.js-task-porch-list tr.result').remove();
    var ajax_url = $(this).parents('.form-group').data('ajax-url');
    console.log(ajax_url);
    if (city == '') {
      atr_form.find('#id_adjuster').parents('.form-group').addClass('hide');
      atr_form.find('#id_area').parents('.form-group').addClass('hide');
    } else {
      atr_form.find('#id_adjuster').parents('.form-group').removeClass('hide');
      atr_form.find('#id_area').parents('.form-group').removeClass('hide');
      $.ajax({
        type: "GET",
        url: ajax_url,
        data: {
          city: city
        }
      }).done(function (data) {
        // заполняем список монтажников
        console.log(data.adjuster_list);
        console.log(data.area_list);
        var adjuster_selector = atr_form.find('#id_adjuster');
        adjuster_selector.find('option').remove();
        adjuster_selector.append($("<option value selected='selected'>--------</option>"));
        for (var i = 0; i < data.adjuster_list.length; i++) {
          adjuster_selector.append($("<option/>", {
            value: data.adjuster_list[i]['id'],
            text: data.adjuster_list[i]['name']
          }));
        }
        // заполняем список районов
        var area_selector = atr_form.find('#id_area');
        area_selector.find('option').remove();
        area_selector.append($("<option value selected='selected'>--------</option>"));
        for (var j = 0; j < data.area_list.length; j++) {
          area_selector.append($("<option/>", {
            value: data.area_list[j]['id'],
            text: data.area_list[j]['name']
          }));
        }
      });
    }
  });
//  получение списка поверхностей (с поломками) района города
  var get_area_damaged_surface = function(){
    $.ajax({
      type: "GET",
      url: atr_form.find('#id_area').parents('.form-group').data('ajax-url'),
      data: {
        area: atr_form.find('#id_area').val(),
        date: atr_form.find('#id_date').val()
      }
    }).done(function( data ) {
      if (data.porch_list) {
        var porch_list = data.porch_list;
        console.log(porch_list);
        var porch_table = $('.js-task-porch-list');
      //  console.log(surface_table);
        for (var i = 0; i < porch_list.length; i++){
          porch_table.append(
            '<tr class="result">'+
            '<td><input type="checkbox" name="chk_group[]" value="' +porch_list[i]['id'] +'"></td>'+
            '<td>'+porch_list[i]['city']+'</td>'+
            '<td>'+porch_list[i]['area']+'</td>'+
            '<td>'+porch_list[i]['street']+'</td>'+
            '<td>'+porch_list[i]['house_number']+'</td>'+
            '<td>'+porch_list[i]['number']+'</td>'+
            '<td>'+porch_list[i]['type']+'</td>'+
            '</tr>'
          )
        }
        var select_all_selector = $('#js-select-all');
        select_all_selector.prop('checked', false);
        select_all_selector.on('click', function(){
            atr_form.find('tr.result input').prop('checked', $(this).prop('checked'));
        })
      }
    });
  };

  atr_form.find('#id_area').change(function(){
    $('.js-task-porch-list tr.result').remove();
    console.log($(this).val());
    get_area_damaged_surface()
  });
  atr_form.find('#id_date').change(function(){
    $('.js-task-porch-list tr.result').remove();
    console.log($(this).val());
    get_area_damaged_surface()
  });
});