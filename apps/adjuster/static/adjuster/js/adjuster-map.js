ymaps.ready(function () {
  var adjuster_list = '';
  var map_block = $('#YMapsID');
  var url = map_block.data('url');
  var city = $('#id_city').val();
  var email = $('#id_email').val();
  var last_name = $('#id_last_name').val();
  $.ajax({
    type: "POST",
    async: false,
    url: url,
    data: {
      city: city,
      email: email,
      last_name: last_name
    }
  }).done(function (data) {
    if (data.adjuster_list.length){
      adjuster_list = data.adjuster_list;
    }
  });
  if (adjuster_list.length){
    center = [adjuster_list[0]['coord_y'], adjuster_list[0]['coord_x']];
  } else {
    center = [48.713339, 44.497116]
  }
  console.log(center)
  var myMap = new ymaps.Map('YMapsID', {
    center: center,
    zoom: 4,
    behaviors: ['default', 'scrollZoom']
  }, {
    searchControlProvider: 'yandex#search'
  }),
    getPointData = function (index) {
    return {
      balloonContent: adjuster_list[index]['name'],
      hintContent: adjuster_list[index]['name']
    };
  },
    getPointOptions = function () {
    return {
      preset: 'islands#violetIcon'
    };
  },
  geoObjects = [];
  for(var i = 0, len = adjuster_list.length; i < len; i++) {
    geoObjects[i] = new ymaps.Placemark([adjuster_list[i]['coord_y'], adjuster_list[i]['coord_x']], getPointData(i), getPointOptions());
  }
  myMap.geoObjects.add(geoObjects);


  //myMap.setBounds(clusterer.getBounds(), {
  //    checkZoomRange: true
  //});
});