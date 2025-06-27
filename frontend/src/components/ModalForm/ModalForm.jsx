import { useEffect, useState } from "react";
import {Select} from 'antd';
import style from './modalform.module.css';
import { notification } from 'antd';
import { HOST_URL } from '../../config';
import {useNavigate} from 'react-router-dom';

import { DatePicker } from 'antd';
import dayjs from "dayjs";
import {disabled7DaysDate} from '../dataPicker/datePicker';
const { RangePicker } = DatePicker;
import {options} from '../../consts';


const dateToBd = (date) => {
  console.log(typeof(date), date)
    const y = date.getYear()
    const m = date.getMonth() + 1
    const d = date.getDate()

    console.log('date:', `${d}.${m}.${y}`)
    return `${d}.${m}.${y}`
}


const end_date = (new Date()).getTime() + 432000 * 1000;

const ModalForm = ({setModal, setListTour}) => {
    const [form, setForm] = useState({location: '', data_start: new Date(), data_end: new Date(end_date) , hobbies: []});
    const [formError, setFormError] = useState(false);
    const [api, contextHolder] = notification.useNotification();

    const handleChange = (value) => {setForm(prev => ({...prev, hobbies: [value]}))}

    const sendForm = () => {
        console.log(form)
        if(!(form.location && form.data_start && form.data_end && form.hobbies)) {
            setFormError(true);
        } else {
          console.log('form:', {})
            fetch(`/api/generate_tour`, {
                method: 'POST', 
                headers: {
                  'Content-Type': 'application/json', 
                  'ngrok-skip-browser-warning': true,
                },
                body: JSON.stringify(
                  // eslint-disable-next-line no-constant-binary-expression
                  {...form, 
                    data_start: typeof(data_start) === 'Date' ? dateToBd(form?.date_start) : form?.data_start,
                    data_end: typeof(data_end) === 'Date' ? dateToBd(form?.date_end) : form?.data_end,
                    }

                  ?? { 
                  user_id: 2,
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
            <div className={style.modalHeader}><h3>Выберите город и даты</h3><button
              onClick={() => {setModal(false)}}
            ><img src="" alt="close"/></button></div>
            <label className={style.inputLabel}> Даты отправки и прибытия
                {/* <input className={style.inputText} value={form?.date}
                onChange={(e) => setForm(prev => ({...prev, date: e.target.value}))}
                /> */}
                <RangePicker 
                disabledDate={disabled7DaysDate}
                value={[dayjs(form?.data_start), dayjs(form?.data_end)]}
                format="YYYY-MM-DD"
                allowClear={false}
                 onChange={(value) => {
                    setForm(prev => ({...prev, data_start: dateToBd((value[0]).format('DD-MM-YYYY')), data_end: dateToBd(value[1]).format('DD-MM-YYYY') }))
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
            //  mode='tags'
              mode="tags"
              style={{ width: '100%' }}
              onChange={handleChange}
              tokenSeparators={[',']}
              options={options}
                placeholder='Выберите предпочтения'
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