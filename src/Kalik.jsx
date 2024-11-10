import React from "react";
import Photo from "./image/kalik.png"

function Kalik() {
    return (
        <div className="Card">
            <img src={Photo} alt="Kaliningrad"/>
            <div className="name_and_cost">
                <h3 className="name_location">Калининград</h3>
                <span className="price">$600</span>
            </div>
            
            <p className="description">
            Город, где встречаются Балтийское море, средневековая архитектура и немецкое наследие.
            </p>

        </div>
    )
}

export default Kalik