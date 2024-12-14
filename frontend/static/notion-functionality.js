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

function create_project_list(data) {
    data.forEach((item, index) => {
        if (item.tipo === 'proyecto') {
            let projectExists = Proyectos.some(proj => proj.nombre === item.nombre_proyecto);
            if (!projectExists) {
                let projectId = `Project-${Proyectos.length}`;
                let projectName = item.nombre_proyecto || `${projectId} Proyecto sin nombre`;
                let newProject = new Proyecto(projectId, projectName, item.resumen, item.fecha_inicio, item.fecha_fin);
                Proyectos.push(newProject);
            }
        }
    });

    data.forEach((item) => {
        if (item.tipo === 'tarea') {
            let project = Proyectos.find(proj => proj.nombre === item.nombre_proyecto) || Proyectos[0];
            let taskId = `${project.id}-Task-${project.tareas.length}`;
            let newTask = new Tarea(taskId, item.nombre_tarea, item.nombre_proyecto, item.nombre_persona, item.fecha_inicio, item.fecha_fin, item.prioridad, item.estado);
            project.tareas.push(newTask);

            let personas = item.nombre_persona.split(' y ');
            personas.forEach(persona => {
                if (!project.personas.includes(persona)) {
                    project.personas.push(persona);
                } else if (!Proyectos[0].personas.includes(persona)) {
                    Proyectos[0].personas.push(persona);
                }
            });
        }
    });
}
function show_project_tasks(project_id) {
    let project_detail = document.querySelector('.project-detail');
    project_detail.innerHTML = '';

    let header = document.createElement('h1');
    header.textContent = 'Datos Incompletos';
    project_detail.appendChild(header);

    let incompleteDataList = document.createElement('ul');
    incompleteDataList.classList.add('incomplete-data-list');

    Datos_incompletos.forEach(data => {
        let listItem = document.createElement('li');
        listItem.classList.add('incomplete-data-item');

        if (data.tipo === 'tarea') {
            listItem.innerHTML = `
                <strong>Tarea:</strong> ${data.nombre_tarea} <br>
                <strong>Persona:</strong> ${data.nombre_persona} <br>
                <strong>Fecha Inicio:</strong> ${data.fecha_inicio} <br>
                <strong>Fecha Fin:</strong> ${data.fecha_fin} <br>
                <strong>Prioridad:</strong> ${data.prioridad} <br>
                <strong>Resumen:</strong> ${data.resumen}
            `;
        } else if (data.tipo === 'proyecto') {
            listItem.innerHTML = `
                <strong>Proyecto:</strong> ${data.nombre_proyecto || 'Sin nombre'} <br>
                <strong>Estado:</strong> ${data.estado} <br>
                <strong>Fecha Inicio:</strong> ${data.fecha_inicio} <br>
                <strong>Fecha Fin:</strong> ${data.fecha_fin} <br>
                <strong>Prioridad:</strong> ${data.prioridad} <br>
                <strong>Resumen:</strong> ${data.resumen}
            `;
        }

        incompleteDataList.appendChild(listItem);
    });

    if (Datos_incompletos.length === 0) {
        incompleteDataList.innerHTML = '<li>No hay datos incompletos.</li>';
    }

    project_detail.appendChild(incompleteDataList);
}

function show_project_blocks() {
    
    Proyectos.forEach((project, index) => {
        let template = document.getElementById('tem-project-list-item');
        let projectItem = template.content.cloneNode(true);
        let projectBlock = projectItem.querySelector('.project-list__item');
        projectBlock.id = project.id;
        projectBlock.querySelector('.project-name').textContent = project.nombre;
        projectBlock.classList.add(get_random_gradient());
        // projectBlock.querySelector('.project-summary').textContent = item.resumen;
        // projectBlock.querySelector('.project-dates').textContent = `${item.fecha_inicio} - ${item.fecha_fin}`;
        document.querySelector('.project-list').appendChild(projectItem);
    });
    
    document.querySelector('.project-count').textContent = `(${Proyectos.length})`;

}

function stop_it(event) {
    event.preventDefault();
}

function edit_task(task_id) {
    let task = document.getElementById(task_id);
    let taskData = Proyectos.flatMap(proj => proj.tareas).find(tarea => tarea.id === task_id);

    let popupContent = `
        <div class="popup-content">
            <label>Nombre: <input type="text" id="edit-task-name" value="${taskData.nombre}"></label>
            <label>Persona: 
                <select id="edit-task-persona">
                    ${Personas.map(persona => `<option value="${persona}" ${taskData.persona.includes(persona) ? 'selected' : ''}>${persona}</option>`).join('')}
                </select>
                <button class="icon" id="edit-persona-btn"><img class="icon" src="static/edit.png" alt="edit"></button>
            </label>
            <label>Proyecto: 
                <select id="edit-task-proyecto">
                    ${Proyectos.map(proj => `<option value="${proj.id}" ${proj.id === taskData.id.split('-')[0] ? 'selected' : ''}>${proj.nombre}</option>`).join('')}
                </select>
                <button class="icon" id="edit-proyecto-btn"><img class="icon" src="static/edit.png" alt="edit"></button>
            </label>
            <label>Fecha Inicio: <input type="date" id="edit-task-inicio" value="${taskData.inicio}"></label>
            <label>Fecha Fin: <input type="date" id="edit-task-fin" value="${taskData.termino}"></label>
            <label>Prioridad: 
                <select id="edit-task-prioridad">
                    <option value="alta" ${taskData.prioridad === 'alta' ? 'selected' : ''}>Alta</option>
                    <option value="media" ${taskData.prioridad === 'media' ? 'selected' : ''}>Media</option>
                    <option value="baja" ${taskData.prioridad === 'baja' ? 'selected' : ''}>Baja</option>
                </select>
            </label>
            <label>Estado: 
                <select id="edit-task-estado">
                    <option value="pendiente" ${taskData.estado === 'pendiente' ? 'selected' : ''}>Pendiente</option>
                    <option value="completado" ${taskData.estado === 'completado' ? 'selected' : ''}>Completado</option>
                </select>
            </label>
            <button id="save-task-btn">Guardar</button>
            <button id="delete-task-btn">Eliminar</button>
            <button id="cancel-task-btn">Cancelar</button>
        </div>
    `;

    let popup = new Popup({
        content: popupContent, 
        width: '400px',
        height: 'auto',
        title: 'Editar tarea',
        fontSizeMultiplier: 0.8
    });

    popup.show();

    document.getElementById('edit-persona-btn').addEventListener('click', () => {
        let personaInput = document.createElement('input');
        personaInput.type = 'text';
        personaInput.id = 'edit-task-persona';
        document.querySelector('#edit-task-persona').replaceWith(personaInput);
    });

    document.getElementById('edit-proyecto-btn').addEventListener('click', () => {
        let proyectoInput = document.createElement('input');
        proyectoInput.type = 'text';
        proyectoInput.id = 'edit-task-proyecto';
        document.querySelector('#edit-task-proyecto').replaceWith(proyectoInput);
    });

    document.getElementById('save-task-btn').addEventListener('click', () => {
        let newName = document.getElementById('edit-task-name').value;
        let newPersona = document.getElementById('edit-task-persona').value;
        let newProyecto = document.getElementById('edit-task-proyecto').value;
        let newInicio = document.getElementById('edit-task-inicio').value;
        let newFin = document.getElementById('edit-task-fin').value;
        let newPrioridad = document.getElementById('edit-task-prioridad').value;
        let newEstado = document.getElementById('edit-task-estado').value;

        let currentProject = Proyectos.find(proj => proj.id === taskData.id.split('-')[0]);
        let newProject = Proyectos.find(proj => proj.id === newProyecto) || new Proyecto(`Project-${Proyectos.length}`, newProyecto, '', newInicio, newFin);

        if (!Proyectos.includes(newProject)) {
            Proyectos.push(newProject);
        }

        currentProject.tareas = currentProject.tareas.filter(tarea => tarea.id !== task_id);
        newProject.tareas.push(new Tarea(task_id, newName, newPersona, newInicio, newFin, newPrioridad, newEstado));

        popup.hide();
        show_project_tasks(active_project_id);
    });

    document.getElementById('delete-task-btn').addEventListener('click', () => {
        if (confirm('¿Estás seguro de que deseas eliminar esta tarea?')) {
            let currentProject = Proyectos.find(proj => proj.id === taskData.id.split('-')[0]);
            currentProject.tareas = currentProject.tareas.filter(tarea => tarea.id !== task_id);
            popup.hide();
            show_project_tasks(active_project_id);
        }
    });

    document.getElementById('cancel-task-btn').addEventListener('click', () => {
        popup.hide();
    });
}


function save_task(current_caller, task_id) {
    var task = document.getElementById(task_id);
    var label = task.querySelector('.form-check-label');
    label.contentEditable = false;
    label.removeEventListener('click', stop_it);

    // Change this tag's value to editing text and it's class 'tag-info' to 'tag-success'
    current_caller.innerHTML = "Edit";
    current_caller.classList.remove('tag-success');
    current_caller.classList.add('tag-info');
    current_caller.onclick = function() { edit_task(current_caller, task_id); }
}


function add_task(section_id, taskNum) {
    var template = document.getElementById('task-item');
    var taskItem = template.content.cloneNode(true);
    var task = taskItem.querySelector('.task-list__item');
    var checkbox = task.querySelector('.form-check-input');
    var label = task.querySelector('.form-check-label');
    var editButton = task.querySelector('.tag');

    task.id = 'item_task' + taskNum;
    checkbox.id = 'task' + taskNum;
    checkbox.name = 'task' + taskNum;
    label.setAttribute('for', 'task' + taskNum);
    editButton.id = 'edit_task' + taskNum;
    editButton.setAttribute('onclick', `save_task(this, 'task${taskNum}')`);

    var taskList = document.querySelector(`#${section_id} ul.task-list`);
    taskList.appendChild(taskItem);
}

function get_random_id() {
    return Math.floor(Math.random() * 1000000);
}

function get_random_gradient() {
    let index = Math.floor(Math.random() * 5);
    let gradients = ['ripe-malinka', 'itmeo-branding', 'mixed-hopes', 'fly-high', 'fruit-blend'];
    return gradients[index];
}

function set_active(project_block) {
    let active_project = document.getElementById(active_project_id);
    active_project.classList.remove('active');
    project_block.classList.add('active');
    active_project_id = project_block.id;
    show_project_tasks(active_project_id);
}

function change_status(task_id) {
    var task = document.getElementById(task_id);
    var checkbox = task.querySelector('.form-check-input');
    var status = task.querySelector('.tag-status');

    if (checkbox.checked) {
        status.textContent = "completado";
        status.classList.remove('tag-info');
        status.classList.add('tag-success');
    } else {
        status.textContent = "pendiente";
        status.classList.remove('tag-success');
        status.classList.add('tag-info');
    }
}

function edit_task_details(task_id) {
    //TODO: Implementar la edición de tareas
}

document.addEventListener('DOMContentLoaded', function() {
    create_project_list(Datos_incompletos);
    show_project_blocks();
    set_active(document.getElementById(active_project_id));
    show_project_tasks(active_project_id);
});