function footer_info() {
    Swal.fire({
        title: 'Información',
        text: 'Trabajo de titulación',
        imageUrl: 'http://ecuciencia.utc.edu.ec/static/home/img/logo-utc.png',
        /*imageUrl: 'http://3.bp.blogspot.com/-BHUW2cbor8Y/VJSgDcgvcFI/AAAAAAAAMuk/XGpNlwCVxu8/s1600/logotipo%2BUTC.jpg',
        */imageUrl: 'https://www.utc.edu.ec/Portals/0/BELEN/NUEVAimagen/universidad_def.png?ver=2019-05-08-101730-527',
        imageWidth: 'auto', /*400,200*/
        imageHeight: 'auto',
        imageAlt: 'Universidad Tecnica de Cotopaxi',
    })
}

function footer_info2() {
    Swal.fire({
        title: 'Información',
        text: 'Desarollado por: RAL/AMP',
        imageUrl: 'http://ecuciencia.utc.edu.ec/static/home/img/logo-utc.png',
        /*imageUrl: 'http://3.bp.blogspot.com/-BHUW2cbor8Y/VJSgDcgvcFI/AAAAAAAAMuk/XGpNlwCVxu8/s1600/logotipo%2BUTC.jpg',
        */imageUrl: 'https://www.utc.edu.ec/Portals/0/BELEN/NUEVAimagen/universidad_def.png?ver=2019-05-08-101730-527',
        imageWidth: 'auto', /*400,200*/
        imageHeight: 'auto',
        imageAlt: 'Universidad Tecnica de Cotopaxi',
    })
}

//notificaciones de paginas

function noti_sin_info() {
    Swal.fire(
        'Atención',
        'No se encuentra disponible esta información.',
        'info'
    )
}

function noti_misma_pagina() {
    Swal.fire(
        'Atención',
        'Se encuentra en la misma pagina.',
        'info'
    )
}

function noti_no_disponible() {
    Swal.fire(
        'No Disponible',
        'Esta función se la agregará en otra de las etapas del desarrollo.',
        'info'
    )
}
