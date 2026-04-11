# BlockGuard Full-Stack Architecture Replacement

## What was built
I completely decoupled the codebase from Streamlit and upgraded it into an enterprise-ready full-stack architecture, providing a significantly better user aesthetic and scalability for the application.

### 1. The Core AI Backend (Flask)
I extracted the entire ML prediction pipeline (Opcodes extraction, LSTM networks, Random Forest heuristic routers, and SHAP Explainability) into an invisible backend API built with `Flask`.

- **File**: `backend/app.py`
- **Functionality**: Replaces Streamlit by listening for `POST /api/analyze` requests.
- **Processing**: Reads the dragged-and-dropped file contents directly from the web client, executes the models, and responds with a fast, structured JSON payload summarizing logic risks and SHAP insights.

### 2. The Interactive UI (React / Native Javascript)
I built a fully responsive Single Page Application (SPA) utilizing `Vite`, `React`, and `TailwindCSS`. 

- **File**: `frontend/src/App.jsx`
- **Functionality**: Connects to the Flask server asynchronously using Axios.
- **Highlights**:
  - 🌟 **Drag and Drop Uploader**: A massive, beautifully animated glassmorphic dropzone explicitly configured to accept raw `.sol`, `.bin`, `.txt`, and `.hex` files. When `.sol` files are explicitly detected, the backend dynamically intercepts the logic and boots up `py-solc-x` locally to compile and extract the runtime-bytecode automatically!
  - 📊 **Dynamic Visualizations**: Replaced the previous basic Matplotlib images with interactive `Recharts` graphs. Users can hover directly over the Opcode metrics and SHAP feature importance charts to see specific impact values.
  - 🎨 **Glassmorphism Theme**: Uses Tailwind's `backdrop-blur` and transparency tokens to implement an unparalleled state-of-the-art hacker-aesthetic layout requested.

## Verification Instructions
The system is now powered by two autonomous services. To launch it locally, you just need two terminal windows:

**Terminal 1 (Flask Intelligence Engine)**:
```bash
cd backend
../venv/bin/python app.py
```

**Terminal 2 (React Frontend Server)**:
```bash
cd frontend
npm run dev
```

> [!TIP]  
> After booting Terminal 2, you can click `http://localhost:5173` to view the stunning new application. Grab any compiled `.bin` hex file, drag it natively onto the browser window, and watch the API spin up the beautiful new visualization dashboards in real-time!
