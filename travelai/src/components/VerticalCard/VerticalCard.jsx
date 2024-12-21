/* eslint-disable react/prop-types */
import React from 'react';
import {Rate} from 'antd';
import style from './card.module.css';


const VerticalCard = (props) => {

    return (
    <div className={style.card}>
        <img src={props?.image ? props?.image: '/mock/pic1.jpg'}/>
        <div className={style.bothInfoDate}>
            <div className={style.bothInfo}>
            <div className={style.listInfo}>
                <h3>{props?.name ? props?.name : 'Сибирь Тур№1'}</h3>
                <p className={style.location}>
                    <imf src="./location.svg"/>
                    {props?.location ? props?.location : 'Сибирь, ул. Прохорова, 34755'}
                </p>
                <p>
                    <Rate></Rate> {props.rate? props?.rate : '5 звезд оценка'}
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
    </div>)


}

export default VerticalCard;