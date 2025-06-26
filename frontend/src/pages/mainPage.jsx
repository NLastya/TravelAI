import Footer from "../components/Footer/Footer"
import Header from "../components/Header"
import style from './searchpage.module.css'
import {getGenerateTours, getTourById, getActiveCityViews,getCityViewsAnalytics, getUserFavorites, getUserSurvey, startCityView, endCityView, addFavorite, removeFavorite} from '../helpers/fetchRoute'


const MainPage = () => {
    const allFethces = () => {
        // 1. Получение анкеты пользователя
console.log('=== 1. Получение анкеты пользователя ===');
getUserSurvey(
  0,
  (data) => console.log('Анкета пользователя:', data),
  (error) => console.error('Ошибка:', error)
);

// 2. Аналитика просмотров городов
console.log('\n=== 2.1. Начать отслеживание просмотра города ===');
const startTime = new Date().toISOString();
startCityView(
  0,
  'Москва',
  startTime,
  (data) => console.log('Начали отслеживание Москвы:', data),
  (error) => console.error('Ошибка:', error)
);

console.log('\n=== 2.2. Завершить отслеживание просмотра города ===');
const endTime = new Date().toISOString();
endCityView(
  0,
  'Москва',
  endTime,
  (data) => console.log('Завершили отслеживание Москвы:', data),
  (error) => console.error('Ошибка:', error)
);

console.log('\n=== 2.3. Получить аналитику просмотров ===');
getCityViewsAnalytics(
  0,
  (data) => {
    console.log('Городы просмотренные >2 мин:', data.moreThan2Min || []);
    console.log('Городы просмотренные <2 мин:', data.lessThan2Min || []);
  },
  (error) => console.error('Ошибка:', error)
);

console.log('\n=== 2.4. Активные просмотры городов ===');
getActiveCityViews(
  0,
  (data) => console.log('Сейчас просматривает:', data || []),
  (error) => console.error('Ошибка:', error)
);

// 3. Работа с избранным
console.log('\n=== 3.1. Добавить тур в избранное ===');
addFavorite(
  0,
  100,
  (data) => console.log('Успешно добавлен тур 100:', data),
  (error) => console.error('Ошибка:', error)
);

console.log('\n=== 3.2. Удалить тур из избранного ===');
removeFavorite(
  0,
  100,
  (data) => console.log('Успешно удален тур 100:', data),
  (error) => console.error('Ошибка:', error)
);

console.log('\n=== 3.3. Получить список избранного ===');
getUserFavorites(
  0,
  (data) => console.log('Список избранных туров:', data || []),
  (error) => console.error('Ошибка:', error)
);

// 4. Комплексный пример
console.log('\n=== 4. Комплексный пример использования ===');
console.log('Начинаем просмотр Парижа...');
startCityView(0, 'Париж', new Date().toISOString(), 
  (startData) => {
    console.log('Статус старта:', startData);
    
    setTimeout(() => {
      console.log('Завершаем просмотр Парижа через 3 сек...');
      endCityView(0, 'Париж', new Date().toISOString(),
        (endData) => {
          console.log('Статус завершения:', endData);
          
          console.log('Проверяем аналитику...');
          getCityViewsAnalytics(0,
            (analytics) => {
              console.log('Аналитика просмотров:');
              console.log('- Долгие просмотры:', analytics.moreThan2Min || []);
              console.log('- Короткие просмотры:', analytics.lessThan2Min || []);
              
              console.log('Добавляем тур 42 в избранное...');
              addFavorite(0, 42,
                (favData) => {
                  console.log('Результат добавления:', favData);
                  
                  console.log('Запрашиваем текущее избранное...');
                  getUserFavorites(0,
                    (favorites) => {
                      console.log('Текущее избранное:', favorites || []);
                      console.log('=== Все операции завершены ===');
                    },
                    (error) => console.error('Ошибка получения избранного:', error)
                  );
                },
                (error) => console.error('Ошибка добавления:', error)
              );
            },
            (error) => console.error('Ошибка аналитики:', error)
          );
        },
        (error) => console.error('Ошибка завершения:', error)
      );
    }, 3000);
  },
  (error) => console.error('Ошибка старта:', error)
);
    }

    allFethces();


    return(
    <>
    <Header/>
    <div className={style.main}>
            <p>Главная страница</p>
    </div>
    <Footer/>
    </>
)
}

export default MainPage;