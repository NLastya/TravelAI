import style from './personalpage.module.css';
import Header from '../components/Header';
import Footer from '../components/Footer/Footer';
import { useState } from 'react';
import ModalForm from '../components/ModalForm/ModalForm';
import { useNavigate } from 'react-router-dom';


const PersonalPage = ({setListTour}) => {
    const [modal, setModal] = useState(false);
    const navigate = useNavigate();


    return(
    <div className={style.wrap}>
    {modal && 
    <ModalForm setModal={setModal}  setListTour={ setListTour}/>
    }
    <Header/>
    <div className={style.main}>
        <div className={style.personalStyle}>
            {/* TODO: безопасные доступы к свойствам пропс props.firstName, props.bg */}
        <img className={style.img} src='/personal/bg.svg'/>
        <img src='/personal/avatar.svg'/>
        </div>

        <div className={style.tabs}></div>

        <h2>Действия</h2>
        <div className={style.operations}>
            <button className='operations-btn' onClick={() => {navigate('/favoritetours/1')}}>Избранное</button>
            <button className='operations-btn'
            onClick={(e) => {setModal(prev => !prev);}}
            >Сгенерировать тур</button>
            <button className='operations-btn' onClick={(e) => {navigate('/tours')}}>Рекомендации нейросети</button>
        </div>
    </div>
    <Footer/>
    </div>
    )

}

export default PersonalPage;