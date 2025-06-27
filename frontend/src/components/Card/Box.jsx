import React from "react";
// import rectangle3 from "./rectangle-3.png";
import styles from "./Box.module.css";

const Box = ({ date, title, location, description }) => {
  return (
    <div className={styles.box}>
      <div className={styles.group}>
        <img className={styles.rectangle} alt="Rectangle" src={'/login-ava.jpg'} />
        
        <div className={styles.overlapGroup}>
          <div className={styles.date}>{date ?? '22.05 - 27.05'}</div>
          <div className={styles.textWrapper}>{title ?? 'Сибирь 1'}</div>
          
          <p className={styles.spanWrapper}>
            <span className={styles.span}>{location ?? 'Сибирь,'}</span>
          </p>
        </div>
        
        <p className={styles.description}>
          {description}
        </p>
      </div>
    </div>
  );
};

export default Box;


export const PlacesList = ({ placesData }) => {
  return (
    <div className={styles.placesList}>
      {placesData.map(([cityName, dates]) => (
        <div key={cityName} className={styles.cityContainer}>
          <h2 className={styles.cityTitle}>{cityName}</h2>
          <div className={styles.daysContainer}>
            {Object.entries(dates).map(([date, places]) => (
              <div key={date} className={styles.dayColumn}>
                <DayPlaces 
                  date={date}
                  places={places}
                  cityName={cityName}
                />
              </div>
            ))}
          </div>
        </div>
      ))}
    </div>
  );
};




export const DayPlaces = ({ date, places, cityName }) => {
  return (
    <div className={styles.dayPlaces}>
      <h3 className={styles.dayTitle}>{date}</h3>
      <div className={styles.placesGrid}>
        {places.map(([title, type], index) => (
          <Box
            key={`${date}-${index}`}
            date={date}
            title={title}
            location={cityName}
            description={type === "закрытое" ? "Крытое" : "Открытое"}
          />
        ))}
      </div>
    </div>
  );
};