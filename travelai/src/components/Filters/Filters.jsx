/* eslint-disable react/prop-types */
import React from 'react';
import style from './filters.module.css';

const Filters = ({form, setForm}) => {

    return(
    <div className={style.filters}>
        <div>
            <label className={style.inputLabel}> Место
                <input className={style.inputText} value={form?.location}
                onChange={(e) => setForm(prev => ({...prev, location: e.target.value}))}
                />
            </label>

            <label className={style.inputLabel}> Даты маршрута
                <input className={style.inputText} value={form?.date}
                onChange={(e) => setForm(prev => ({...prev, date: e.target.value}))}
                />
            </label>
        </div>

        <div>
            <button className='mint-btn'>
                <img src='/icons/plane.svg' alt='plane'/>
                Найти туры
            </button>
        </div>

    </div>
    )


}

export default Filters;