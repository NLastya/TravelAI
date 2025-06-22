import React, { useState } from 'react';


const CheckboxCustom = ({ options, isOneChoose, onChange }) => {
  const [selectedOptions, setSelectedOptions] = useState([]);

  const handleOptionChange = (optionId) => {
    let newSelected;
    if (isOneChoose) {
      newSelected = [optionId];
    } else {
      if (selectedOptions.includes(optionId)) {
        newSelected = selectedOptions.filter(id => id !== optionId);
      } else {
        newSelected = [...selectedOptions, optionId];
      }
    }
    setSelectedOptions(newSelected);
    onChange(newSelected);
  };

  return (
    <div className="options-container">
      {options.map(option => (
        <div key={option.id} className="option-item">
          <input
            className="option-input"
            type={isOneChoose ? "radio" : "checkbox"}
            id={`option-${option.id}`}
            checked={selectedOptions.includes(option.id)}
            onChange={() => handleOptionChange(option.id)}
          />
          <label className="option-label" htmlFor={`option-${option.id}`}>{option.text}</label>
        </div>
      ))}
    </div>
  );
};


export default CheckboxCustom;