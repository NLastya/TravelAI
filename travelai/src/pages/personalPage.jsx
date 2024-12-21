import style from './personalpage.module.css';
import Header from '../components/Header';
import Footer from '../components/Footer/Footer';
import { useState } from 'react';
import ModalForm from '../components/ModalForm/ModalForm';


const PersonalPage = ({setListTour}) => {
    const [modal, setModal] = useState(false);


    return(
    <div className="wrap">
    {modal && 
    <ModalForm setModal={setModal}  setListTour={ setListTour}/>
    }
    <Header/>
    <div className={style.main}>
        <div className={style.personalStyle}>
            {/* TODO: безопасные доступы к свойствам пропс props.firstName, props.bg */}
        <img src='/personal/bg.svg'/>
        <img src='/personal/avatar.svg'/>
        </div>

        <div className={style.tabs}></div>

        <h2>Действия</h2>
        <div className={style.operations}>
            <button className='operations-btn'>Избранное</button>
            <button className='operations-btn'
            onClick={() => {setModal(prev => !prev);}}
            >Сгенерировать тур</button>
            <button className='operations-btn'>Рекомендации нейросети</button>
        </div>
    </div>
    <Footer/>
    </div>
    )

}

export default PersonalPage;