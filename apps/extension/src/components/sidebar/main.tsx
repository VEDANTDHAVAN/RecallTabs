import React from "react";
import ReactDOM from "react-dom/client";

import Sidebar from "./Sidebar";

const container = document.createElement("div");

container.id = "recalltabs-root";

document.body.appendChild(container);

ReactDOM.createRoot(container).render(<Sidebar/>);