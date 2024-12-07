import { useState } from "react";
import {Select} from 'antd';
import style from './modalform.module.css';
import { notification } from 'antd';
import { HOST_URL } from '../../config';
import {useNavigate} from 'react-router-dom'


const ModalForm = ({setModal}) => {
    const [form, setForm] = useState({location: '', date: '', hobies: []});

  
const options = [
    { value: '1', label: 'Театр' },
    // { value: 'Спортзал', label: 'Спортзал' },
    // { value: 'Спа', label: 'Спа' },
    // { value: 'Бассейн', label: 'Бассейн' },
    // { value: 'Животные', label: 'Животные' },
    // { value: 'Галереи', label: 'Галереи' },
    // { value: 'Бары', label: 'Бары' },
    // { value: 'Рестораны', label: 'Рестораны' },
    // { value: 'Кинотеатры', label: 'Кинотеатры' },
    // { value: 'Клубы', label: 'Клубы' },
    // { value: 'Пляжи', label: 'Пляжи' },
    // { value: 'Парки', label: 'Парки' },
    // { value: 'Музеи', label: 'Музеи' },
    // { value: 'Фестивали', label: 'Фестивали' },
    // { value: 'Концерты', label: 'Концерты' },
    // { value: 'Кафе', label: 'Кафе' },
    // { value: 'Библиотеки', label: 'Библиотеки' },
    // { value: 'Зоопарки', label: 'Зоопарки' },
    // { value: 'Аквапарки', label: 'Аквапарки' },
    // { value: 'Цирки', label: 'Цирки' },
    // { value: 'Стадионы', label: 'Стадионы' },
    // { value: 'Теннисные корты', label: 'Теннисные корты' },
    // { value: 'Боулинг', label: 'Боулинг' },
    // { value: 'Картинг', label: 'Картинг' },
    // { value: 'Пейнтбол', label: 'Пейнтбол' },
    // { value: 'Квесты', label: 'Квесты' },
    // { value: 'Туристические маршруты', label: 'Туристические маршруты' },
    // { value: 'Горы', label: 'Горы' },
    // { value: 'Озера', label: 'Озера' },
    // { value: 'Реки', label: 'Реки' },
    // { value: 'Лес', label: 'Лес' },
    // { value: 'Поля', label: 'Поля' },
    // { value: 'Сады', label: 'Сады' },
    // { value: 'Фермы', label: 'Фермы' },
    // { value: 'Ранчо', label: 'Ранчо' },
    // { value: 'Винодельни', label: 'Винодельни' },
    // { value: 'Пивоварни', label: 'Пивоварни' },
    // { value: 'Фабрики', label: 'Фабрики' },
    // { value: 'Заводы', label: 'Заводы' },
    // { value: 'Театральные студии', label: 'Театральные студии' },
    // { value: 'Кулинарные студии', label: 'Кулинарные студии' },
    // { value: 'Танцевальные студии', label: 'Танцевальные студии' },
    // { value: 'Йога центры', label: 'Йога центры' },
    // { value: 'Пилатес студии', label: 'Пилатес студии' },
    // { value: 'Фитнес клубы', label: 'Фитнес клубы' },
    // { value: 'Бильярдные', label: 'Бильярдные' },
    // { value: 'Караоке клубы', label: 'Караоке клубы' },
    // { value: 'Бары с живой музыкой', label: 'Бары с живой музыкой' },
    // { value: 'Арт-студии', label: 'Арт-студии' },
    // { value: 'Мастер-классы', label: 'Мастер-классы' },
    // { value: 'Выставки', label: 'Выставки' },
    // { value: 'Фотостудии', label: 'Фотостудии' }
];

    const handleChange = (value) => {setForm(prev => ({...prev, hobies: [...prev.hobies, value]}))}
    const navigate = useNavigate();

    const [api, contextHolder] = notification.useNotification();

    const sendForm = () => {
        fetch(`${HOST_URL}/generate_tour`, {
            user_id: 1,
            data_start: '26.01.25',
            data_end: '30.01.25',
            location: 'Москва',
            hobby: ['музеи искусства', 'спортзал'],
        })
        .then(res => res.json())
        .then(res => {
            setListTour(res);
            navigate('/tours');
        }
    )
        .catch(e => {
            console.log(e);
            // TODO: написать моки чтобы работал переход вне catch
            navigate('/tours');
            api.error({message: `Код ошибки: ${e.code}`,
                description: e.message,
                placement: 'bottomRight'});
        })

    }

    return(
    <>
        <div className={style.modal}>
            <h3>Выберите место и даты</h3>
            <label className={style.inputLabel}> Даты отправки и прибытия
                <input className={style.inputText} value={form?.date}
                onChange={(e) => setForm(prev => ({...prev, date: e.target.value}))}
                />
            </label>
            <label className={style.inputLabel}> Город
                <input className={style.inputText} value={form?.location}
                onChange={(e) => setForm(prev => ({...prev, location: e.target.value}))}
                />

            <h3>Предпочтения</h3>
            <Select 
            mode='tags'
            style={{width: '100%'}}
            placeholder='Выберите предпочтения'
            onChange={() => handleChange()}
            options={options}
            />
            </label>
            <button className='mint-btn' onClick={() => sendForm()}>Сгенерировать</button>
        </div>
        <div className={style.overlay} onClick={() => setModal(false)}></div>
        </>
    )
}

export default ModalForm;