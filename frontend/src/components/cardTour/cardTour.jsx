import style from './card.module.css';

const CardTour = ({title, type}={title: '', type: 'part'}, ...props) => {
    return( 
    <div className={style.card}>
        {/* {type === 'rating'} */}
        {type === 'park' && <img src="/icons/cardFeature.svg"/>}
        {type === 'club' && <img src="/icons/cardFeature.svg"/>}
        {type === 'sport' && <img src="/icons/cardFeature.svg"/>}
        {type === 'culture' && <img src="/icons/cardFeature.svg"/>}

        <p className={style.text}>{title}</p>
    </div>)
}

export default CardTour;