// src/routers/Routing.jsx

import React from "react";
import { Routes, Route } from "react-router-dom";
import configRouting from "./configRouting";

const Routing = () => {
  return (
    <Routes>
      {configRouting.map((route, index) => (
        <Route key={index} path={route.path} element={<route.page />} />
      ))}
      <Route path="*" element={<div>404 Not Found</div>} />
    </Routes>
  );
};

export default Routing;
