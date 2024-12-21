import { useState } from "react";
import {Select} from 'antd';
import style from './modalform.module.css';
import { notification } from 'antd';
import { HOST_URL } from '../../config';
import {useNavigate} from 'react-router-dom';

import { DatePicker } from 'antd';
import dayjs from "dayjs";
const { RangePicker } = DatePicker;


const ModalForm = ({setModal, setListTour}) => {
    const [form, setForm] = useState({location: '', data_start: '2024-11-12', data_end: '2024-11-31', hobies: []});
    const [formError, setFormError] = useState(false);

  
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

    const handleChange = (value) => {setForm(prev => ({...prev, hobies: [value]}))}
    // const navigate = useNavigate();

    const [api, contextHolder] = notification.useNotification();

    const sendForm = () => {
        console.log(form)
        if(!(form.location && form.data_start && form.data_end && form.hobies)) {
            setFormError(true);
        } else {
            fetch(`${HOST_URL}/generate_tour`, {
                method: 'POST', 
                headers: {
                  'Content-Type': 'application/json', 
                  'ngrok-skip-browser-warning': true,
                },
                body: JSON.stringify({ 
                  user_id: 1,
                  data_start: '26.01.25',
                  data_end: '30.01.25',
                  location: 'Москва',
                  hobby: ['музеи искусства', 'спортзал'],
                }),
              })
              .then(res => {
                if (!res.ok) {
                  throw new Error(`HTTP error! Status: ${res.status}`);
                }
                return res.json();
              })
              .then(data => setListTour(data))
              .catch(e => {
                console.log(e);
                api.error({
                  message: `Код ошибки: ${e.code || 'unknown'}`, 
                  description: e.message,
                  placement: 'bottomRight',
                });
              });

        }
    }

    return(
    <>
        <div className={style.modal}>
            <h3>Выберите место и даты</h3>
            <label className={style.inputLabel}> Даты отправки и прибытия
                {/* <input className={style.inputText} value={form?.date}
                onChange={(e) => setForm(prev => ({...prev, date: e.target.value}))}
                /> */}
                <RangePicker 
                value={[dayjs(form?.data_start), dayjs(form?.data_end)]}
                format="YYYY-MM-DD"
                allowClear={false}
                 onChange={(value) => {
                    setForm(prev => ({...prev, data_start: (value[0]).format('YYYY-MM-DD'), data_end: (value[1]).format('YYYY-MM-DD') }))
                    console.log((value[0]).format('DD-MM-YYYY'))
                 }
                }
                />
            </label>
            <label className={style.inputLabel}> Город
                <input className={style.inputText} value={form?.location}
                onChange={(e) => setForm(prev => ({...prev, location: e.target.value}))}
                />

            <h3>Предпочтения</h3>
            <Select 
            mode='tags'
            style={{width: '100%', height: '42px',
                border: '1px solid black',
                background: 'white',
                color: '#1C1B1F',
                boxSizing: 'border-box',
                borderRadius: '2px', }}
            placeholder='Выберите предпочтения'
            onChange={(value) => handleChange(value)}
            options={options}
            />
            </label>
            {formError && <span style={{color: 'red', fontSize: '12px'}}>Заполните все поля</span>}
            <button className='mint-btn' onClick={() => sendForm()}>Сгенерировать</button>
        </div>
        <div className={style.overlay} onClick={() => setModal(false)}></div>
        </>
    )
}

export default ModalForm;