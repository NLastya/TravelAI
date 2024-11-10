import React from 'react'
import Header from './Header'
import Moscow from './Moscow'
import Piter from './Piter'
import Kalik from './Kalik'
import "./App.css"

function App() {

  return (
    <main>
      <Header />
      <div className='Cards'>
        <Moscow />
        <Piter />
        <Kalik />
      </div>

    </main>
  )
}

export default App
