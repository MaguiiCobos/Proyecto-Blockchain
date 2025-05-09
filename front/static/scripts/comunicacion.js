const votoData = {
    voto: "Candidato A",
    identidad: "hash_unico_de_usuario"
  };
  
  fetch("http://localhost:5000/emitir_voto", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(votoData)
  })
  .then(res => res.json())
  .then(data => {
    alert(data.mensaje);
  });
  