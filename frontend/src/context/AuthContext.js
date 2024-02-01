import React, { useState, createContext, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import {jwtDecode } from "jwt-decode"
import { AUTHTOKENS } from "../utils/enums";

const AuthContext = createContext();

export default AuthContext;

export const AuthProvider = ({ children }) => {
    const [authTokens, setAuthTokens] = useState(() => 
        localStorage.getItem(AUTHTOKENS)
            ? JSON.parse(localStorage.getItem(AUTHTOKENS))
            : null
    );

    const [user, setUser] = useState(() => 
        localStorage.getItem(AUTHTOKENS)
            ? jwtDecode(JSON.parse(localStorage.getItem(AUTHTOKENS)).access)
            // ? jwtDecode(localStorage.getItem(AUTHTOKENS))
            : null
    );

    const navigate = useNavigate();

    const [loading, setLoading] = useState(true);

    const loginUser = async (username, password) => {
        const response = await fetch("http://127.0.0.1:8000/api/token/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ username, password })
        });

        const data = await response.json();
        console.log("loginUser >> data ::", data);

        if (response.status === 200) {
            setAuthTokens(data)
            setUser(jwtDecode(data.access))

            localStorage.setItem(AUTHTOKENS, JSON.stringify(data))
            navigate("/")
        } else {
            console.log("loginUser >> ERROR", response.status)
        }
    };

    const registerUser = async (email, username, password, password2) => {
        const response = await fetch("http://127.0.0.1:8000/api/register/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ email, username, password, password2 })
        });
        console.log("registerUser >> response ::", await response.json())

        if (response.status === 201) {
            navigate("/login")
        } else {
            console.log("registerUser >> ERROR", response.status)
        }
    };

    const logoutUser = () => {
        setAuthTokens(null)
        setUser(null)
        localStorage.removeItem(AUTHTOKENS)
        navigate("/login")
    };

    const ContextData = {
        user, setUser,
        authTokens, setAuthTokens,
        registerUser,
        loginUser,
        logoutUser,
        // loading, setLoading,

    }

    useEffect(() => {
        if (authTokens) {
            setUser(jwtDecode(authTokens.access))
        }
        setLoading(false)
    }, [authTokens, loading])

    return (
        <AuthContext.Provider value={ContextData}>
            {loading ? null : children}
        </AuthContext.Provider>
    )

}

