/**
 * Created by alexy on 18.05.16.
 */
ymaps.ready(function () {
  var surface_list = '';
  var map_block = $('.js-map');
  var url = map_block.data('url');
  var coord_x = map_block.data('coord-x');
  var coord_y = map_block.data('coord-y');
  var center = [coord_y.replace(',','.'), coord_x.replace(',','.')];
  var map_zoom = 3;
  var management = $('#management_filter').val();
  var city = $('#city_filter').val();
  var area = $('#area_filter').val();
  var street = $('#street_filter').val();
  var release_date = $('#id_release_date').val();
  var free = $('#free_filter').val();
  var city_count = map_block.data('city-count');
  if (city_count == 1){
    map_zoom = 9;
  }
  if (city != '0') {
    map_zoom = 9;
  }
  $.ajax({
    type: "POST",
    async: false,
    url: url,
    data: {
      management: management,
      city: city,
      area: area,
      street: street,
      release_date: release_date,
      free: free
    }
  }).done(function (data) {
    if (data.surface_list.length){
      surface_list = data.surface_list;
    }
  });
    var myMap = new ymaps.Map('surfaceMap', {
      center: center,
      zoom: map_zoom,
      behaviors: ['default', 'scrollZoom']
    }, {
      searchControlProvider: 'yandex#search'
    }),
      clusterer = new ymaps.Clusterer({
      preset: 'islands#invertedVioletClusterIcons',
      groupByCoordinates: false,
      clusterDisableClickZoom: true,
      clusterHideIconOnBalloonOpen: false,
      geoObjectHideIconOnBalloonOpen: false
    }),
      getPointData = function (index) {
      return {
          balloonContentBody: '<span>Адрес: ' + surface_list[index]['name'] + '. Кол-во подъездов' + surface_list[index]['porch_count'] + '</span>',
          clusterCaption: '<span>Адрес: ' + surface_list[index]['name'] + '. Кол-во подъездов' + surface_list[index]['porch_count'] + '</span>'
      };
    },
      getPointOptions = function () {
      return {
          preset: 'islands#violetIcon'
      };
    },
    geoObjects = [];
    for(var i = 0, len = surface_list.length; i < len; i++) {
        geoObjects[i] = new ymaps.Placemark([surface_list[i]['coord_y'], surface_list[i]['coord_x']], getPointData(i), getPointOptions());
    }
    clusterer.options.set({
        gridSize: 80,
        clusterDisableClickZoom: true
    });
    clusterer.add(geoObjects);
    myMap.geoObjects.add(clusterer);

    //myMap.setBounds(clusterer.getBounds(), {
    //    checkZoomRange: true
    //});
});