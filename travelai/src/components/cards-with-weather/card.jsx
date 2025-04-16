import React from "react"
import IMG from "./image/img0.jpg"
import Pointer from './image/pointer_2.png'
import './card.css'
import Sun from "./image/sunny.png"



//type props = {start_date?:Date; end_date?:Date; title?: string; location?:string; desc?: string; img?: string }

function Card(props) {

    const start_date = props?.start_date ?? new Date(2024, 11, 24);
    const month1 = String(start_date.getMonth() + 1).padStart(2, '0'); 
    const day1 = String(start_date.getDate()).padStart(2, '0');
    const stars_date_str = `${month1}.${day1}`;

    const end_date = props?.end_date ?? new Date(2025, 0, 7);
    const month2 = String(end_date.getMonth() + 1).padStart(2, '0'); 
    const day2 = String(end_date.getDate()).padStart(2, '0');
    const end_date_str = `${month2}.${day2}`;

    const title = props?.title ?? "Красная Поляна";
    const location = props?.location ?? "Сибирь ул. Каменская";
    const desc = props?.desc ?? "Хорошее место для отдыха и генерации фантазии Chat GPT. Хвала Chat GPT.";

    const calcDate = () => {
        const differenceInTime = end_date.getTime() - start_date.getTime();
        const daysBetween = differenceInTime / (1000 * 3600 * 24);
        return Math.floor(daysBetween); 
    }

    const daysBetween = calcDate();

    return (
        <div className='fullCard'>
            <div className="date">
                <span>{stars_date_str}</span>
                <img src={Sun} alt="pic" />
            </div>

            <div className="divider">
                <div className="darkDivider"></div>
                <div className="lightDivider"></div>
            </div>

            <div className="Card">
                      
                <div className="Base_img">
                    <img src={props?.img ?? IMG} alt="Base_img" />
                </div>
                
                <div className="Information">
                    <h3 className='Name'>{title}</h3> 
    
                    <div className="Adress">
                        <img className="Pointer" src={Pointer}/>
                        <p className="Location_adress">{location}</p>
                    </div>
    
                    <p className="Description">{desc}</p>
                    <div className="Date">
                        
                        <p className="Date_text">даты вылета</p>

                        <div className="Duration">
                            <p className="Date_days">{stars_date_str}</p>
                            <p className="Date_days">-</p>
                            <p className="Date_days">{end_date_str}</p>
                        </div>

                        <div className="Count">
                            <p className="Date_count">{daysBetween}</p>
                            <p className="Date_text">дней</p>
                        </div>
                        
                    </div>
                   
                    <button className="Look">Посмотреть место</button> 
                
                </div> 
    
            </div>

        </div>

    )
}

export default Card