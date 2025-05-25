import { gql, useLazyQuery, useQuery } from '@apollo/client';
import { useState } from 'react';

const GET_ALMACENES_POR_CIUDAD = gql`
  query ($ciudad: String!) {
    almacenesPorCiudad(ciudad: $ciudad)
  }
`;

const GET_CIUDADES = gql`
  query {
    todasLasCiudades
  }
`;

export default function AlmacenesPorCiudad() {
  const [ciudad, setCiudad] = useState('');
  const [getAlmacenes, { loading: loadingAlmacenes, data: dataAlmacenes, error: errorAlmacenes }] =
    useLazyQuery(GET_ALMACENES_POR_CIUDAD);

  const { data: dataCiudades, loading: loadingCiudades, error: errorCiudades } = useQuery(GET_CIUDADES);

  const handleSearch = () => {
    if (ciudad) {
      getAlmacenes({ variables: { ciudad } });
    }
  };

  return (
    <div className="container py-5 d-flex justify-content-center">
      <div className="card shadow-sm" style={{ maxWidth: 700, width: '100%' }}>
        <div className="card-header bg-primary text-white">
          <h3 className="mb-1">🏬 Almacenes por Ciudad</h3>
          <small className="opacity-75">Consulta los almacenes disponibles en una ciudad específica</small>
        </div>

        <div className="card-body">
          {loadingCiudades && (
            <div className="alert alert-info py-2 mb-4" role="alert">
              Cargando lista de ciudades...
            </div>
          )}

          {errorCiudades && (
            <div className="alert alert-danger py-2 mb-4" role="alert">
              Error al cargar ciudades: {errorCiudades.message}
            </div>
          )}

          {!loadingCiudades && dataCiudades && (
            <form
              onSubmit={(e) => {
                e.preventDefault();
                handleSearch();
              }}
              className="row g-3 align-items-center mb-4"
            >
              <div className="col-md-9">
                <label htmlFor="ciudadSelect" className="form-label fw-semibold mb-2">
                  Selecciona una Ciudad
                </label>
                <select
                  id="ciudadSelect"
                  className="form-select"
                  value={ciudad}
                  onChange={(e) => setCiudad(e.target.value)}
                  aria-label="Seleccionar ciudad"
                >
                  <option value="">-- Elige una ciudad --</option>
                  {dataCiudades.todasLasCiudades.map((ciudadItem) => (
                    <option key={ciudadItem} value={ciudadItem}>
                      {ciudadItem}
                    </option>
                  ))}
                </select>
              </div>
              <div className="col-md-3 d-flex align-items-center">
                <button type="submit" className="btn btn-primary w-100" disabled={!ciudad}>
                  Buscar
                </button>
              </div>
            </form>
          )}

          {loadingAlmacenes && (
            <div className="text-center text-muted my-4">
              <div className="spinner-border text-primary" role="status" aria-hidden="true" />
              <div className="mt-2">Cargando almacenes...</div>
            </div>
          )}

          {errorAlmacenes && (
            <div className="alert alert-danger py-2 my-4" role="alert">
              Error: {errorAlmacenes.message}
            </div>
          )}

          {dataAlmacenes && dataAlmacenes.almacenesPorCiudad.length > 0 && (
            <>
              <h5 className="mb-3">Almacenes disponibles en {ciudad}:</h5>
              <ul className="list-group list-group-flush rounded shadow-sm">
                {dataAlmacenes.almacenesPorCiudad.map((almacen) => (
                  <li key={almacen} className="list-group-item py-3">
                    {almacen}
                  </li>
                ))}
              </ul>
            </>
          )}

          {dataAlmacenes && dataAlmacenes.almacenesPorCiudad.length === 0 && (
            <div className="alert alert-warning my-4" role="alert">
              No se encontraron almacenes para la ciudad seleccionada.
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
