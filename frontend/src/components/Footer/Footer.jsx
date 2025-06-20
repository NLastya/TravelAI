import style from './footer.module.css';

const Footer = () => {
    return (
        <div className={style.footer}>
            <img src='/icons/logo.svg' alt='svg'/>
            <p>Наш блог</p>
            <p>О нас</p>
            <p>Нейросеть</p>
            <p>Связаться с нами</p>
        </div>

    )
}

export default Footer;