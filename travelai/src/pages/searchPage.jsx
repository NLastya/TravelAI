/* eslint-disable react/prop-types */
import React, {useEffect, useState} from 'react'
import Header from '../components/Header';
import style from './searchpage.module.css';
import Filters from '../components/Filters/Filters'
import VerticalCard from '../components/VerticalCard/VerticalCard';
import { notification } from 'antd';
import Footer from '../components/Footer/Footer'
import { HOST_URL } from '../config';
import dayjs from "dayjs";

const SearchPage = (props) => {
  // props.form, props.setForm

    const [isLoading, setIsLoading] = useState(false);
    const [listTours, setListTour] = useState([{data: '04.01.25'}]);
    const [form, setForm] = useState({location: '', data_start: '2024-12-', data_end: '2024-12-30', user_id: 1})

    const [api, contextHolder] = notification.useNotification();

    const listToursMap = (props?.listTours).map(item => (<VerticalCard key={item.key} {...item}/>) )

    const handleSubmit = () => {
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


    // useEffect(() => {
    //     setIsLoading(true);
        // fetch(`${HOST_URL}/generate_tour`, {
        //     method: 'POST', // Указываем метод запроса
        //     headers: {
        //       'Content-Type': 'application/json', // Устанавливаем тип контента
        //       'ngrok-skip-browser-warning': true,
        //     },
        //     body: JSON.stringify({ // Преобразуем тело запроса в JSON-строку
        //       user_id: 1,
        //       data_start: '26.01.25',
        //       data_end: '30.01.25',
        //       location: 'Москва',
        //       hobby: ['музеи искусства', 'спортзал'],
        //     }),
        //   })
        //   .then(res => {
        //     if (!res.ok) {
        //       throw new Error(`HTTP error! Status: ${res.status}`);
        //     }
        //     return res.json();
        //   })
        //   .then(data => setListTour(data))
        //   .catch(e => {
        //     console.log(e);
        //     api.error({
        //       message: `Код ошибки: ${e.code || 'unknown'}`, // Используем шаблонные строки
        //       description: e.message,
        //       placement: 'bottomRight',
        //     });
        //   });
    //     setIsLoading(false);

    // }, [])

    if(!props?.listTours)
        return null;


    return(
    <>
    <div className={style.main}>
        <Header user={props?.user ? props.user : {}}/>
        <Filters form={form} setForm={setForm}/>
        {!isLoading && listToursMap
        }
        
    </div>
    <Footer/>
    </>
    )


}

export default SearchPage;