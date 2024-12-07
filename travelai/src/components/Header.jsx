import style from './header.module.css';

const Header = (props) => {


    return (
    <div className={style.header}>
        <img src='./icons/logo.svg' alt='logo'/>

        <div className={style.user}>
            <img src='/icons/Ellipse 1.svg' alt='user avatar'/>
            <span>{props?.username ? props?.username : 'Влад З.'}</span>
        </div>

    </div>)

}

export default Header;