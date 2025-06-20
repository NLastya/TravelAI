import {useState} from 'react';
import style from './loginpage.module.css'
import getAlert from '../helpers/getAlert';
import { HOST_URL } from '../config';
import { useNavigate } from 'react-router-dom';

const Registration = (props) => {
    const [form, setForm] = useState({login: '', password: '', twice_password: '', city: '', name: ''});
    const [isLogged, setIsLogged] = useState(false);
    const navigate = useNavigate();

    const handleClick = (e) => {
        fetch(`${HOST_URL}/register`,
            {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json', 
                },
                body: JSON.stringify({login: form.login, password: form.password, city: form.city, name: form.name})
            }
        ).then(res => {
            if(!res.ok)
                throw new Error('error connection')
        }).then(body => {
            setIsLogged(true)
            navigate('/popularTours');
        })
        .catch(err => {
            getAlert('Ошибка при попытке войти', err.message, 'messages')
        }
        )
    }

    return (<div className={style.main}>
        <div className={style.leftSide}>
            <h1>Регистрация</h1>
            <p>Получи доступ к рекомендациям нейросети</p>
            <div className={style.inputContainer}>
                <label className={style.inputLabel}> Имя
                                <input className={style.inputText} value={form?.name} placeholder='Алексей'
                                onChange={(e) => setForm(prev => ({...prev, name: e.target.value}))}
                                />
                            </label>
                        <label className={style.inputLabel}> Почта
                            <input className={style.inputText} type="mail" value={form?.login} placeholder='example@mail.ru'
                            onChange={(e) => setForm(prev => ({...prev, login: e.target.value}))}
                            />
                        </label>
                <label className={style.inputLabel}> Город проживания *
                                <input className={style.inputText} value={form?.city} placeholder='Москва'
                                onChange={(e) => setForm(prev => ({...prev, city: e.target.value}))}
                                />
                            </label>
            </div>
            <div className={style.inputContainer}>
            <label className={style.inputLabel}> Пароль
                                <input className={style.inputText} value={form?.password} placeholder='**********************'
                                type="password"
                                onChange={(e) => setForm(prev => ({...prev, password: e.target.value}))}
                                />
                            </label>
                <label className={style.inputLabel}> Подтвердить пароль
                                <input className={style.inputText} value={form?.twice_password} placeholder='**********************'
                                type="password"
                                onChange={(e) => setForm(prev => ({...prev, twice_password: e.target.value}))}
                                />
                            </label>
            </div>
            <div className={style.checker}>
                <input type="checkbox" id="remember" name="remember" />
                    <label htmlFor='remember'>Я согласен с <a className={style.dangerText}>правилами</a> и доступном к <a className={style.dangerText}>персональным данным</a></label>
            </div>
            <button className="mint-btn" onClick={(e) => handleClick(e)}>Зарегестрироваться</button>
            <span className={style.centerText}>Есть аккаунт? <a className={style.dangerText} href="/auth-in">Войти</a></span>

            <span className={style.centerText}>Зарегестрироваться с помощью</span>
            <div className={style.operations}>
                        <button className={style.operationsBtn}>
                            <img src="./icons/google.jpg"/>
                        </button>
                        <button className={style.operationsBtn}><img src="./icons/vk.jpg"/></button>
                        <button className={style.operationsBtn}><img src="./icons/vk.jpg"/></button>
                </div>
        </div>

        <div className={style.carousel}>
            <img src="/login-ava.jpg" className={style.img}/>
        </div>

        <div id="messages" className={style.messages}/>
    </div>)
}

export default Registration;