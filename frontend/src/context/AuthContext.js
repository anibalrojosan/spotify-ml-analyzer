import React, { createContext, useState } from 'react';
import client from '../api/axiosClient';

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
    
    // Lazy initialization: this functions runs before the first renderization
    // It checks if 'spotify_user' and 'spotify_token' are already saved on localStorage
    const [user, setUser] = useState(() => {
        const storedUser = localStorage.getItem('spotify_user'); 
        return storedUser ? JSON.parse(storedUser) : null;
    });

    const [token, setToken] = useState(() => {
        return localStorage.getItem('spotify_token') || null;
    });
    // Since we read localStorage at the start, we don't need a 'loading' state.
    

    // Login function
    const login = async (archetypeId = null) => {
        try {
            const payload = archetypeId !== null ? { archetype_id: archetypeId } : {};
            const response = await client.post('auth/login/', payload);
            
            const { user, auth } = response.data;

            setUser(user);
            setToken(auth.access_token);

            localStorage.setItem('spotify_user', JSON.stringify(user));
            localStorage.setItem('spotify_token', auth.access_token);

            console.log("✅ Simulation Login Successful:", user.display_name);

        } catch (error) {
            console.error("❌ Login Failed:", error);
            alert("Login failed. Is the Django backend running?");
        }
    };


    // Logout function
    const logout = () => {
        setUser(null);
        setToken(null);
        localStorage.removeItem('spotify_user');
        localStorage.removeItem('spotify_token');
        console.log("👋 User Logged Out");
    };


    return (
        <AuthContext.Provider value={{ user, token, login, logout }}>
            {children}
        </AuthContext.Provider>
    );
};