// document.addEventListener("DOMContentLoaded", () => {
//     const dniInput = document.getElementById("dni");
//     const btnDni = document.getElementById("btn_dni");

    // dniInput.addEventListener("input", async () => {
    //     const dni = dniInput.value;

    //     // Verifica si el DNI tiene 8 caracteres
    //     if (dni.length === 8) {
    //         try {
    //             // Simula una consulta a la base de datos
    //             const response = await fetch(`/api/verificar_dni?dni=${dni}`);
    //             const data = await response.json();

    //             if (data.existe) {
    //                 // Cambia el borde a verde si el DNI existe
    //                 dniInput.style.border = "2px solid green";
    //                 btnDni.classList.remove("disabled");
    //                 btnDni.removeAttribute("disabled");
    //             } else {
    //                 // Cambia el borde a rojo si el DNI no existe
    //                 dniInput.style.border = "2px solid red";
    //                 btnDni.classList.add("disabled");
    //                 btnDni.setAttribute("disabled", "true");
    //             }
    //         } catch (error) {
    //             console.error("Error al verificar el DNI:", error);
    //             dniInput.style.border = "2px solid red"; // Marca en rojo en caso de error
    //             btnDni.classList.add("disabled");
    //             btnDni.setAttribute("disabled", "true");
    //         }
    //     } else {
    //         // Restablece el estilo si el DNI no tiene 8 caracteres
    //         dniInput.style.border = "1px solid #ccc";
    //         btnDni.classList.add("disabled");
    //         btnDni.setAttribute("disabled", "true");
    //     }
    // });

    // btnDni.addEventListener('click', function() {
    //     const dni = dniInput.value;

    //     fetch('http://localhost:5000/verificar_dni', {
    //         method: 'POST',
    //         headers: {
    //             'Content-Type': 'application/json'
    //         },
    //         body: JSON.stringify({ dni: dni })
    //     })
    //     .then(response => response.json())
    //     .then(data => {
    //         const resultado = document.getElementById('resultado');
    //         if (data.encontrado) {
    //             resultado.textContent = "✅ DNI encontrado.";
    //             // Aquí podés hacer otras acciones si se encontró
    //         } else {
    //             resultado.textContent = "❌ DNI no encontrado.";
    //             // Aquí podés hacer otras acciones si NO se encontró
    //         }
    //     })
    //     .catch(error => {
    //         console.error('Error:', error);
    //     });
    // });

    // const testButton = document.createElement("button");
    // testButton.textContent = "Probar conexión";
    // testButton.style.marginTop = "40px";
    // document.body.appendChild(testButton);

    // const resultadoConexion = document.createElement("p");
    // resultadoConexion.id = "resultadoConexion";
    // document.body.appendChild(resultadoConexion);

    // testButton.addEventListener("click", async () => {
    //     try {
    //         const response = await fetch("http://localhost:5000/test_conexion");
    //         const data = await response.json();

    //         if (data.conexion) {
    //             resultadoConexion.textContent = "✅ " + data.mensaje;
    //             resultadoConexion.style.color = "green";
    //         } else {
    //             resultadoConexion.textContent = "❌ " + data.mensaje;
    //             resultadoConexion.style.color = "red";
    //         }
    //     } catch (error) {
    //         resultadoConexion.textContent = "❌ Error al conectar con el servidor.";
    //         resultadoConexion.style.color = "red";
    //         console.error("Error:", error);
    //     }
    // });
// });