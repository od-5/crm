// 
// $(function(){
ymaps.ready(init);
var myMap;
var w = screen.width,
    h = screen.height;
console.log(w);
console.log(h);
//$('#map-wrapper').height(h);
//$('#map-wrapper').height(h);
function init(){
    city = $('main.container').data('city');
    var coord = '';
    var myGeocoder = ymaps.geocode(city);
        myGeocoder.then(
            function (res) {
                coord = res.geoObjects.get(0).geometry.getCoordinates();
                myMap = new ymaps.Map("map", {
                    center: coord,
                    zoom: 15
                });
                console.log(res.geoObjects.get(0).geometry.getCoordinates());
                //$.get("/map/",
                //    function(e) {
                //        //var data = JSON.parse(e); // получаем данные от сервера
                //        //console.log(e);
                //        function outputItem(item, i, e) {
                //            myMap.geoObjects.add(
                //                new ymaps.Placemark([item['coord_y'], item['coord_x']], {
                //                balloonContent: item['address'],
                //                hintContent: item['name']
                //                })
                //            );
                //        }
                //        e.forEach(outputItem);
                //    }
                //);


            }
            //function (err) {
            //    coord = [48.707103, 44.516939];
            //    myMap = new ymaps.Map("YMapsID", {
            //        center: coord,
            //        zoom: 11
            //    });
            //    $.get("/map/",
            //        function(e) {
            //            //var data = JSON.parse(e); // получаем данные от сервера
            //            //console.log(e);
            //            function outputItem(item, i, e) {
            //                myMap.geoObjects.add(
            //                    new ymaps.Placemark([item['coord_y'], item['coord_x']], {
            //                    balloonContent: item['address'],
            //                    hintContent: item['name']
            //                    })
            //                );
            //            }
            //            e.forEach(outputItem);
            //        }
            //    );
            //}
        );
    $('.js-map-show-btn').click(function(){
        //var coord_x = $(this).data('coord-x');
        //var coord_y = $(this).data('coord-y');
      myMap.geoObjects.removeAll();
        var point_coord = [parseFloat($(this).data('coord-y')), parseFloat($(this).data('coord-x'))];
        ymaps.geocode(city, { results: 1 })
        .then(function (res) {
          myMap.panTo(point_coord,
            {
                flying: true
            }
          );
          console.log('['+coord_x+', '+coord_y+']');
        });
      myMap.geoObjects.add(
        new ymaps.Placemark(point_coord)
      );
      $('#map-wrapper').removeClass('hide');
      $('#map-wrapper').height(h);
    });

    $('.js-map-hide-btn').click(function(){
      $('#map-wrapper').addClass('hide');
    });
}