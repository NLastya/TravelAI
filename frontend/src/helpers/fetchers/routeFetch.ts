
const fetchTourRoute = (LagLatPoints, ...details) => {
    let data = {};
    fetch(`https://graphhopper.com/api/1/route?key=`).then(res => {
        if(!res.ok){
            throw new Error('Ошибка при соединении')
        }
        return res;
    }).then(res => res.json())
    .then(ans => {
        data = ans;
    })
    .catch(err => {
        console.log(err);
    })
    return data;
}

'https://graphhopper.com/api/1/route?key=YOUR_API_KEY_HERE' \
  -H 'Content-Type: application/json' \
  -d '{
    "profile": "bike",
    "points": [
      [
        11.539421,
        48.118477
      ],
      [
        11.559023,
        48.12228
      ]
    ],
    "point_hints": [
      "Lindenschmitstraße",
      "Thalkirchener Str."
    ],
    "snap_preventions": [
      "motorway",
      "ferry",
      "tunnel"
    ],
    "details": [
      "road_class",
      "surface"
    ]
  }'