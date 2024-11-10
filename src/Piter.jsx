import React from "react";
import Photo from "./image/piter.png"

function Piter() {
    return (
        <div className="Card">
            <img src={Photo} alt="Saint-Petersburg"/>
            <div className="name_and_cost">
                <h3 className="name_location">Санкт-Петербург</h3>
                <span className="price">$400</span>
            </div>
            
            <p className="description">
            Город с богатой историей, мощеными улицами и романтичной атмосферой.
            </p>

        </div>
    )
}

export default Piter
