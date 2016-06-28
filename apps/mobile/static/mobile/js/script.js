/**
 * Created by alexy on 24.06.16.
 */
$(function() {
  $('#js-show-menu').click(function(){
    $('.navbar').slideToggle();
  });

  $('#js-show-search').click(function(){
    $('.form-search').slideToggle();
    $(this).find('.glyphicon-chevron-down').toggleClass('hide');
    $(this).find('.glyphicon-chevron-up').toggleClass('hide');
  });
  var client_photo_search_form = $('#js-client-photo-search-form');
  client_photo_search_form.find("#id_a_date_s").datepicker({
    defaultDate: 1,
    dateFormat: "dd.mm.yy"
  });
  client_photo_search_form.find("#id_a_date_e").datepicker({
    defaultDate: 1,
    dateFormat: "dd.mm.yy"
  });
  // получение списка районов по выбранному городу
  client_photo_search_form.find('#id_a_city').change(function(){
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
          client_photo_search_form.find('#id_a_area').find('option').remove();
          client_photo_search_form.find('#id_a_area').append($("<option/>", {
                value: '',
                text: 'Район'
            }));
          client_photo_search_form.find('#id_a_street').find('option').remove();
          client_photo_search_form.find('#id_a_street').append($("<option/>", {
              value: '',
              text: 'Улица'
          }));
          for (var i = 0; i < area_list.length; i++) {
            client_photo_search_form.find('#id_a_area').append($("<option/>", {
                value: area_list[i]['id'],
                text: area_list[i]['name']
            }));
          }
        }
      });
    } else {
      console.log('empty');
      client_photo_search_form.find('#id_a_area').find('option').remove();
      client_photo_search_form.find('#id_a_area').append($("<option/>", {
          value: '',
          text: 'Район'
      }));
      client_photo_search_form.find('#id_a_street').find('option').remove();
      client_photo_search_form.find('#id_a_street').append($("<option/>", {
          value: '',
          text: 'Улица'
      }));
    }
  });
  // получение списка улиц по выбранному району
  client_photo_search_form.find('#id_a_area').change(function(){
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
          client_photo_search_form.find('#id_a_street').find('option').remove();
          client_photo_search_form.find('#id_a_street').append($("<option/>", {
                value: '',
                text: 'Улица'
            }));
          for (var i = 0; i < street_list.length; i++) {
            client_photo_search_form.find('#id_a_street').append($("<option/>", {
                value: street_list[i]['id'],
                text: street_list[i]['name']
            }));
          }
        }
      });
    } else {
      console.log('empty');
      client_photo_search_form.find('#id_a_street').find('option').remove();
      client_photo_search_form.find('#id_a_street').append($("<option/>", {
          value: '',
          text: 'Улица'
      }));
    }
  });
});