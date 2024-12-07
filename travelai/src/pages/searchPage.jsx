/* eslint-disable react/prop-types */
import React, {useEffect, useState} from 'react'
import Header from '../components/Header';
import style from './searchpage.module.css';
import Filters from '../components/Filters/Filters'
import VerticalCard from '../components/VerticalCard/VerticalCard';
import { notification } from 'antd';
import Footer from '../components/Footer/Footer'
import { HOST_URL } from '../config';

const SearchPage = (props) => {
    const [isLoading, setIsLoading] = useState(false);
    const [listTours, setListTour] = useState([{date: '04.01.25'}]);
    const [form, setForm] = useState({location: '', date: ''})

    const [api, contextHolder] = notification.useNotification();

    const listToursMap = listTours.map(item => (<VerticalCard key={item.key} {...item}/>) )


    useEffect(() => {
        setIsLoading(true);
        fetch(`${HOST_URL}/generate_tour`, {
            user_id: 1,
            data_start: '26.01.25',
            data_end: '30.01.25',
            location: 'Москва',
            hobby: ['музеи искусства', 'спортзал'],
        })
        .then(res => res.json())
        .then(res => setListTour(res))
        .catch(e => {
            console.log(e);
            api.error({message: `Код ошибки: ${e.code}`,
                description: e.message,
                placement: 'bottomRight'});
        })
        setIsLoading(false);

    }, [])

    // if(isLoading)
    //     return null;


    return(
    <>
    <div className={style.main}>
        <Header user={props?.user ? props.user : {}}/>
        <Filters form={form} setForm={setForm}/>
        {!isLoading && listToursMap
        }
        
    </div>
    <Footer/>
    </>
    )


}

export default SearchPage;