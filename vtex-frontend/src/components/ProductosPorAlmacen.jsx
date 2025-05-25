import { gql, useQuery } from '@apollo/client';

const GET_PRODUCTOS_POR_ALMACEN = gql`
  query {
    productosPorAlmacen {
      almacen
      productos
    }
  }
`;

export default function ProductosPorAlmacen() {
  const { loading, error, data } = useQuery(GET_PRODUCTOS_POR_ALMACEN);

  if (loading) return <p className="text-muted">Cargando...</p>;
  if (error) return <div className="alert alert-danger">Error: {error.message}</div>;

  return (
    <div className="container py-4">
      <h1 className="mb-4 text-primary">📦 Productos por Almacén</h1>

      {data.productosPorAlmacen.length === 0 ? (
        <p className="text-muted">No hay datos disponibles.</p>
      ) : (
        <div className="row">
          {data.productosPorAlmacen.map((item) => (
            <div key={item.almacen} className="col-md-6 mb-4">
              <div className="card shadow-sm">
                <div className="card-header fw-semibold">{item.almacen}</div>
                <ul className="list-group list-group-flush">
                  {item.productos.map((producto) => (
                    <li key={producto} className="list-group-item">
                      {producto}
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
