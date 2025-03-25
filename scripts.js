// Lógica para Finanzas y Costos
document.getElementById('finanzasForm').addEventListener('submit', function (e) {
    e.preventDefault();
    const ingresos = parseFloat(document.getElementById('ingresos').value);
    const gastos = parseFloat(document.getElementById('gastos').value);
    const balance = ingresos - gastos;
    document.getElementById('balance').textContent = balance.toFixed(2);
});

// Lógica para Registro y Análisis de Costos
document.getElementById('costosForm').addEventListener('submit', function (e) {
    e.preventDefault();
    const costo = document.getElementById('costo').value;
    const descripcion = document.getElementById('descripcion').value;
    const listaCostos = document.getElementById('lista-costos');
    const nuevoCosto = document.createElement('li');
    nuevoCosto.innerHTML = `<span>${descripcion}:</span> $${costo}`;
    listaCostos.appendChild(nuevoCosto);
    document.getElementById('costosForm').reset();
});

// Lógica para Solicitud de Compra de Alimentos
document.getElementById('compraForm').addEventListener('submit', function (e) {
    e.preventDefault();
    const alimento = document.getElementById('alimento').value;
    const cantidad = document.getElementById('cantidad').value;
    const proveedor = document.getElementById('proveedor').value;
    const listaSolicitudes = document.getElementById('lista-solicitudes');
    const nuevaSolicitud = document.createElement('li');
    nuevaSolicitud.innerHTML = `<span>${alimento}:</span> ${cantidad} unidades (Proveedor: ${proveedor})`;
    listaSolicitudes.appendChild(nuevaSolicitud);
    document.getElementById('compraForm').reset();
});

// Lógica para Ventas y Compras
document.getElementById('ventasForm').addEventListener('submit', function (e) {
    e.preventDefault();
    const tipo = document.getElementById('tipo').value;
    const cantidad = document.getElementById('cantidad').value;
    const precio = document.getElementById('precio').value;
    const listaTransacciones = document.getElementById('lista-transacciones');
    const nuevaTransaccion = document.createElement('li');
    nuevaTransaccion.innerHTML = `<span>${tipo}:</span> ${cantidad} unidades a $${precio} cada una`;
    listaTransacciones.appendChild(nuevaTransaccion);
    document.getElementById('ventasForm').reset();
});