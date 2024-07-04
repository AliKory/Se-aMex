import logo from "./logo.svg";
import "./App.css";
import Menu from "./layout/Navbar";
import Routing from "./routers/Routing";
import { BrowserRouter as Router } from "express";
import LayoutNavbar from "./layout/Navbar";

function App() {
  return (
    <Router>
      <LayoutNavbar />
      <Routing />
    </Router>
  );
}

export default App;
