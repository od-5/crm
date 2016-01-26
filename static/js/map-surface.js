//ymaps.ready(init);
//var myMap;
//
//function init(){
//    city = $('.js-map').data('city');
//    var coord = '';
//    var myGeocoder = ymaps.geocode(city);
//    myGeocoder.then(
//        function (res) {
//            coord = res.geoObjects.get(0).geometry.getCoordinates();
//            myMap = new ymaps.Map("surfaceMap", {
//                center: coord,
//                zoom: 10
//            });
//            $.get("/surface-map/",
//                function(e) {
//                    //var data = JSON.parse(e); // получаем данные от сервера
//                    //console.log(e);
//                    function outputItem(item, i, e) {
//                        myMap.geoObjects.add(
//                            new ymaps.Placemark([item['coord_y'], item['coord_x']], {
//                            balloonContent: item['name'],
//                            hintContent: item['name']
//                            })
//                        );
//                    }
//                    e.forEach(outputItem);
//                }
//            );
//        }
//    );
//}

ymaps.ready(function () {
  var map_block = $('.js-map');
  var coord_x = map_block.data('coord-x');
  var coord_y = map_block.data('coord-y');
  var surface_list = '';
  var city_count = map_block.data('city-count');
  if (city_count == 1){
    var map_zoom = 9;
  } else {
    var map_zoom = 3;
  }
  $.ajax({
    type: "GET",
    async: false,
    url: "/surface-map/",
    success: function (data) {
      surface_list = data;
    }
  });
  console.log(surface_list);
  var new_points = [];
  var new_baloon = [];
  for (var i = 0; i<surface_list.length; i++) {
    new_points.push([surface_list[i]['coord_y'], surface_list[i]['coord_x']]);
    new_baloon.push([surface_list[i]['name'], surface_list[i]['porch']]);

  }

  console.log(new_points);
  console.log(new_baloon);
  var myMap = new ymaps.Map('surfaceMap', {
        center: [coord_y.replace(',','.'), coord_x.replace(',','.')],
        //center: [55.751574, 37.573856],
        zoom: map_zoom,
        behaviors: ['default', 'scrollZoom']
    }, {
        searchControlProvider: 'yandex#search'
    }),
    /**
     * Создадим кластеризатор, вызвав функцию-конструктор.
     * Список всех опций доступен в документации.
     * @see https://api.yandex.ru/maps/doc/jsapi/2.1/ref/reference/Clusterer.xml#constructor-summary
     */
    clusterer = new ymaps.Clusterer({
        /**
         * Через кластеризатор можно указать только стили кластеров,
         * стили для меток нужно назначать каждой метке отдельно.
         * @see https://api.yandex.ru/maps/doc/jsapi/2.1/ref/reference/option.presetStorage.xml
         */
      preset: 'islands#invertedVioletClusterIcons',
      /**
       * Ставим true, если хотим кластеризовать только точки с одинаковыми координатами.
       */
      groupByCoordinates: false,
      /**
       * Опции кластеров указываем в кластеризаторе с префиксом "cluster".
       * @see https://api.yandex.ru/maps/doc/jsapi/2.1/ref/reference/ClusterPlacemark.xml
       */
      clusterDisableClickZoom: true,
      clusterHideIconOnBalloonOpen: false,
      geoObjectHideIconOnBalloonOpen: false
    }),
    /**
     * Функция возвращает объект, содержащий данные метки.
     * Поле данных clusterCaption будет отображено в списке геообъектов в балуне кластера.
     * Поле balloonContentBody - источник данных для контента балуна.
     * Оба поля поддерживают HTML-разметку.
     * Список полей данных, которые используют стандартные макеты содержимого иконки метки
     * и балуна геообъектов, можно посмотреть в документации.
     * @see https://api.yandex.ru/maps/doc/jsapi/2.1/ref/reference/GeoObject.xml
     */
      getPointData = function (index) {
      return {
          balloonContentBody: 'Адрес: <strong>' + new_baloon[index][0] + '</strong><br/>Количество стендов: <strong>' + new_baloon[index][1] + '</strong>',
          clusterCaption: '<strong>' + new_baloon[index][0] + '</strong>'
      };
    },
    /**
     * Функция возвращает объект, содержащий опции метки.
     * Все опции, которые поддерживают геообъекты, можно посмотреть в документации.
     * @see https://api.yandex.ru/maps/doc/jsapi/2.1/ref/reference/GeoObject.xml
     */
      getPointOptions = function () {
      return {
          preset: 'islands#violetIcon'
      };
    },
    points = new_points;
    //points = [
    //  [55.831903,37.411961], [55.763338,37.565466], [55.763338,37.565466], [55.744522,37.616378], [55.780898,37.642889], [55.793559,37.435983], [55.800584,37.675638], [55.716733,37.589988], [55.775724,37.560840], [55.822144,37.433781], [55.874170,37.669838], [55.716770,37.482338], [55.780850,37.750210], [55.810906,37.654142], [55.865386,37.713329], [55.847121,37.525797], [55.778655,37.710743], [55.623415,37.717934], [55.863193,37.737000], [55.866770,37.760113], [55.698261,37.730838], [55.633800,37.564769], [55.639996,37.539400], [55.690230,37.405853], [55.775970,37.512900], [55.775777,37.442180], [55.811814,37.440448], [55.751841,37.404853], [55.627303,37.728976], [55.816515,37.597163], [55.664352,37.689397], [55.679195,37.600961], [55.673873,37.658425], [55.681006,37.605126], [55.876327,37.431744], [55.843363,37.778445], [55.875445,37.549348], [55.662903,37.702087], [55.746099,37.434113], [55.838660,37.712326], [55.774838,37.415725], [55.871539,37.630223], [55.657037,37.571271], [55.691046,37.711026], [55.803972,37.659610], [55.616448,37.452759], [55.781329,37.442781], [55.844708,37.748870], [55.723123,37.406067], [55.858585,37.484980]
    //],
    geoObjects = [];

  /**
   * Данные передаются вторым параметром в конструктор метки, опции - третьим.
   * @see https://api.yandex.ru/maps/doc/jsapi/2.1/ref/reference/Placemark.xml#constructor-summary
   */
  for(var i = 0, len = points.length; i < len; i++) {
      geoObjects[i] = new ymaps.Placemark(points[i], getPointData(i), getPointOptions());
  }

  /**
   * Можно менять опции кластеризатора после создания.
   */
  clusterer.options.set({
    gridSize: 80,
    clusterDisableClickZoom: true
  });

  /**
   * В кластеризатор можно добавить javascript-массив меток (не геоколлекцию) или одну метку.
   * @see https://api.yandex.ru/maps/doc/jsapi/2.1/ref/reference/Clusterer.xml#add
   */
  clusterer.add(geoObjects);
  myMap.geoObjects.add(clusterer);

  /**
   * Спозиционируем карту так, чтобы на ней были видны все объекты.
   */

  //myMap.setBounds(clusterer.getBounds(), {
  //    checkZoomRange: true
  //});
});