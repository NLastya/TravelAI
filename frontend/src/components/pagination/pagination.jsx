import { Pagination } from 'antd';
const itemRender = (_, type, originalElement) => {
  if (type === 'prev') {
    return <a>Previous</a>;
  }
  if (type === 'next') {
    return <a>Next</a>;
  }
  return originalElement;
};
const PaginationCustom = ({total}, ...pros) => <Pagination total={total} itemRender={itemRender} showSizeChanger={false}/>;

export default PaginationCustom;
