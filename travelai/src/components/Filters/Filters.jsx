/* eslint-disable react/prop-types */
import React, {useState} from 'react';
import style from './filters.module.css';
import { DatePicker } from 'antd';
import dayjs from "dayjs";
import { HOST_URL } from '../../config';
const { RangePicker } = DatePicker;

const Filters = ({form, setForm}) => {
    const [error, setError] = useState(false);

    const handleClick = () => {
        if(!(form.location && form.data_start && form.data_end)) {
            setError(true);
        }

        else {
            setError(false);
        fetch(`${HOST_URL}/generate_tour`, {
                    method: 'POST', // Указываем метод запроса
                    headers: {
                      'Content-Type': 'application/json', // Устанавливаем тип контента
                      'ngrok-skip-browser-warning': true,
                    },
                    body: JSON.stringify({ // Преобразуем тело запроса в JSON-строку
                      user_id: 1,
                      data_start: '26.01.25',
                      data_end: '30.01.25',
                      location: 'Москва',
                      hobby: ['музеи искусства', 'спортзал'],
                    }),
                  })
                  .then(res => {
                    if (!res.ok) {
                      throw new Error(`HTTP error! Status: ${res.status}`);
                    }
                    return res.json();
                  })
                  .then(data => setListTour(data))
                  .catch(e => {
                    console.log(e);
                    api.error({
                      message: `Код ошибки: ${e.code || 'unknown'}`, // Используем шаблонные строки
                      description: e.message,
                      placement: 'bottomRight',
                    });
                  });
        }
    }

    return(
    <div className={style.filters}>
        <div>
            <label className={style.inputLabel}> Место
                <input className={style.inputText} value={form?.location}
                onChange={(e) => setForm(prev => ({...prev, location: e.target.value}))}
                />
            </label>

            <label className={style.inputLabel}> Даты маршрута
                {/* <input className={style.inputText} value={form?.date}
                onChange={(e) => setForm(prev => ({...prev, data_start: e.target.value}))}
                /> */}
                 <RangePicker 
                                value={[dayjs(form?.data_start) ?? dayjs('26.12.2024'), dayjs(form?.data_end) ?? dayjs('31.12.2024')]}
                                format="YYYY-MM-DD"
                                allowClear={false}
                                 onChange={(value) => {
                                    setForm(prev => ({...prev, data_start: (value[0]).format('YYYY-MM-DD'), data_end: (value[1]).format('YYYY-MM-DD') }))
                                    console.log((value[0]).format('DD-MM-YYYY'))
                                 }
                                }
                                />
            </label>
        </div>

        <div>
            <div>
                {error && <span style={{color: 'red', fontSize: '12px'}}>Заполните все поля</span>}
            <button className='mint-btn' onClick={handleClick}>
                <img src='/icons/plane.svg' alt='plane'/>
                Найти туры
            </button>
            </div>
        </div>

    </div>
    )


}

export default Filters;