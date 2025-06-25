import Footer from "../components/Footer/Footer"
import Header from "../components/Header"
import style from './searchpage.module.css'


const MainPage = () => {


    return(
    <>
    <Header/>
    <div className={style.main}>
            <p>Главная страница</p>
    </div>
    <Footer/>
    </>
)
}

export default MainPage;