import { gql, useLazyQuery } from '@apollo/client';
import { useState } from 'react';

const GET_MOVIMIENTOS_GENERALES = gql`
  query($desde: String!, $hasta: String!) {
    movimientosGenerales(desde: $desde, hasta: $hasta) {
      producto
      almacen
      ciudadDestino
      fecha
    }
  }
`;

export default function MovimientosGenerales() {
  const [desde, setDesde] = useState('');
  const [hasta, setHasta] = useState('');
  const [getMovimientos, { loading, data, error }] = useLazyQuery(GET_MOVIMIENTOS_GENERALES);

  const handleSearch = (e) => {
    e.preventDefault();
    if (desde && hasta) {
      getMovimientos({ variables: { desde, hasta } });
    }
  };

  return (
    <div className="container py-5 d-flex justify-content-center">
      <div className="card shadow-sm" style={{ maxWidth: 700, width: '100%' }}>
        <div className="card-header bg-primary text-white">
          <h3 className="mb-1">📦 Movimientos Generales</h3>
          <small className="opacity-75">Consulta movimientos por rango de fechas</small>
        </div>

        <div className="card-body">
          <form onSubmit={handleSearch} className="row g-3 align-items-end mb-4">
            <div className="col-md-5">
              <label htmlFor="fechaDesde" className="form-label fw-semibold">
                Desde
              </label>
              <input
                type="date"
                id="fechaDesde"
                className="form-control"
                value={desde}
                onChange={(e) => setDesde(e.target.value)}
                max={hasta || undefined}
                required
              />
            </div>
            <div className="col-md-5">
              <label htmlFor="fechaHasta" className="form-label fw-semibold">
                Hasta
              </label>
              <input
                type="date"
                id="fechaHasta"
                className="form-control"
                value={hasta}
                onChange={(e) => setHasta(e.target.value)}
                min={desde || undefined}
                required
              />
            </div>
            <div className="col-md-2 d-grid">
              <button type="submit" className="btn btn-primary" disabled={!desde || !hasta}>
                Buscar
              </button>
            </div>
          </form>

          {loading && (
            <div className="text-center text-muted my-4">
              <div className="spinner-border text-primary" role="status" aria-hidden="true" />
              <div className="mt-2">Cargando movimientos...</div>
            </div>
          )}

          {error && (
            <div className="alert alert-danger py-2 my-4" role="alert">
              Error: {error.message}
            </div>
          )}

          {data && data.movimientosGenerales.length === 0 && (
            <div className="alert alert-warning my-4" role="alert">
              No se encontraron movimientos en el rango seleccionado.
            </div>
          )}

          {data && data.movimientosGenerales.length > 0 && (
            <ul className="list-group list-group-flush rounded shadow-sm">
              {data.movimientosGenerales.map((m, idx) => (
                <li key={idx} className="list-group-item py-3">
                  <strong>Producto:</strong> {m.producto} <br />
                  <strong>Almacén:</strong> {m.almacen} <br />
                  <strong>Ciudad destino:</strong> {m.ciudadDestino} <br />
                  <strong>Fecha:</strong> {m.fecha}
                </li>
              ))}
            </ul>
          )}
        </div>
      </div>
    </div>
  );
}
