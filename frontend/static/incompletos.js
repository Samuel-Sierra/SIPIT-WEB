class Proyecto {
    constructor(id, nombre, resumen, fecha_inicio, fecha_fin) {
        this.id = id; // ID del proyecto, relacionada a su posición en el arreglo de proyectos
        this.nombre = nombre;
        this.resumen = resumen;
        this.fecha_inicio = fecha_inicio;
        this.fecha_fin = fecha_fin;
        this.prioridad;
        this.personas = [];
    }
}

class Tarea {
    constructor(id, nombre, proyecto, persona, inicio, termino, prioridad, estado) {
        this.id = id; // ID de la tarea, combinación de la ID del proyecto y la posición de la tarea en el arreglo de tareas
        this.nombre = nombre;
        this.proyecto = proyecto; // La ID del proyecto al que pertenecen
        this.persona = persona;
        this.inicio = inicio;
        this.termino = termino;
        this.prioridad = prioridad;
        this.estado = estado;
    }
}


active_project_id = "Project-0";

// Arreglo de proyectos, con el proyecto para guardar las tareas sin proyecto en la primer posición
const Proyectos = [
    new Proyecto("Project-0", "Tareas sin proyecto", "Proyecto para guardar tareas sin un nombre de proyecto", "2024-12-07", "2024-12-08")
];
Personas = [];

num_proyectos_sin_nombre = 0;

Datos_incompletos = [
    {
        "tipo": "tarea",
        "accion": "crear",
        "nombre_proyecto": "",
        "nombre_tarea": "Revisión y detalle de permisos de red",
        "nombre_persona": "Laura",
        "estado": "pendiente",
        "fecha_inicio": "2024-12-07",
        "fecha_fin": "2024-12-08",
        "prioridad": "alta",
        "resumen": "Revisar los permisos de red actuales y detallar lo que falta para coordinar con administración."
    },
    {
        "tipo": "tarea",
        "accion": "crear",
        "nombre_proyecto": "",
        "nombre_tarea": "Optimización de la base de datos",
        "nombre_persona": "María",
        "estado": "pendiente",
        "fecha_inicio": "2024-12-07",
        "fecha_fin": "2024-12-12",
        "prioridad": "media",
        "resumen": "Revisar y optimizar la base de datos para mejorar la velocidad."
    },
    {
        "tipo": "tarea",
        "accion": "crear",
        "nombre_proyecto": "",
        "nombre_tarea": "Añadir controles de seguridad a la base de datos",
        "nombre_persona": "Lucía y María",
        "estado": "pendiente",
        "fecha_inicio": "2024-12-07",
        "fecha_fin": "2024-12-12",
        "prioridad": "alta",
        "resumen": "Coordinación para revisar y añadir controles de seguridad en la base de datos."
    },
    {
        "tipo": "tarea",
        "accion": "crear",
        "nombre_proyecto": "",
        "nombre_tarea": "Informe sobre problemas de soporte en inicio de sesión",
        "nombre_persona": "María",
        "estado": "pendiente",
        "fecha_inicio": "2024-12-07",
        "fecha_fin": "2024-12-13",
        "prioridad": "media",
        "resumen": "Elaborar un informe detallado de problemas de inicio de sesión y coordinar con Andrea."
    },
    {
        "tipo": "tarea",
        "accion": "crear",
        "nombre_proyecto": "",
        "nombre_tarea": "Documentación de avances y coordinación con interfaz",
        "nombre_persona": "Miguel",
        "estado": "pendiente",
        "fecha_inicio": "2024-12-07",
        "fecha_fin": "2024-12-10",
        "prioridad": "media",
        "resumen": "Actualizar la documentación de avances y coordinar con Carlos para la parte visual de la interfaz."
    },
    {
        "tipo": "proyecto",
        "accion": "crear",
        "nombre_proyecto": "Módulo de Autenticación",
        "estado": "en progreso",
        "fecha_inicio": "2024-12-07",
        "fecha_fin": "2024-12-16",
        "prioridad": "alta",
        "resumen": "Desarrollo y revisión del módulo de autenticación con protocolos de seguridad actualizados."
    }
];

function show_project_tasks() {

    getCookie=()=>{
        let decode =decodeURIComponent(document.cookie)
        let arr = decode.split(";")
        let nombres = []
        for (let a in arr){
            let conjunto = arr[a].split("=")
            let nombre = conjunto.at(0)
            nombres.push(nombre)
        }
        return nombres
    }
    alert(getCookie());
    let project_detail = document.querySelector('.project-detail');
    project_detail.innerHTML = '';

    let header = document.createElement('h1');
    header.textContent = 'Datos Incompletos';
    project_detail.appendChild(header);


    Datos_incompletos.forEach(data => {


        const form = document.createElement('form');
        form.method = 'POST';
        form.action = `/incompletos/`

        for (let key in data ){
            const input = document.createElement('input');
            if (data[key] === ""){
                const label = document.createElement('label')
                label.textContent = `${key}:`;
                input.name = key;
                input.type = 'string';     
                form.append(label);               
            }else{
                input.type = 'hidden';
                input.name = key;
                input.value = data[key]; // Por ejemplo, el índice del dato.
            }
            form.appendChild(input)
        };
        const saveButton = document.createElement('button');
        saveButton.textContent = 'Guardar';
        saveButton.type = 'submit';
        form.appendChild(saveButton);
        project_detail.appendChild(form);
        
    });

    if (Datos_incompletos.length === 0) {
        project_detail.innerHTML = '<p>No hay datos incompletos.</p>';
    }

    
}
function deleteAllCookies() {
    document.cookie.split(';').forEach(cookie => {
        const eqPos = cookie.indexOf('=');
        const name = eqPos > -1 ? cookie.substring(0, eqPos) : cookie;
        document.cookie = name + '=;expires=Thu, 01 Jan 1970 00:00:00 GMT';
    });
}

document.addEventListener('DOMContentLoaded', function() {
    show_project_tasks();
    deleteAllCookies();
});