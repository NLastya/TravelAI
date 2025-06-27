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


    return (
  <>
    <Header />
    <div className={style.main}>
      <div style={{
        display: 'flex',
        minHeight: 'calc(100vh - 160px)',
        backgroundColor: '#f6f8fa',
        fontFamily: 'Inter, sans-serif',
        padding: '60px',
        boxSizing: 'border-box'
      }}>
        <div style={{ flex: 1, display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
          <h1 style={{ fontSize: '48px', marginBottom: '20px' }}>Открой мир с нами</h1>
          <p style={{ fontSize: '18px', marginBottom: '40px', maxWidth: '500px' }}>
            Лучшие туристические предложения, составленные нейросетью специально для тебя. Получи персональные рекомендации и выбери тур мечты!
          </p>
          <div style={{ display: 'flex', gap: '16px', marginBottom: '24px', flexWrap: 'wrap' }}>
            <a href="/popularTours" style={{
              padding: '12px 24px',
              backgroundColor: '#90d7c6',
              borderRadius: '8px',
              textDecoration: 'none',
              color: '#000',
              fontWeight: 600
            }}>Популярные туры</a>
            <a href="/tours" style={{
              padding: '12px 24px',
              backgroundColor: '#90d7c6',
              borderRadius: '8px',
              textDecoration: 'none',
              color: '#000',
              fontWeight: 600
            }}>Рекомендации</a>
          </div>
          <a href="/auth-in" style={{
            marginTop: '20px',
            padding: '14px 28px',
            backgroundColor: '#0fa47f',
            color: 'white',
            borderRadius: '10px',
            textDecoration: 'none',
            fontWeight: 'bold',
            width: 'fit-content'
          }}>Начать</a>
        </div>
        <div style={{
          flex: 1,
          borderRadius: '24px',
          background: `url('/path/to/your/image.png') center/cover no-repeat`
        }} />
      </div>
    </div>
    <Footer />
  </>
);

}

export default MainPage;