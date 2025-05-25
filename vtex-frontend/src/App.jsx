import { ApolloProvider } from '@apollo/client';
import { client } from './apolloClient';
import { BrowserRouter, Routes, Route, NavLink } from 'react-router-dom';
import ProductosPorAlmacen from './components/ProductosPorAlmacen';
import CiudadesPorProducto from './components/CiudadesPorProducto';
import AlmacenesPorCiudad from './components/AlmacenesPorCiudad';
import MovimientosGenerales from './components/MovimientosGenerales';
import Home from './components/Home';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.bundle.min.js';
import './custom.css'; // CSS personalizado

function App() {
  return (
    <ApolloProvider client={client}>
      <BrowserRouter>
        <nav className="navbar navbar-expand-lg navbar-light custom-navbar mb-4">
          <div className="container">
            <NavLink className="navbar-brand" to="/">VTEX Panel</NavLink>
            <button
              className="navbar-toggler"
              type="button"
              data-bs-toggle="collapse"
              data-bs-target="#navbarNav"
              aria-controls="navbarNav"
              aria-expanded="false"
              aria-label="Toggle navigation"
            >
              <span className="navbar-toggler-icon" />
            </button>

            <div className="collapse navbar-collapse" id="navbarNav">
              <ul className="navbar-nav ms-auto">
                <li className="nav-item">
                  <NavLink className="nav-link" to="/" end>Inicio</NavLink>
                </li>
                <li className="nav-item">
                  <NavLink className="nav-link" to="/productos-por-almacen">Productos por Almacén</NavLink>
                </li>
                <li className="nav-item">
                  <NavLink className="nav-link" to="/ciudades-por-producto">Ciudades por Producto</NavLink>
                </li>
                <li className="nav-item">
                  <NavLink className="nav-link" to="/almacenes-por-ciudad">Almacenes por Ciudad</NavLink>
                </li>
                <li className="nav-item">
                  <NavLink className="nav-link" to="/movimientos-generales">Movimientos Generales</NavLink>
                </li>
              </ul>
            </div>
          </div>
        </nav>

        <div className="container">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/productos-por-almacen" element={<ProductosPorAlmacen />} />
            <Route path="/ciudades-por-producto" element={<CiudadesPorProducto />} />
            <Route path="/almacenes-por-ciudad" element={<AlmacenesPorCiudad />} />
            <Route path="/movimientos-generales" element={<MovimientosGenerales />} />
          </Routes>
        </div>
      </BrowserRouter>
    </ApolloProvider>
  );
}

export default App;
