class Proyecto {
    constructor(id, nombre, resumen, fecha_inicio, fecha_fin) {
        this.id = id; // ID del proyecto, relacionada a su posición en el arreglo de proyectos
        this.nombre = nombre;
        this.resumen = resumen;
        this.fecha_inicio = fecha_inicio;
        this.fecha_fin = fecha_fin;
        this.tareas = [];
        this.personas = [];
    }
}

class Tarea {
    constructor(id, nombre, persona, inicio, termino, prioridad, estado) {
        this.id = id; // ID de la tarea, combinación de la ID del proyecto y la posición de la tarea en el arreglo de tareas
        this.nombre = nombre;
        this.persona = persona;
        this.inicio = inicio;
        this.termino = termino;
        this.prioridad = prioridad;
        this.estado = estado;
    }
}


active_project_id = "Project-0";

// Arreglo de proyectos, con el proyecto para guardar las tareas sin proyecto en la primer posición
Proyectos = [
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
            let newTask = new Tarea(taskId, item.nombre_tarea, item.nombre_persona, item.fecha_inicio, item.fecha_fin, item.prioridad, item.estado);
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
    let project = Proyectos.find(proj => proj.id === project_id);
    let project_detail = document.querySelector('.project-detail');
    let header = document.createElement('h1');
    header.textContent = project.nombre;
    let summary = document.createElement('p');
    summary.textContent = project.resumen;

    project_detail.innerHTML = '';
    project_detail.appendChild(header);
    project_detail.appendChild(summary);


    let personas = [...new Set(project.personas)];
    personas.forEach(persona => {
        let sectionTemplate = document.getElementById('tem-task-section');
        let sectionItem = sectionTemplate.content.cloneNode(true);
        let section = sectionItem.querySelector('.section');
        section.id = `tareas-${persona}`;
        section.querySelector('.section-title h2').textContent = `Tareas de ${persona}`;
        let taskList = section.querySelector('.task-list');

        project.tareas.forEach(tarea => {
            if (tarea.persona.includes(persona)) {
                let taskTemplate = document.getElementById('tem-task-item');
                let taskItem = taskTemplate.content.cloneNode(true);
                let task = taskItem.querySelector('.task-list__item');
                let checkbox = task.querySelector('.form-check-input');
                let label = task.querySelector('.form-check-label');
                let status = task.querySelector('.tag');

                task.id = tarea.id;
                checkbox.id = tarea.id;
                checkbox.name = tarea.id;
                label.setAttribute('for', tarea.id);
                label.textContent = tarea.nombre;
                status.textContent = tarea.estado;
                taskList.appendChild(taskItem);
            }
        });

        project_detail.appendChild(sectionItem);
    });

    let unassignedSectionTemplate = document.getElementById('tem-task-section');
    let unassignedSectionItem = unassignedSectionTemplate.content.cloneNode(true);
    let unassignedSection = unassignedSectionItem.querySelector('.section');
    unassignedSection.id = 'tareas-sin-persona';
    unassignedSection.querySelector('.section-title h2').textContent = 'Tareas sin persona asignada';
    let unassignedTaskList = unassignedSection.querySelector('.task-list');

    let unassignedTasks = project.tareas.filter(tarea => !tarea.persona);
    if (unassignedTasks.length > 0) {
        unassignedTasks.forEach(tarea => {
            let taskTemplate = document.getElementById('tem-task-item');
            let taskItem = taskTemplate.content.cloneNode(true);
            let task = taskItem.querySelector('.task-list__item');
            let checkbox = task.querySelector('.form-check-input');
            let label = task.querySelector('.form-check-label');
            let status = task.querySelector('.tag');

            task.id = tarea.id;
            checkbox.id = tarea.id;
            checkbox.name = tarea.id;
            label.setAttribute('for', tarea.id);
            label.textContent = tarea.nombre;
            status.textContent = tarea.estado;
            unassignedTaskList.appendChild(taskItem);
        });
    } else {
        unassignedTaskList.innerHTML = '<li>Sin tareas no asignadas</li>';
    }

    project_detail.appendChild(unassignedSectionItem);
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


// Makes a label editable by taking the checkbox's id and making its label editable, toggling the contenteditable attribute
function edit_task(current_caller, task_id) {
    
    var task = document.getElementById(task_id);
    var label = task.labels[0];
    label.contentEditable = true;
    label.focus();
    label.addEventListener('click', stop_it);

    // Change this tag's value to editing text and it's class 'tag-info' to 'tag-success'
    current_caller.innerHTML = "Save";
    current_caller.classList.remove('tag-info');
    current_caller.classList.add('tag-success');
    current_caller.onclick = function() { save_task(current_caller, task_id); }
}


function save_task(current_caller, task_id) {
    var task = document.getElementById(task_id);
    var label = task.labels[0];
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