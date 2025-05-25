export default function Home() {
  return (
    <div className="d-flex justify-content-center mt-5">
      <div className="card shadow p-4" style={{ maxWidth: '800px', width: '100%' }}>
        <div className="card-body">
          <h2 className="card-title text-primary mb-3">
            🏠 Panel de Visualización Logística VTEX
          </h2>
          <p className="card-text">
            Esta plataforma permite analizar y consultar información logística derivada del sistema de órdenes,
            facilitando la toma de decisiones operativas mediante herramientas visuales y consultas optimizadas
            a una base de datos estructurada.
          </p>

          <h5 className="mt-4 text-secondary">🛠 Funcionalidades principales:</h5>
          <ul className="list-group list-group-flush mb-3">
            <li className="list-group-item">
              📦 <strong>Productos por Almacén:</strong> visualiza qué productos han sido despachados desde cada centro logístico.
            </li>
            <li className="list-group-item">
              🏙️ <strong>Ciudades por Producto:</strong> consulta las ciudades destino de cada producto despachado.
            </li>
            <li className="list-group-item">
              🏬 <strong>Almacenes por Ciudad:</strong> identifica los centros de distribución que han operado en cada localidad.
            </li>
            <li className="list-group-item">
              📊 <strong>Movimientos Generales:</strong> analiza los flujos de productos por fecha, ciudad y almacén.
            </li>
          </ul>

          <p className="card-text mt-3">
            La aplicación está respaldada por una API GraphQL integrada con una base de datos relacional,
            lo que permite consultas dinámicas, eficientes y escalables.
          </p>
        </div>
      </div>
    </div>
  );
}
