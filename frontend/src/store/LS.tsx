class LocalStorageHelper {
    get(key) {
      const value = localStorage.getItem(key);
      try {
        return JSON.parse(value);
      } catch (error) {
        return value;
      }
    }

    set(key, value) {
      const data = (typeof value === "object") ? JSON.stringify(value) : value;
      localStorage.setItem(key, data);
    }
  
    delete(key) {
      localStorage.removeItem(key);
    }
  }

const LS = new LocalStorageHelper()
  
export default LS;