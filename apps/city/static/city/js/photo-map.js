ymaps.ready(function () {
  var photo_list = '';
  var map_block = $('#photoMap');
  var url = map_block.data('url');
  var city = $('#id_a_city').val();
  var area = $('#id_a_area').val();
  var street = $('#id_a_street').val();
  var date_s = $('#id_a_date_s').val();
  var date_e = $('#id_a_date_e').val();
  $.ajax({
    type: "POST",
    async: false,
    url: url,
    data: {
      city: city,
      area: area,
      street: street,
      date_s: date_s,
      date_e: date_e
    }
  }).done(function (data) {
    if (data.photo_list.length){
      photo_list = data.photo_list;
    }
  });
  center = [photo_list[0]['coord_y'], photo_list[0]['coord_x']];
  var myMap = new ymaps.Map('photoMap', {
    center: center,
    zoom: 4,
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
      balloonContentBody: '<strong>' + photo_list[index]['surface'] + ', ' + photo_list[index]['porch'] + '</strong><br/><img src="' + photo_list[index]['image'] +'" style="width:150px"/>',
      clusterCaption: '<span>' + photo_list[index]['surface'] + ', ' + photo_list[index]['porch'] + '</span>'
    };
  },
    getPointOptions = function () {
    return {
      preset: 'islands#violetIcon'
    };
  },
  //points = photo_points,
  geoObjects = [];
  for(var i = 0, len = photo_list.length; i < len; i++) {
    geoObjects[i] = new ymaps.Placemark([photo_list[i]['coord_y'], photo_list[i]['coord_x']], getPointData(i), getPointOptions());
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