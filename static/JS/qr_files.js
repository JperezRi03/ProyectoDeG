document.addEventListener('DOMContentLoaded', function() {
    const video = document.getElementById('qr-video');
    const canvasElement = document.createElement('canvas');
    const canvas = canvasElement.getContext('2d', { willReadFrequently: true }); // Se agrega el atributo aquí

    document.getElementById('btn-scan-qr').addEventListener('click', function() {
        navigator.mediaDevices.getUserMedia({ video: { facingMode: "environment" } })
            .then(function(stream) {
                video.srcObject = stream;
                video.setAttribute("playsinline", true); // required to tell iOS safari we don't want fullscreen
                video.style.display = 'block'; // Asegúrate de que el video se muestre
                video.play();
                requestAnimationFrame(scanQRCode);
            })
            .catch(function(err) {
                console.error(err);
                alert('Error al acceder a la cámara: ' + err);
            });
    });

    function scanQRCode() {
        if (video.readyState === video.HAVE_ENOUGH_DATA) {
            canvasElement.height = video.videoHeight;
            canvasElement.width = video.videoWidth;
            canvas.drawImage(video, 0, 0, canvasElement.width, canvasElement.height);
            var imageData = canvas.getImageData(0, 0, canvasElement.width, canvasElement.height);
            var code = jsQR(imageData.data, imageData.width, imageData.height, {
                inversionAttempts: "dontInvert",
            });
    
            if (code) {
                console.log("Found QR code", code.data);
                video.srcObject.getTracks().forEach(track => track.stop());
                video.style.display = 'none'; // Oculta el video después de escanear
    
                // Extraer el hash_unico del URL
                const url = new URL(code.data);
                const hash_unico = url.pathname.split('/')[2]; // Asumiendo que la URL sigue el patrón dado
    
                // Hacer la solicitud al servidor usando fetch
                fetch(`/descargar_pdf/${hash_unico}`)
                    .then(response => {
                        if (!response.ok) {
                            throw new Error('Network response was not ok ' + response.statusText);
                        }
                        return response.json();
                    })
                    .then(data => {
                        if (data.error) {
                            alert('Error: ' + data.error);
                        } else {
                            alert('Éxito: ' + data.message + ' Descarga en: ' + code.data);
                        }
                    })
                    .catch(error => {
                        console.error('Error al procesar la solicitud:', error);
                        alert('Este QR ya ha sido utilizado.');
                    });
            } else {
                requestAnimationFrame(scanQRCode);
            }
        } else {
            requestAnimationFrame(scanQRCode);
        }
    }
    
    
});
