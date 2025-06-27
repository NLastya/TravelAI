export const getGenerateTours = (
  fetchData = {},
  storeSaveFunc = (data) => {}
) => {
  fetch('/generate_tour', {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
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
    });
};

export const getTourById = (
  tour_id,
  fetchData = {},
  storeSaveFunc = (data) => {}
) => {
  fetch(`/tour/${tour_id}`)
    .then((res) => res.json())
    .then((data) => storeSaveFunc(data))
    .catch((e) => {
      console.log(e);
    });
};

export const postUserInterests = (user_id, fetchData={}, storeSaveFunc, setIsSuccessfull) => {
  fetch('/user_survey/', {
    method: 'POST',
    body: JSON.stringify(fetchData),
    headers: {
      "Content-Type": "application/json",
    },
  })
  .then((res) => res.json())
  .then((data) => {
    setIsSuccessfull(true)
    storeSaveFunc(data)
  })
  .catch((e) => {
    setIsSuccessfull(true)
    console.log(e);
  });
}

export const getUserSurvey = async (userId, saveDataState, isError) => {
  try {
    const response = await fetch(`/user_survey/${userId}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
    
    const data = await response.json();
    saveDataState(data);
  } catch (error) {
    isError(error.message);
    console.error('Error in getUserSurvey:', error);
  }
};

export const startCityView = async (userId, cityName, timestamp, saveDataState, isError) => {
  try {
    const response = await fetch('/analytics/city-view/start', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        user_id: userId,
        city_name: cityName,
        timestamp,
        action: 'start'
      }),
    });

    if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
    
    const data = await response.json();
    saveDataState(data);
  } catch (error) {
    isError(error.message);
    console.error('Error in startCityView:', error);
  }
};

export const endCityView = async (userId, cityName, timestamp, saveDataState, isError) => {
  try {
    const response = await fetch('/analytics/city-view/end', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        user_id: userId,
        city_name: cityName,
        timestamp,
        action: 'end'
      }),
    });

    if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
    
    const data = await response.json();
    saveDataState(data);
  } catch (error) {
    isError(error.message);
    console.error('Error in endCityView:', error);
  }
};

export const getCityViewsAnalytics = async (userId, saveDataState, isError) => {
  try {
    const response = await fetch(`/analytics/city-view/${userId}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
    
    const data = await response.json();
    saveDataState(data);
  } catch (error) {
    isError(error.message);
    console.error('Error in getCityViewsAnalytics:', error);
  }
};

export const getActiveCityViews = async (userId, saveDataState, isError) => {
  try {
    const response = await fetch(`/analytics/city-view/${userId}/active`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
    
    const data = await response.json();
    saveDataState(data);
  } catch (error) {
    isError(error.message);
    console.error('Error in getActiveCityViews:', error);
  }
};

export const addFavorite = async (userId, tourId, saveDataState, isError) => {
  try {
    const response = await fetch('/favorites', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        user_id: userId,
        tour_id: tourId
      }),
    });

    if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
    
    const data = await response.json();
    saveDataState(data);
  } catch (error) {
    isError(error.message);
    console.error('Error in addFavorite:', error);
  }
};

export const removeFavorite = async (userId, tourId, saveDataState, isError) => {
  try {
    const response = await fetch('/favorites', {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        user_id: userId,
        tour_id: tourId
      }),
    });

    if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
    
    const data = await response.json();
    saveDataState(data);
  } catch (error) {
    isError(error.message);
    console.error('Error in removeFavorite:', error);
  }
};

export const getUserFavorites = async (userId, saveDataState, isError) => {
  try {
    const response = await fetch(`/users/${userId}/favorites`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
    
    const data = await response.json();
    saveDataState(data);
  } catch (error) {
    isError(error.message);
    console.error('Error in getUserFavorites:', error);
  }
};

// Функция для построения маршрута (оставлена без изменений)
export async function fetchRoute(
  startCoordinates,
  endCoordinates,
  type,
) {
  let truck;
  if (type === 'truck') {
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
  
  const routes = await ymaps3.route({
    points: [startCoordinates, endCoordinates],
    type,
    bounds: true,
    truck
  });

  if (!routes[0]) return;
  const route = routes[0].toRoute();
  if (route.geometry.coordinates.length == 0) return;
  return route;
}