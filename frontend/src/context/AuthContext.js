import React, { useState, useEffect, createContext } from "react";
import { useNavigate } from "react-router-dom";
import { jwtDecode } from "jwt-decode"
import { AUTHTOKENS, BASE_URL } from "../utils/enums";

const AuthContext = createContext();

export default AuthContext;

export const AuthProvider = ({ children }) => {
    const navigate = useNavigate();
    const [loading, setLoading] = useState(true);

    const [user, setUser] = useState(() => 
        localStorage.getItem(AUTHTOKENS)
            ? jwtDecode(JSON.parse(localStorage.getItem(AUTHTOKENS)).access)
            : null
    );

    const [authTokens, setAuthTokens] = useState(() => 
        localStorage.getItem(AUTHTOKENS)
            ? JSON.parse(localStorage.getItem(AUTHTOKENS))
            : null
    );

    const loginUser = async (username, password) => {
        const response = await fetch(`${BASE_URL}/token/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ username, password })
        });

        const data = await response.json();

        if (response.status === 200) {
            setAuthTokens(data)
            setUser(jwtDecode(data.access))

            localStorage.setItem(AUTHTOKENS, JSON.stringify(data))
            navigate("/")
        } else {
            console.log("loginUser >> ERROR", response.status)
        }
    };

    const registerUser = async (full_name, email, username, password, password2) => {
        const response = await fetch(`${BASE_URL}/register/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ full_name, email, username, password, password2 })
        });

        if (response.status === 201) {
            navigate("/login")
        } else {
            console.log("registerUser >> ERROR", response.json())
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
