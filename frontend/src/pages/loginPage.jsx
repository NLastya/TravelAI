import {useState} from 'react';
import style from './loginpage.module.css'
import { Checkbox } from '@heroui/react';
import getAlert from '../helpers/getAlert';
import { HOST_URL } from '../config';
import { useNavigate } from 'react-router-dom';
import LS from '../store/LS';
import {LOCALSTORAGEAUTH} from '../config';


const Login = (props) => {
    const [form, setForm] = useState({login: '', password: ''});
    const [isLogged, setIsLogged] = useState(false);
    const [userId, setUserId] = useState(-1);
    const navigate = useNavigate();

    const handleClick = (e) => {
        if(LOCALSTORAGEAUTH){
            const user = LS.get('user')
            if (user.login === form.login && user.password === user.password)
                navigate('/popularTours')
            else
                getAlert('Ошибка при попытке войти', 'Ошибка', 'messages')
        }
            
        e.preventDefault(); 
        fetch(`/api/login`, {
            method: 'POST', 
            headers: {
                'Content-Type': 'application/json', 
            },
            body: JSON.stringify(form), 
        })
        .then(res => {
            if (!res.ok) {
                throw new Error('Ошибка соединения');
            }
            return res.json(); 
        })
        .then(body => {
            setIsLogged(true);
            console.log(body);
            setUserId(body?.user_id);
            navigate('/popularTours');
        })
        .catch(err => {
            getAlert('Ошибка при попытке войти', err.message, 'messages');
        });
    }

    return (<div className={style.main}>
        <div className={style.leftSide}>
            <h1>Вход</h1>
            <p>Войди чтобы  получить доступ к рекомендациях нейросети</p>
            <label className={style.inputLabel}> Почта
                            <input className={style.inputText} value={form?.login} placeholder='john.doe@gmail.com'
                            onChange={(e) => setForm(prev => ({...prev, login: e.target.value}))}
                            />
                        </label>
            <label className={style.inputLabel}> Пароль
                            <input className={style.inputText} value={form?.password} placeholder='**********************'
                            type="password"
                            onChange={(e) => setForm(prev => ({...prev, password: e.target.value}))}
                            />
                        </label>
            <div className={style.checker}>
                <div>
                    <input type="checkbox" id="remember" name="remember" />
                        <label htmlFor='remember'>Запомнить меня</label>
                </div>
                <a className={style.dangerText}>Забыл пароль</a>
            </div>
            <button className="mint-btn" onClick={(e) => handleClick(e)}>Войти</button>
            <span className={style.centerText}>Нет аккаунта? <a className={style.dangerText} href="/registration">Зарегестрироваться</a></span>

            <span className={style.centerText}>Войти с помощью</span>
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

export default Login;