import React from "react";
import "./App.css";
import SearchPage from "./pages/searchPage";
// import {Routes, Route} from 'react-router'
import { BrowserRouter, Routes, Route } from "react-router-dom";
import PopularTours from "./pages/popularTours";
import PersonalPage from "./pages/personalPage";
import TourPage from "./pages/TourPage";
import { useState } from "react";
import { AuthProvider, useAuth } from "./hooks/useAuth";
import { HeroUIProvider } from "@heroui/react";
import Login from "./pages/loginPage";
import Developing from "./pages/developingpage";
import Registration from "./pages/registrationpage";
import RecomendationPage from "./pages/recomendationPage";
import MainPage from "./pages/mainPage";
import FavoriteToursPage from "./pages/favoritetourspage";

function App() {
  useAuth();
  const [listTours, setListTour] = useState([]);

  return (
    <>
      <HeroUIProvider>
      <AuthProvider>
        <BrowserRouter>
            <Routes>
              <Route
                path="/tours"
                element={
                  <SearchPage listTours={listTours} setListTour={setListTour} />
                }
              />
              <Route
                path="/tours"
                element={
                  <RecomendationPage
                    listTours={listTours}
                    setListTour={setListTour}
                  />
                }
              />

              <Route path="/" element={<MainPage/>}/>
              <Route path="/listTours" element={<RecomendationPage />} />
              <Route path="/favoriteTours/1" element={<FavoriteToursPage />} />
              <Route path="/popularTours" element={<PopularTours />} />
              <Route path="/user/:user_id" element={<PersonalPage />} />
              <Route path="/tour/:tour_id" element={<TourPage />} />
              <Route path="/auth-in" element={<Login />} />
              <Route path="/registration" element={<Registration />} />
              <Route path="/return-password" element={<Developing />} />
            </Routes>
        </BrowserRouter>
        </AuthProvider>
      </HeroUIProvider>
    </>
  );
}

export default App;
