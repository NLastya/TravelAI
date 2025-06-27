import React from "react";
import Loc_Photo from "./image/krpol.jpg"
import Pointer from "./image/pointer_2.png"
import Star from "./image/star_2.png"
import './card.css'

const CardCustom2 = (props) {
    return (
        <div>
            <img className="Location_photo" src={Loc_Photo} alt="Location_photo"/>
            <div className="Card">
                
                <h3 className="Location_name">Красная поляна</h3>
                <div className="Adress">
                    <img className="Pointer" src={Pointer}/>
                    <p className="Location_adress">Gornaya 1, SOCHI, Russia, 354392</p>
                </div>
                
                <p className="Location_description">
                Хорошее место для отдыха и генерации фантазии Chat GPT. Хвала Chat GPT.
                </p>
                
                <div className="Rating"> 
                    <div className="Stars">
                        <img className="Star" src={Star}/>
                        <img className="Star" src={Star}/>
                        <img className="Star" src={Star}/>
                        <img className="Star" src={Star}/>
                        <img className="Star" src={Star}/>
                    </div>
                    <p className="Stars_count">5</p>
                    <p className="Stars_text"> Star Hotel</p>
                
                </div>

                <div className="Date">
                    <p className="Date_text">Даты вылета</p>
                    <p className="Date_days">24.12 - 7.01</p>
                    <p className="Date_count">14</p>
                    <p className="Date_text">дней</p>

                </div>

                <div className="React">
                    <button className="Look">Посмотреть тур</button> 
                    <button className="Like"></button>
                    
                </div>

            </div>
        </div>
    )
}

export default CardCustom2;