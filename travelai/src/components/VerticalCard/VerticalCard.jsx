import React from 'react';
import style from 'card.modules.css'

const VerticalCard = (props) => {

    return (<div className={style.card}>
        <div className={style.bothInfoDate}>
            <div className={style.listInfo}>
                <h3>{props?.name ? props?.name : 'Сибирь Тур№1'}</h3>
                <p className={style.locatыion}>
                    <imf src="./geo.svg"/>
                    {props?.location? props?.location: 'Сибирь - Сибирь'}
                </p>

                <div className={style.infoRow}></div>

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