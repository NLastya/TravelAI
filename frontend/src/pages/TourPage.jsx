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
import CardTour from "../components/cardTour/cardTour";
import RatingCard from '../components/ratingCard';
import ButtonLike from '../components/buttonLike';
import Box from '../components/Card/Box'
import { PlacesList } from "../components/Card/Box";
import {FullCards} from '../components/Card/vCard'


const mockTour =  
{
  "tour_id": 1,
  "title": "Тур по Белгород — день 1",
  "date": [
    "2022-02-21",
    ""
  ],
  "location": "Белгород",
  "rating": 4,
  "relevance": 1,
  "url": "",
  "places": [
    {
      "id_place": 0,
      "name": "Южный Парк",
      "location": "Белгород",
      "rating": "нет данных",
      "date": "2",
      "description": "Парк",
      "photo": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSGKPdm1NTslz32yLdZKLBH41Pu4fPBu7ggAQ&s",
      "mapgeo": [
        0,
        0
      ]
    },
    {
      "id_place": 0,
      "name": "Парк им. Юрия Гагарина",
      "location": "Белгород",
      "rating": "нет данных",
      "date": "1",
      "description": "Парк",
      "photo": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSGKPdm1NTslz32yLdZKLBH41Pu4fPBu7ggAQ&s",
      "mapgeo": [
        0,
        0
      ]
    },
    {
      "id_place": 0,
      "name": "Котофей",
      "location": "Белгород",
      "rating": "нет данных",
      "date": "2",
      "description": "Парк",
      "photo": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSGKPdm1NTslz32yLdZKLBH41Pu4fPBu7ggAQ&s",
      "mapgeo": [
        0,
        0
      ]
    },
    {
      "id_place": 0,
      "name": "Музей-диорама «Курская битва. Белгородское направление»",
      "location": "Белгород",
      "rating": "нет данных",
      "date": "4",
      "description": "Музей",
      "photo": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSGKPdm1NTslz32yLdZKLBH41Pu4fPBu7ggAQ&s",
      "mapgeo": [
        0,
        0
      ]
    }
  ],
  "categories": [],
  "description": "Увлекательный тур для всей семьи!",
  "is_favorite": false
}



const TourPage = (props) => {
  const { tour_id } = useParams();
  const [dataTour, setDataTour] = useState(mockTour);

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
                <div className={style.innerRatingRow}>
                <h3>{props?.name ? dataTour?.tour : "Сибирь Тур№1"}</h3>
                <Rate value={dataTour?.rating}></Rate> {(dataTour?.rate ? dataTour?.rate + getTourText(dataTour.rate) : '') ?? "5 звезд"}              
                <div className={style.infoRow}>
              </div>
                </div>
                <p className={style.location}>
                  <img src="/icons/location.svg" />
                  <span>{ "Сибирь, ул. Прохорова, 34755"}</span>
                </p>
                <RatingCard rating={dataTour?.rating ?? '4.2'}/>
              </div>

              <div className={style.dateVisit}>
                <p>Даты посещения</p>
                <p className={style.date}>cl
                  {dataTour?.date ? dataTour?.date : "26.01.25 - 30.01.25"}
                </p>
                <p>{(dateDiff ? dateDiff + getDateText(dateDiff) : '') ?? '5 дней'}</p>
              </div>
            </div>
            <div className={style.buttons}>
             <ButtonLike/>
              <button className={"mint-btn"}>Посмотреть тур</button>
            </div>
          </div>
        </div>
        <div className={style.cardsTourDiv}>
          {/* {(mockPlaces?.places).map((key, item) =><Box key={key} {...item}/>)} */}
          {/* <PlacesList placesData={dataTour.places} /> */}
          {<FullCards arr={dataTour?.places}/>}
          
        </div>
        <div className={style.disc}>
          <h3 className={style.h3dsic}>Описание</h3>
          <p>
            {props?.description
              ? props?.description
              : "Насыщенный впечатлениями маршрут сразу по трем Сибирским регионам! Вас ждут уникальные музеи Хакасии с гастрономией региона, сибирская деревня \
                 – Шушенское, буддийские артефакты Тувы, мировое достояние – золото Скифов и музыка хоомей."}
          </p>
          <div className={style.cards}>
            {(props?.categories ?? []).map((id, item)=> <CardTour title={item} key={id}/>)}
          </div>
        </div>
        <div className={style.map}>
          <div className={style.s}>
            <h3>Маршрут</h3>
            <button onClick={() => {window.location.href = "https://yandex.ru/maps/213/moscow/?ll=37.740444%2C55.651073&z=10";}}>Посмортеть на Яндекс Карте</button>
          </div>
        </div>
        <div className={style.mapDiv}>
        <CustomMap routeArr={dataTour?.geomap ?? routeArr} points={dataTour?.geomap}/>
        </div>
      </div>
      <Footer />
    </>
  );
};

export default TourPage;
