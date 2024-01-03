import React, { useContext } from 'react';
import AuthContext from '../context/AuthContext';

function HomePage() {
    const { user } = useContext(AuthContext)
    console.log("HOMEpage >> user ::", user.username)
    return (
        <div>
            HomePage
        </div>
    )
}

export default HomePage