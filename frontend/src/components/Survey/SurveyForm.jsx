import React, { useState } from 'react';
import CheckboxCustom from './CheckboxCustom';
import './SurveyForm.css'

const SurveyForm = () => {
  const surveyData = [
    {
      id: 0,
      question: "Какие виды отдыха вас интересуют?",
      options: [
        { id: 0, text: "Деловой" },
        { id: 1, text: "Этнический" },
        { id: 2, text: "Спортивный" },
        { id: 3, text: "Познавательный или культурно-развлекательный тур"},
        { id: 4, text: "Религиозный (в т.ч. паломничество)"}
      ],
      isOneChoose: false
    },
    {
      id: 1,
      question: "Как вы предпочитаете путешествовать?",
      options: [
        { id: 0, text: "С детьми" },
        { id: 1, text: "С семьей"},
        { id: 2, text: "С компанией среднего возраста 15-24 лет" },
        { id: 3, text: "С компанией среднего возраста 25-44 лет" },
        { id: 4, text: "С компанией среднего возраста 45-64 лет" },
      ],
      isOneChoose: false
    },
    {
      id: 2,
      question: "Какие у вас предпочтения в кухне?",
      options: [
        { id: 0, text: "Русская" },
        { id: 1, text: "Грузинская" },
        { id: 2, text: "Европейская" },
        { id: 3, text: "Восточная"},
        { id: 4, text: "Индийская"}
      ],
      isOneChoose: false
    },
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
        const formattedAnswers = surveyData.map(question => ({
        questionId: question.id,
        questionText: question.question,
        selectedOptions: answers[question.id] || [],
        selectedOptionsTexts: (answers[question.id] || []).map(optionId => 
        question.options.find(opt => opt.id === optionId)?.text || '')
    }));
    
    console.log("Форма отправлена. Ответы:", formattedAnswers);
  };

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