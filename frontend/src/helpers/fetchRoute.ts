export async function fetchRoute(
    startCoordinates,
    endCoordinates,
    type,
  ) {
    let truck;
    if (type === 'truck') {
      // set truck with trailer by default
      truck = {
        weight: 40,
        maxWeight: 40,
        axleWeight: 10,
        payload: 20,
        height: 4,
        width: 2.5,
        length: 16,
        ecoClass: 4,
        hasTrailer: true
      };
    }
    console.log('yes');
    // Request a route from the Router API with the specified parameters.
    const routes = await ymaps3.route({
      points: [startCoordinates, endCoordinates], // Start and end points of the route LngLat[]
      type, // Type of the route
      bounds: true, // Flag indicating whether to include route boundaries in the response
      truck
    });
  
    console.log('route', routes);    // Check if a route was found
    if (!routes[0]) return;
  
    // Convert the received route to a RouteFeature object.
    const route = routes[0].toRoute();
  
    // Check if a route has coordinates
    if (route.geometry.coordinates.length == 0) return;
  
    console.log('route:', route)
    return route;
  }