import style from './tourpage.module.css';
import {useParams} from 'react-router-dom';
import {useState, useEffect} from 'react';
import { HOST_URL } from '../config';
import Header from '../components/Header';
import Footer from '../components/Footer/Footer';
import {Rate} from 'antd';
import {
    YMapComponentsProvider,
    YMap,
    YMapDefaultSchemeLayer,
    YMapDefaultFeaturesLayer,
    YMapDefaultMarker,
    // ...other components
  } from "ymap3-components";
import CustomMap from '../components/Map';


const TourPage = (props) => {
    const {tour_id} = useParams()
    const [dataTour, setDataTour] = useState({}); 
    // TODO: перенести на rtk - query
    useEffect(() => {
        fetch(`${HOST_URL}/tour/1`)
        .then(res => res.json())
        .then(res => {
            setDataTour(res);
        }
    )
        .catch(e => {
            console.log(e);
            // TODO: написать моки чтобы работал переход вне catch
            // api.error({message: `Код ошибки: ${e.code}`,
            //     description: e.message,
            //     placement: 'bottomRight'});
        }
    )

    }, [])

    const [location, setLocation] = useState({zoom: 10,
        center: [25.229762, 55.289311]});

    const routeArr = [
    {coords: [73.3654, 54.9914]},
    {coords: [73.3925, 54.9998]},
    ]

    return(
        <>
        <Header/>
        <div className={style.main}>
             <div className={style.card}>
                <div className={style.bothInfoDate}>
                    <div className={style.bothInfo}>
                    <div className={style.listInfo}>
                        <h3>{props?.name ? props?.name : 'Сибирь Тур№1'}</h3>
                        <p className={style.location}>
                            <imf src="./location.svg"/>
                            {props?.location ? props?.location : 'Сибирь, ул. Прохорова, 34755'}
                        </p>
                        <p>
                            <Rate></Rate> {props.rate? props?.rate : '5 звезд'}
                        </p>

                        <div className={style.infoRow}></div>
                    </div>
                    <div>
                        <p>Даты посещения</p>
                        <p className={style.date}>{props?.date ? props?.date: '26.01.25 - 30.01.25'}</p>
                        <p>5 дней</p>
                    </div>
                    </div>
                    <div className={style.buttons}>
                        <button className={'mint-btn'}>Посмотреть тур</button>
                        <button className={'btn-like'}>
                            <img src="./icons/like.svg"/>
                        </button>
                    </div>
                </div>
            </div>

            <div className={style.disc}>
                <h3>Описание</h3>
                <p>{props?.description ? props?.description : 'Насыщенный впечатлениями маршрут сразу по трем Сибирским регионам! Вас ждут уникальные музеи Хакасии с гастрономией региона, сибирская деревня \
                 – Шушенское, буддийские артефакты Тувы, мировое достояние – золото Скифов и музыка хоомей.'}</p>
            </div>

            <div className={style.map}>
                <h3>Маршрут</h3>
                <YMapComponentsProvider apiKey={'9bb13193-cc52-4a38-88b3-11179a14242c'}>
                    <YMap location={location}>
                    <YMapDefaultSchemeLayer />
                    <YMapDefaultFeaturesLayer />
                    <YMapDefaultMarker
                    coordinates={[60, 105]}
                    />
                </YMap>
                </YMapComponentsProvider>
            </div>
                <CustomMap routeArr={routeArr}/>
        </div>
        <Footer/>
        </>
    )

} 

export default TourPage;