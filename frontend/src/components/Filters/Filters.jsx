/* eslint-disable react/prop-types */
import React from "react";
import style from "./filters.module.css";
import dayjs from "dayjs";
import { DatePicker } from "antd";
import { getGenerateTours } from "../../helpers/fetchRoute";
const { RangePicker } = DatePicker;

// fetchFunc? : any;
const Filters = ({ form, setForm, dataList, setListTour }, ...props) => {
  return (
    <div className={style.filters}>
      <div>
        <label className={style.inputLabel}>
          {" "}
          Город
          <input
            className={style.inputText}
            value={form?.location}
            placeholder="Москва"
            onChange={(e) =>
              setForm((prev) => ({ ...prev, location: e.target.value }))
            }
          />
        </label>

        {/* <label className={style.inputLabel}> Даты маршрута
                <input className={style.inputText} value={form?.date}
                onChange={(e) => setForm(prev => ({...prev, date: e.target.value}))}
                />
            </label> */}
        <label className={style.inputLabel}>
          {" "}
          Даты тура
          <RangePicker
            value={[dayjs(form?.data_start), dayjs(form?.data_end)]}
            format="YYYY-MM-DD"
            allowClear={false}
            onChange={(value) => {
              setForm((prev) => ({
                ...prev,
                data_start: value[0].format("YYYY-MM-DD"),
                data_end: value[1].format("YYYY-MM-DD"),
              }));
              console.log(value[0].format("DD-MM-YYYY"));
            }}
          />
        </label>
      </div>

      {props?.fetchFunc && (
        <button
          className="mint-btn"
          onClick={() => getGenerateTours(form, setListTour)}
        >
          <img src="/icons/plane.svg" alt="plane" />
          Найти туры
        </button>
      )}
    </div>
  );
};

export default Filters;
