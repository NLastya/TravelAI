/* eslint-disable react/prop-types */
import React, {useEffect, useState} from 'react'
import Header from '../components/Header';
import style from './searchpage.module.css';
import Filters from '../components/Filters/Filters'
import VerticalCard from '../components/VerticalCard/VerticalCard';
import { notification } from 'antd';
import Footer from '../components/Footer/Footer'
import { HOST_URL } from '../config';

const PopularTours = (props) => {
    const [isLoading, setIsLoading] = useState(false);
    const [listTours, setListTour] = useState([{date: '04.01.25'}]);
    const [form, setForm] = useState({location: '', date: ''})

    const [api, contextHolder] = notification.useNotification();

    const listToursMap = listTours.map(item => (<VerticalCard key={item.key} {...item}/>) )


    useEffect(() => {
        setIsLoading(true);
        fetch(`${HOST_URL}/list_popular`, {
            method: 'GET', 
            headers: {
               'ngrok-skip-browser-warning': true,
                mode: 'no-cors',
            }
            // headers: {
            //   'Content-Type': 'application/json', // Устанавливаем тип контента
            //   'ngrok-skip-browser-warning': true,
            // },
            // body: JSON.stringify({ // Преобразуем тело запроса в JSON-строку
            //   user_id: 1,
            //   data_start: '26.01.25',
            //   data_end: '30.01.25',
            //   location: 'Москва',
            //   hobby: ['музеи искусства', 'спортзал'],
            // }),
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
              message: `Код ошибки: ${e.code || 'unknown'}`, 
              description: e.message,
              placement: 'bottomRight',
            });
          });
        setIsLoading(false);

    }, [])

    // if(isLoading)
    //     return null;


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

export default PopularTours;