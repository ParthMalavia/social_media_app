import  {BrowserRouter, Route, Routes} from "react-router-dom";

import Navbar from "./components/Navbar";
import  {AuthProvider} from "./context/AuthContext"
import LogInPage from "./views/LogInPage";
import DashboardPage from "./views/DashboardPage";
import PrivateRoute from "./utils/PrivateRoute";
import RegisterPage from "./views/RegisterPage";
import HomePage from "./views/HomePage";

function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <Navbar/>
        <Routes>
          <Route path="/login" Component={LogInPage} />
          <Route path="/register" Component={RegisterPage} />
          <Route path="/dashboard" element={<PrivateRoute><DashboardPage /></PrivateRoute>} />
          <Route exact path="/" Component={HomePage} />
        </Routes>
      </AuthProvider>
    </BrowserRouter>
  );
}

export default App;
