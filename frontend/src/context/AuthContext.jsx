import React, { createContext, useContext, useState, useEffect } from 'react';
import { signupApi, loginApi, getMeApi } from '../services/api';

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [profile, setProfile] = useState(null);
  const [token, setToken] = useState(localStorage.getItem('careercampus_token') || null);
  const [loading, setLoading] = useState(true);

  // Restore session from token on initial load
  useEffect(() => {
    async function restoreSession() {
      if (token) {
        try {
          const data = await getMeApi();
          setUser(data.user);
          setProfile(data.profile);
        } catch (err) {
          console.error("Session restore failed:", err);
          logout();
        }
      }
      setLoading(false);
    }
    restoreSession();
  }, [token]);

  const login = async (email, password) => {
    const res = await loginApi({ email, password });
    localStorage.setItem('careercampus_token', res.access_token);
    setToken(res.access_token);
    setUser(res.user);
    setProfile(res.profile);
    return res;
  };

  const signup = async (userData) => {
    const res = await signupApi(userData);
    localStorage.setItem('careercampus_token', res.access_token);
    setToken(res.access_token);
    setUser(res.user);
    setProfile(res.profile);
    return res;
  };

  const logout = () => {
    localStorage.removeItem('careercampus_token');
    setToken(null);
    setUser(null);
    setProfile(null);
  };

  const updateLocalProfile = (newProfile) => {
    setProfile(newProfile);
  };

  return (
    <AuthContext.Provider value={{ user, profile, token, loading, login, signup, logout, updateLocalProfile }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}
