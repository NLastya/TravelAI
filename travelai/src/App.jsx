
import React, { useState } from 'react';
import './App.css';
import SearchPage from './pages/searchPage';
import PopularTours from './pages/popularTours';
import PersonalPage from './pages/personalPage';
import TourPage from './pages/TourPage';
import { HashRouter as Router, Routes, Route } from 'react-router-dom';
import { AuthProvider, useAuth } from './hooks/useAuth';

function App() {
  const { isLogged, login, logout } = useAuth();
  const [form, setForm] = useState({location: '', data_start: '2024-11-12', data_end: '2024-11-31', hobies: []});
  const [popularTourForm, setPopularTourForm] = useState({location: '', data_start: '2024-11-12', data_end: '2024-11-31'});
  const [listTours, setListTour] = useState({data: '04.01.25'});


  return(
      <AuthProvider>
        <Router>
          <Routes>
            <Route path='/tours' element={<SearchPage listTours={listTours} setListTour={setListTour} form={form} setForm={setForm}/>} />
            <Route path='/popularTours' element={<PopularTours popularTourForm={popularTourForm} setPopularTourForm={setPopularTourForm}/>} />
            <Route path='/user/:user_id' element={<PersonalPage setForm={setForm} form={form}/>} />
            <Route path='/tour/:tour_id' element={<TourPage setForm={setForm}/>} />
          </Routes>
        </Router>
      </AuthProvider>
      )
}

export default App;
