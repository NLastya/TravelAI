import style from './card.module.css';

const CardTour = ({title, type}={title: '', type: 'park'}, ...props) => {
    return( 
    <div className={style.card}>
         <img className={style.icon} src="/icons/cardFeature.svg"/>
        <p className={style.text}>{title}</p>
    </div>)
}

export default CardTour;