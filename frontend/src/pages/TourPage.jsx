import style from "./tourpage.module.css";
import { useParams } from "react-router-dom";
import { useState, useEffect } from "react";
import { HOST_URL } from "../config";
import Header from "../components/Header";
import Footer from "../components/Footer/Footer";
import { Rate } from "antd";
import {
  YMapComponentsProvider,
  YMap,
  YMapDefaultSchemeLayer,
  YMapDefaultFeaturesLayer,
  YMapDefaultMarker,
  // ...other components
} from "ymap3-components";
import CustomMap from "../components/Map";
import { getTourById } from "../helpers/fetchRoute";
import getTourText from "../helpers/getRatingText";
import getDateText from "../helpers/getDateText";

const TourPage = (props) => {
  const { tour_id } = useParams();
  const [dataTour, setDataTour] = useState({
    tour_id: -1,
    title: "",
    date: "",
    location: "",
    rating: 0,
    relevance: 0,
    places: [],
    description: '',
  });

  let dateDiff = ''
  if (dataTour.length > 1)
      dateDiff = new Date(dataTour.date[1] - dataTour.date[0]) 

  // TODO: перенести на rtk - query
  useEffect(() => {
    getTourById(tour_id, setDataTour);
  }, []);

  const [location, setLocation] = useState({
    zoom: 10,
    center: [25.229762, 55.289311],
  });

  const routeArr = [
    { coords: [73.3654, 54.9914] },
    { coords: [73.3925, 54.9998] },
  ];

  return (
    <>
      <Header />
      <div className={style.main}>
        <div className={style.card}>
          <div className={style.bothInfoDate}>
            <div className={style.bothInfo}>
              <div className={style.listInfo}>
                <h3>{props?.name ? dataTour?.tour : "Сибирь Тур№1"}</h3>
                <p className={style.location}>
                  <imf src="./location.svg" />
                  {dataTour?.location
                    ?? "Сибирь, ул. Прохорова, 34755"}
                </p>
                <p>
                  <Rate></Rate> {(dataTour?.rate ? dataTour?.rate + getTourText(dataTour.rate) : '') ?? "5 звезд"}
                </p>
                <div className={style.infoRow}></div>
              </div>
              <div>
                <p>Даты посещения</p>
                <p className={style.date}>
                  {dataTour?.date ? dataTour?.date : "26.01.25 - 30.01.25"}
                </p>
                <p>{(dateDiff ? dateDiff + getDateText(dateDiff) : '') ?? '5 дней'}</p>
              </div>
            </div>
            <div className={style.buttons}>
              <button className={"mint-btn"}>Посмотреть тур</button>
              <button className={"btn-like"}>
                <img src="./icons/like.svg" />
              </button>
            </div>
          </div>
        </div>

        <div className={style.disc}>
          <h3>Описание</h3>
          <p>
            {props?.description
              ? props?.description
              : "Насыщенный впечатлениями маршрут сразу по трем Сибирским регионам! Вас ждут уникальные музеи Хакасии с гастрономией региона, сибирская деревня \
                 – Шушенское, буддийские артефакты Тувы, мировое достояние – золото Скифов и музыка хоомей."}
          </p>
        </div>

        <div className={style.map}>
          <h3>Маршрут</h3>
          <YMapComponentsProvider
            apiKey={"9bb13193-cc52-4a38-88b3-11179a14242c"}
          >
            <YMap location={location}>
              <YMapDefaultSchemeLayer />
              <YMapDefaultFeaturesLayer />
              <YMapDefaultMarker coordinates={[60, 105]} />

              
            </YMap>
          </YMapComponentsProvider>
        </div>
        <CustomMap routeArr={routeArr} />
      </div>
      <Footer />
    </>
  );
};

export default TourPage;
