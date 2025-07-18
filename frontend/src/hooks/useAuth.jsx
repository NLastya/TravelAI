import React, { createContext, useContext, useState } from 'react';

const initAuthContext = {

  isLogged: false,
  user_id: -1,
  user: {},
  login: () => {},
  logout: () => {},
  listFavorites: [],
  setFavorites: () => {},
};

export const AuthContext = createContext(initAuthContext);

// eslint-disable-next-line react/prop-types
export const AuthProvider = ({ children }) => {
  const [isLogged, setIsLogged] = useState(false);
  const [user_id, setUserId] = useState(-1);
  const [user, setUser] = useState();
  const [listFavorites, setFavorites] = useState()

  const login = () => {
    setIsLogged(true);
  };

  const logout = () => {
    setIsLogged(false);
  };

  return (
    <AuthContext.Provider value={{ isLogged, login, logout, user_id, setUserId, user, setUser, setFavorites,  listFavorites
      
    }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  return useContext(AuthContext);
};
