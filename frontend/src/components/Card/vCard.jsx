import styles from './vcard.module.css';

const VCard = ({item}, ...props) => {
    // console.log('e:', name, location, rating)
    console.log('tem:', item)
    return (
        <div className={styles.out}>
            <img className={styles.img} src="/login-ava.jpg"/>
        <div className={styles.box}>
          <div className={styles.header}>
            {item?.name && <h3 className={styles.date}>{item?.name ?? '323'}</h3>}
            <p className={styles.location}>
                              <img src="/icons/location.svg" />
                              <span>{ "Сибирь, ул. Прохорова, 34755"}</span>
                            </p>
          </div>
          <div className={styles.footer}>
            <button className={styles.btn + " mint-btn"}>Посмотреть место</button>
            <span className={styles.description}>{item?.description ?? 'Красиове место для отыха всей семьей'}</span>
          </div>
        </div>
        </div>);};
export default VCard;

export const ListvCards = ({arr}) => {
    console.log('arr:', arr)
    return(<div className={styles.list}>
        {arr.map((key, item) => <VCard item={key} key={item}/>
    )}
    </div>)
}

export const FullCards = ({arr}) => {
    const groupedByDate = arr.reduce((acc, item) => {
        const key = item.date;
        if (!acc[key]) {
          acc[key] = [];
        }
        acc[key].push(item);
        return acc;
      }, {});
      console.log('gr:', groupedByDate)

    return(
        <>
        <div className={styles.full}>
            {Object.entries(groupedByDate).map(([date, items]) => (
                <div className={styles.y}>
                <h4>{date}</h4>
        <ListvCards key={date} arr={items} />
        </div>
      ))}
        </div>
        </>
    )
}