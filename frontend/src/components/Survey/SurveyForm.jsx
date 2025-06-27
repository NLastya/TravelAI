import React, { useEffect, useState } from 'react';
import CheckboxCustom from './CheckboxCustom';
import './SurveyForm.css';
import { postUserInterests} from '../../helpers/fetchRoute';
import { LOCALSTORAGEAUTH } from '../../config';
import LS from '../../store/LS';
import { HOST_URL } from '../../config';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../hooks/useAuth';


const SurveyForm = ({form, setForm, isLogged, setIsLogged}, ...props) => {
  const navigate = useNavigate();
  const [isSuccessful, setIsSuccessfull] = useState(false);
  const {setUserId} = useAuth();

  const postRegistration = (form, setIsSuccessfull) => {
        if(LOCALSTORAGEAUTH){
            LS.set('user', JSON.stringify({login: form.login, password: form.password, city: form.city, name: form.name}))
            setUserId(2)
            const user_id = 2
            navigate(`/user/${user_id}`)
        }
        else{
        fetch(`/api/register`,
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
          const userId = body?.user_id
          setUserId(userId);
          // setIsSuccessfull(true)
            // setIsLogged(true)
            navigate('/popularTours');
        })
        .catch(err => {
            // getAlert('Ошибка при попытке войти', err.message, 'messages')
        }
        )}
    }


  const surveyData = [
    {
      id: 0,
      question: "Какие виды отдыха вас интересуют?",
      options: [
        { id: "delovoy", text: "Деловой" },
        { id: "etnicheskiy", text: "Этнический" },
        { id: "sportivnyj", text: "Спортивный" },
        { id: "poznavatelnyj_kulturno_razvlekatelnyj", text: "Познавательный или культурно-развлекательный тур"},
        { id: "religioznyj", text: "Религиозный (в т.ч. паломничество)"}
      ],
      isOneChoose: false
    },
    {
      id: 1,
      question: "Как вы предпочитаете путешествовать?",
      options: [
        { id: "s_detmi", text: "С детьми" },
        { id: "s_semej", text: "С семьей"},
        { id: "s_kompaniej_15_24", text: "С компанией среднего возраста 15-24 лет" },
        { id: "s_kompaniej_25_44", text: "С компанией среднего возраста 25-44 лет" },
        { id: "s_kompaniej_45_66", text: "С компанией среднего возраста 45-64 лет" },
      ],
      isOneChoose: false
    },
    {
      id: 2,
      question: "Какие у вас предпочтения в кухне?",
      options: [
        { id: "russian", text: "Русская" },
        { id: "gryzinskaya", text: "Грузинская" },
        { id: "evropeiskya", text: "Европейская" },
        { id: "vostochnaya", text: "Восточная"},
        { id: "indiskaya", text: "Индийская"}
      ],
      isOneChoose: false  
    }
];
  const [answers, setAnswers] = useState({});

  const handleAnswerChange = (questionId, selectedOptions) => {
    setAnswers(prev => ({
      ...prev,
      [questionId]: selectedOptions
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    let resData = {};
    console.log('res:', answers)
      for (const key in answers) {
        if (Object.prototype.hasOwnProperty.call(answers, key)) {
          for (let i in answers[key]) {
            const item = answers[key][i]
            resData[item] = true;
          }
        }
      }

    console.log('survey:', resData)
    postRegistration({...form[1]}, setIsSuccessfull)
    postUserInterests(1, {...form[2], ...resData}, () => {}, setIsSuccessfull)
  };

  useEffect(() => {
    if(isSuccessful) navigate('/popularTours')
  },
[isSuccessful])

  return (
    <form onSubmit={handleSubmit} className="survey-form">
      <h2>Расскажите о себе</h2>
      <p>Эта информация поможет подбирать более релевантные
туры</p>
      
      {surveyData.map(question => (
        <div key={question.id} className="question-block">
          <h4>{question.question}</h4>
          <CheckboxCustom
            options={question.options}
            isOneChoose={question.isOneChoose}
            onChange={(selected) => handleAnswerChange(question.id, selected)}
          />
        </div>
      ))}
      
      <button type="submit" className="submit-btn">Отправить</button>
    </form>
  );
};

export default SurveyForm;
