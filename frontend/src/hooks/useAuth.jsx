import React, { createContext, useContext, useState } from 'react';

const initAuthContext = {

  isLogged: false,
  login: () => {},
  logout: () => {},
};

export const AuthContext = createContext(initAuthContext);

// eslint-disable-next-line react/prop-types
export const AuthProvider = ({ children }) => {
  const [isLogged, setIsLogged] = useState(false);

  const login = () => {
    setIsLogged(true);
  };

  const logout = () => {
    setIsLogged(false);
  };

  return (
    <AuthContext.Provider value={{ isLogged, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  return useContext(AuthContext);
};
