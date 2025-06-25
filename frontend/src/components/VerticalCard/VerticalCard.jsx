/* eslint-disable react/prop-types */
import React from "react";
import { Rate } from "antd";
import style from "./card.module.css";
import { useNavigate } from "react-router-dom";

const VerticalCard = ({ id }, ...props) => {
  const navigate = useNavigate();
  return (
    <div
      className={style.card}
      style={{ "margin-bottom": props?.marginBottom }}
    >
      <img src={props?.image ? props?.image : "/mock/pic1.jpg"} />
      <div className={style.bothInfoDate}>
        <div className={style.bothInfo}>
          <div className={style.listInfo}>
            <h3>{props?.name ? props?.name : "Сибирь Тур№1"}</h3>
            <p className={style.location}>
              <imf src="./location.svg" />
              {props?.location
                ? props?.location
                : "Сибирь, ул. Прохорова, 34755"}
            </p>
            <p>
              <Rate defaultValue={props?.rate ? props.rate : 5}></Rate>{" "}
              {props?.rate ? props?.rate : "5 звезд"}
            </p>

            <div className={style.infoRow}></div>
          </div>
          <div>
            <p>Даты посещения</p>
            <p className={style.date}>
              {props?.date ? props?.date : "26.01.25 - 30.01.25"}
            </p>
            <p>5 дней</p>
          </div>
        </div>
        <div className={style.buttons}>
          <button
            className={"mint-btn"}
            onClick={() =>{navigate("/tour/" + (id ?? "1"))}}
          >
            Посмотреть тур
          </button>
          <button className={"btn-like"}>
            <img src="./icons/like.svg" />
          </button>
        </div>
      </div>
    </div>
  );
};

export default VerticalCard;
