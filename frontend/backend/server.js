"use strict";

const express = require("express");
const app = express();

// Позволяем читать JSON из тела запроса
app.use(express.json());

/*
  POST /generate_tour
  Ожидаемый входной формат:
  {
    user_id: int,
    data_start: str,
    data_end: str,
    location: str,
    hobby: list
  }
  Ответ – список туров:
  [
    {
      tour_id: int,
      title: string,
      photos?: [objectPhoto|string_url, ...],
      date: [start:string, end:string], // формат 'dd:mm:yyyy'
      location: string,
      rating: float|string,
      relevance: float // процент совпадения с интересами пользователя
    },
    ...
  ]
*/
app.post("/generate_tour", (req, res) => {
  // Можно обработать входные данные, например, user_id, data_start и т.д.
  // Здесь мы просто возвращаем замоканный список туров.

  const mockedTours = [
    {
      tour_id: 1,
      title: "Amazing Adventure",
      photos: ["https://example.com/photo1.jpg"],
      date: ["01:01:2024", "05:01:2024"],
      location: req.body.location || "Unknown",
      rating: 4.8,
      relevance: 85.5,
    },
    {
      tour_id: 2,
      title: "Cultural Experience",
      photos: [{ objectPhoto: "PhotoObject1" }],
      date: ["02:01:2024", "06:01:2024"],
      location: req.body.location || "Unknown",
      rating: "4.5",
      relevance: 90.0,
    },
  ];

  res.json(mockedTours);
});

/*
  GET /tour/:id_tour
  Ответ – детальная информация о туре:
  {
    tour_id: number,
    title: string,
    date: [start:string, end:string],  // формат 'dd:mm:yyyy'
    location: string,
    rating: float|string,
    places: [
      {
        id_place: int,
        name: string,
        location: string,
        rating: float|string,
        date: [start:string, end:string], // формат 'dd:mm:yyyy'
        description?: string,
        photo?: objectPhoto|string,
        mapgeo: [xcoord, y_coord]
      },
      ...
    ],
    features: object,   // дополнительные характеристики тура
    reviews: [          // отзывы пользователей
      {
        user: string,
        rating: number,
        comment: string
      },
      ...
    ]
  }
*/
app.get("/tour/:id_tour", (req, res) => {
  const idTour = parseInt(req.params.id_tour, 10);

  // Замоканные данные для детальной информации о туре
  const mockedTourDetail = {
    tour_id: idTour,
    title: "Detailed Tour Title",
    date: ["03:01:2024", "07:01:2024"],
    location: "City of Wonders",
    rating: 4.7,
    places: [
      {
        id_place: 101,
        name: "Museum of History",
        location: "Downtown",
        rating: 4.6,
        date: ["03:01:2024", "03:01:2024"],
        description: "A historic museum featuring ancient artefacts",
        photo: "https://example.com/place_photo.jpg",
        mapgeo: [40.7128, -74.0060],
      },
      {
        id_place: 102,
        name: "Art Gallery",
        location: "City Center",
        rating: "4.5",
        date: ["04:01:2024", "04:01:2024"],
        mapgeo: [40.7138, -74.0070],
      },
    ],
    features: {
      includesMeals: true,
      guidedTours: true,
    },
    reviews: [
      {
        user: "Alice",
        rating: 5,
        comment: "Amazing experience!",
      },
      {
        user: "Bob",
        rating: 4,
        comment: "Very enjoyable, but could be better organized.",
      },
    ],
  };

  res.json(mockedTourDetail);
});

/*
  GET /list_popular
  Возвращает список популярных туров
  (аналогично /generate_tour, но без входных параметров)
*/
app.get("/list_popular", (req, res) => {
  const popularTours = [
    {
      tour_id: 3,
      title: "Popular Tour 1",
      photos: ["https://example.com/popular1.jpg"],
      date: ["05:01:2024", "10:01:2024"],
      location: "Popular City",
      rating: 4.9,
      relevance: 95.0,
    },
    {
      tour_id: 4,
      title: "Popular Tour 2",
      photos: [{ objectPhoto: "PopularPhotoObj" }],
      date: ["06:01:2024", "11:01:2024"],
      location: "Popular City 2",
      rating: "4.8",
      relevance: 92.0,
    },
  ];

  res.json(popularTours);
});

// Запуск сервера
const PORT = 3000;
app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});