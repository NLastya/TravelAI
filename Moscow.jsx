import React from "react";
import Photo from "./image/moscow.png"

function Moscow() {
    return (
        <div className="Card">
            <img src={Photo} alt="Moskow"/>
            <div className="name_and_cost">
                <h3 className="name_location">Москва</h3>
                <span className="price">$455</span>
            </div>
            
            <p className="description">
            Город, где история, культура и современность 
            сливаются в единое захватывающее путешествие.
            </p>

        </div>
    )
}

export default Moscow
