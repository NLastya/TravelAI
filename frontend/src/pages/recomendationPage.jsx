/* eslint-disable react/prop-types */
import React, { useEffect, useState } from "react";
import Header from "../components/Header";
import style from "./recomendationpage.module.css";
import Filters from "../components/Filters/Filters";
import VerticalCard from "../components/VerticalCard/VerticalCard";
import { notification } from "antd";
import Footer from "../components/Footer/Footer";
import PaginationCustom from "../components/pagination/pagination";
import Loader from '../components/Loader/loader';
import {getGenerateTours} from '../helpers/fetchRoute';

const RecomendationPage = (props) => {
  const [isLoading, setIsLoading] = useState(false);
  const [listTours, setListTour] = useState([
    {
      date: "04.01.25",
      name: "Тур в Сибирь",
      image: "/mock/pic1.jpg",
      location: "Сибирь",
    },
    {
      date: "04.01.25",
      name: "Тур в Сибирь",
      image: "/mock/pic1.jpg",
      location: "Сибирь",
    },
    {
      date: "04.01.25",
      name: "Тур в Сибирь",
      image: "/mock/pic1.jpg",
      location: "Сибирь",
    },
    {
      date: "04.01.25",
      name: "Тур в Сибирь",
      image: "/mock/pic1.jpg",
      location: "Сибирь",
    },
  ]);

  useEffect(() => {
    getGenerateTours(props?.form ?? {}, setListTour)
  }, [])

  const [form, setForm] = useState({ location: "", date: "", user_id: 1 });

  // const [api, contextHolder] = notification.useNotification();

  const pagination = <PaginationCustom total={listTours.length}/>

  const listToursMap = (props?.listTours ?? []).map((item) => (
    <VerticalCard key={item.key} {...item} />
  ));

  // const handleSubmit = () => {
  //   fetch(`${HOST_URL}/generate_tour`, {
  //     method: "POST",
  //     headers: {
  //       "Content-Type": "application/json",
  //       "ngrok-skip-browser-warning": true,
  //     },
  //     body: JSON.stringify({
  //       user_id: 1,
  //       data_start: "26.01.25",
  //       data_end: "30.01.25",
  //       location: "Москва",
  //       hobby: ["музеи искусства", "спортзал"],
  //     }),
  //   })
  //     .then((res) => {
  //       if (!res.ok) {
  //         throw new Error(`HTTP error! Status: ${res.status}`);
  //       }
  //       return res.json();
  //     })
  //     .then((data) => setListTour(data))
  //     .catch((e) => {
  //       console.log(e);
  //       api.error({
  //         message: `Код ошибки: ${e.code || "unknown"}`,
  //         description: e.message,
  //         placement: "bottomRight",
  //       });
  //     });
  // };

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

  // if (!props?.listTours) return null;

  return (
    <>
      <div className={style.main}>
        <Header user={props?.user ? props.user : {}} />
        <h2>Рекомендованные туры</h2>
        <span>Подборка на основе ваших предпочтений</span>
        <Filters
          form={form}
          setForm={setForm}
          dataList={listTours}
          setListTour={setListTour}
        />
        {isLoading && <div className={style.loaderDiv}><Loader/></div>}
        {!isLoading && listToursMap}
         <div className={style.paginationDiv}>
                  {listTours.length != 0 && !isLoading && pagination}
                  </div>
      </div>
      <Footer />
    </>
  );
};

export default RecomendationPage;
