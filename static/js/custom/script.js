/**
 * Created by alexy on 28.01.16.
 */
$(function() {
//  форма поиска поверхностей на странице списка поверхностей
  $('#city_filter').change(function(){
    console.log($(this).val());
    if ($(this).val() != 0){
      // запрос на получение списка районов выбранного города
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
          $('#area_filter').find('option').remove();
          $('#area_filter').append($("<option/>", {
            value: '',
            text: 'Район'
          }));
          for (var i = 0; i < area_list.length; i++) {
            $('#area_filter').append($("<option/>", {
                value: area_list[i]['id'],
                text: area_list[i]['name']
            }));
          }
        }
        if (data.management_list){
          var management_list = data.management_list;
          $('#management_filter').find('option').remove();
          $('#management_filter').append($("<option/>", {
            value: '',
            text: '--- Управляющая компания ---'
          }));
          for (var i = 0; i < management_list.length; i++) {
            $('#management_filter').append($("<option/>", {
                value: management_list[i]['id'],
                text: management_list[i]['name']
            }));
          }
        }
        if (data.clientorder_list){
          var clientorder_list = data.clientorder_list;
          $('#client_filter').find('option').remove();
          $('#client_filter').append($("<option/>", {
            value: '',
            text: '--- Клиент ---'
          }));
          for (var i = 0; i < clientorder_list.length; i++) {
            $('#client_filter').append($("<option/>", {
                value: clientorder_list[i]['id'],
                text: clientorder_list[i]['name']
            }));
          }
        }
        $('#street_filter').find('option').remove();
        $('#street_filter').append($("<option/>", {
          value: '',
          text: 'Улица'
        }));

      });
    } else {
      $('#area_filter').find('option').remove();
      $('#area_filter').append($("<option/>", {
        value: '',
        text: 'Район'
      }));
      $('#street_filter').find('option').remove();
      $('#street_filter').append($("<option/>", {
        value: '',
        text: 'Улица'
      }));
    }
  });

  $('#area_filter').change(function(){
    console.log($(this).val());
    if ($(this).val() != 0){
      // запрос на получение списка районов выбранного города
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
          $('#street_filter').find('option').remove();
          $('#street_filter').append($("<option/>", {
            value: '',
            text: 'Улица'
          }));
          for (var i = 0; i < street_list.length; i++) {
            $('#street_filter').append($("<option/>", {
                value: street_list[i]['id'],
                text: street_list[i]['name']
            }));
          }
        }
      });
    } else {
      $('#street_filter').find('option').remove();
      $('#street_filter').append($("<option/>", {
        value: '',
        text: 'Улица'
      }));
    }
  });
  $('#street_filter').change(function(){
    console.log($(this).val());
  })

});
