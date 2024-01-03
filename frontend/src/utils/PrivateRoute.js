
import React, {useContext} from "react";
import { Navigate } from "react-router-dom";
import AuthContext from "../context/AuthContext";

export default function PrivateRoute({children, ...rest}) {

    const {user} = useContext(AuthContext);
    return user ? children : <Navigate to="/login" replace />;
}

// export default function PrivateRoute({children, ...rest}) {

//     const {user} = useContext(AuthContext);
    
//     return <Route {...rest}>{!user ? <Navigate to="/login" replace /> : children}</Route>
// }
