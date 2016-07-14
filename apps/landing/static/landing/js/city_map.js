ymaps.ready(function () {
  var myMap;
  var url = $('#YMapsID').data('url');
  city = 'Екатеринбург';
  var coord = '';
  var myGeocoder = ymaps.geocode(city);
  myGeocoder.then(
    function (res) {
      coord = res.geoObjects.get(0).geometry.getCoordinates();
      myMap = new ymaps.Map("YMapsID", {
        center: coord,
        zoom: 3
      });
      $.ajax({
        url: url
      }).done(function (data) {
        if (data.city_list.length) {
          var city_list = data.city_list;
          for(var i = 0, len = city_list.length; i < len; i++) {
            myMap.geoObjects.add(
              new ymaps.Placemark([city_list[i]['coord_y'], city_list[i]['coord_x']], {
              balloonContent: city_list[i]['name'] + ' Количество поверхностей: ' + city_list[i]['surface_count'],
              hintContent: city_list[i]['name'] + ' Количество поверхностей: ' + city_list[i]['surface_count']
              })
            );
          }
        }
      });
    }
  );
});