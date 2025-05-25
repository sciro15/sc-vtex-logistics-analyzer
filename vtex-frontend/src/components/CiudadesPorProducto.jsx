import { gql, useLazyQuery, useQuery } from '@apollo/client';
import { useState } from 'react';

const GET_CIUDADES_POR_PRODUCTO = gql`
  query($nombre: String!) {
    ciudadesPorProducto(nombre: $nombre)
  }
`;

const GET_TODOS_LOS_PRODUCTOS = gql`
  query {
    todosLosProductos
  }
`;

export default function CiudadesPorProducto() {
  const [productId, setProductId] = useState('');
  const [getCiudades, { loading, data, error }] = useLazyQuery(GET_CIUDADES_POR_PRODUCTO);
  const { data: productosData, loading: loadingProductos, error: errorProductos } = useQuery(GET_TODOS_LOS_PRODUCTOS);

  const handleSearch = (e) => {
    e.preventDefault();
    if (productId) {
      getCiudades({ variables: { nombre: productId } });
    }
  };

  return (
    <div className="container py-5 d-flex justify-content-center">
      <div className="card shadow-sm" style={{ maxWidth: 700, width: '100%' }}>
        <div className="card-header bg-primary text-white">
          <h3 className="mb-1">🏙️ Ciudades por Producto</h3>
          <small className="opacity-75">Consulta destinos por producto para análisis logístico</small>
        </div>

        <div className="card-body">
          {loadingProductos && (
            <div className="alert alert-info py-2 mb-4" role="alert">
              Cargando lista de productos...
            </div>
          )}

          {errorProductos && (
            <div className="alert alert-danger py-2 mb-4" role="alert">
              Error al cargar productos: {errorProductos.message}
            </div>
          )}

          {!loadingProductos && productosData && (
            <form onSubmit={handleSearch} className="row g-3 align-items-center mb-4">
              <div className="col-md-9">
                <label htmlFor="productoSelect" className="form-label fw-semibold mb-2">
                  Selecciona un Producto
                </label>
                <select
                  id="productoSelect"
                  className="form-select"
                  value={productId}
                  onChange={(e) => setProductId(e.target.value)}
                  aria-label="Seleccionar producto"
                  required
                >
                  <option value="">-- Elige un producto --</option>
                  {productosData.todosLosProductos.map((producto) => (
                    <option key={producto} value={producto}>
                      {producto}
                    </option>
                  ))}
                </select>
              </div>
              <div className="col-md-3 d-flex align-items-center">
                <button type="submit" className="btn btn-primary w-100" disabled={!productId}>
                  Buscar
                </button>
              </div>
            </form>
          )}

          {loading && (
            <div className="text-center text-muted my-4">
              <div className="spinner-border text-primary" role="status" aria-hidden="true" />
              <div className="mt-2">Cargando ciudades...</div>
            </div>
          )}

          {error && (
            <div className="alert alert-danger py-2 my-4" role="alert">
              Error: {error.message}
            </div>
          )}

          {data && data.ciudadesPorProducto.length === 0 && (
            <div className="alert alert-warning my-4" role="alert">
              No se encontraron ciudades para el producto seleccionado.
            </div>
          )}

          {data && data.ciudadesPorProducto.length > 0 && (
            <>
              <h5 className="mb-3">Ciudades destino para el producto:</h5>
              <ul className="list-group list-group-flush rounded shadow-sm">
                {data.ciudadesPorProducto.map((ciudad) => (
                  <li key={ciudad} className="list-group-item py-3">
                    {ciudad}
                  </li>
                ))}
              </ul>
            </>
          )}
        </div>
      </div>
    </div>
  );
}
