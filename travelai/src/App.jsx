import React from 'react'
import './App.css'
import SearchPage from './pages/searchPage'
// import {Routes, Route} from 'react-router'
import { BrowserRouter, Routes, Route } from "react-router-dom";
import PopularTours from './pages/popularTours'
import PersonalPage from './pages/personalPage'

function App() {
  return (
    <>
    <BrowserRouter>
      <Routes>
        <Route path='/tours' element={<SearchPage/>}/>
        <Route path='/popularTiurs' element={<PopularTours/>}/>
        <Route path='/user/:user_id' element={<PersonalPage/>}/>
      </Routes>
    </BrowserRouter>
    </>

    
  )
}

export default App
