ymaps.ready(init);
var myMap;

function init(){
    city = 'Волгоград';
    var coord = '';
    var myGeocoder = ymaps.geocode(city);
        myGeocoder.then(
            function (res) {
                coord = res.geoObjects.get(0).geometry.getCoordinates();
                myMap = new ymaps.Map("surfaceMap", {
                    center: coord,
                    zoom: 3
                });
                $.get("/surface-map/",
                    function(e) {
                        //var data = JSON.parse(e); // получаем данные от сервера
                        //console.log(e);
                        function outputItem(item, i, e) {
                            myMap.geoObjects.add(
                                new ymaps.Placemark([item['coord_y'], item['coord_x']], {
                                balloonContent: item['name'],
                                hintContent: item['name']
                                })
                            );
                        }
                        e.forEach(outputItem);
                    }
                );


            }
        );

}