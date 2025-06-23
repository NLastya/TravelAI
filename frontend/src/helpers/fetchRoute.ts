// export async function fetchRoute(
//     startCoordinates,
//     endCoordinates,
//     type,
//   ) {
//     let truck;
//     if (type === 'truck') {
//       // set truck with trailer by default
//       truck = {
//         weight: 40,
//         maxWeight: 40,
//         axleWeight: 10,
//         payload: 20,
//         height: 4,
//         width: 2.5,
//         length: 16,
//         ecoClass: 4,
//         hasTrailer: true
//       };
//     }
//     console.log('yes');
//     // Request a route from the Router API with the specified parameters.
//     const routes = await ymaps3.route({
//       points: [startCoordinates, endCoordinates], // Start and end points of the route LngLat[]
//       type, // Type of the route
//       bounds: true, // Flag indicating whether to include route boundaries in the response
//       truck
//     });

//     console.log('route', routes);    // Check if a route was found
//     if (!routes[0]) return;

//     // Convert the received route to a RouteFeature object.
//     const route = routes[0].toRoute();

//     // Check if a route has coordinates
//     if (route.geometry.coordinates.length == 0) return;

//     console.log('route:', route)
//     return route;
//   }

import { HOST_URL } from "../../src/config.jsx";

export const getGenerateTours = (
  fetchData = {},
  storeSaveFunc = (data) => {}
) => {
  fetch(`${HOST_URL}/generate_tour`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      // "ngrok-skip-browser-warning": true,
    },
    body:
      JSON.stringify(fetchData) ??
      JSON.stringify({
        user_id: 1,
        data_start: "26.01.25",
        data_end: "30.01.25",
        location: "Москва",
        hobby: ["музеи искусства", "спортзал"],
      }),
  })
    .then((res) => {
      if (!res.ok) {
        throw new Error(`HTTP error! Status: ${res.status}`);
      }
      return res.json();
    })
    .then((data) => storeSaveFunc(data))
    .catch((e) => {
      console.log(e);
      // api.error({
      //   message: `Код ошибки: ${e.code || "unknown"}`,
      //   description: e.message,
      //   placement: "bottomRight",
      // });
    });
};
