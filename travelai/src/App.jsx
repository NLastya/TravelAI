
import React, { useState } from 'react';
import './App.css';
import SearchPage from './pages/searchPage';
import PopularTours from './pages/popularTours';
import PersonalPage from './pages/personalPage';
import TourPage from './pages/TourPage';
import { HashRouter as Router, Routes, Route } from "react-router-dom";
import { AuthProvider, useAuth } from './hooks/useAuth';

function App() {
  const { isLogged, login, logout } = useAuth();
  const [listTours, setListTour] = useState([]);

  return (
    <Router>
      <AuthProvider>
        <Routes>
          <Route path='/tours' element={<SearchPage listTours={listTours} setListTour={setListTour} />} />
          <Route path='/popularTours' element={<PopularTours />} />
          <Route path='/user/:user_id' element={<PersonalPage />} />
          <Route path='/tour/:tour_id' element={<TourPage />} />
        </Routes>
      </AuthProvider>
    </Router>
  );
}

export default App;
