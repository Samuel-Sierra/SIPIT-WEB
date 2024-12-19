class Proyecto {
    constructor(id, nombre, resumen, fecha_inicio, fecha_fin, estado, prioridad) {
        this.id = id; // ID del proyecto, relacionada a su posición en el arreglo de proyectos
        this.nombre = nombre;
        this.fecha_inicio = fecha_inicio;
        this.fecha_fin = fecha_fin;
        this.estado = estado;
        this.tareas = [];
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
let Proyectos = [
    new Proyecto("Project-0", "Tareas sin proyecto", "2024-12-07", "2024-12-08","Current")
];
Personas = [];

num_proyectos_sin_nombre = 0;

function create_project_list(data) {
    
    data.forEach((item, index) => {

        if (item.tipo === 'proyecto') {
            let projectExists = Proyectos.some(proj => proj.nombre === item.nombre_proyecto);
            if (!projectExists) {
                let projectId = item.id_proyecto;
                let projectName = item.nombre || `${projectId} Proyecto sin nombre`;
                let newProject = new Proyecto(projectId, projectName, item.fecha_inicio, item.fecha_fin, item.estado);
                Proyectos.push(newProject);
            }
        }
    });
    console.log(Proyectos)

    data.forEach((item) => {
        if (item.tipo === 'tarea') {
            let project = Proyectos.find(proj => proj.id === item.nombre_sprint) || Proyectos[0];
            let taskId = `${project.id}-Task`;
            let newTask = new Tarea(taskId, item.nombre_tarea, item.nombre_sprint, item.titular, item.fecha_inicio, item.fecha_fin, item.prioridad, item.estado);
            project.tareas.push(newTask);

            let persona = item.titular;
            
            if (!project.personas.includes(persona)) {
                project.personas.push(persona);
            } else if (!Proyectos[0].personas.includes(persona)) {
                Proyectos[0].personas.push(persona);
            }
        
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
                let status = task.querySelector('.tag-status');
                let priority = task.querySelector('.tag-priority');
                let editButton = task.querySelector('.tag-edit');

                task.id = tarea.id;
                checkbox.id = tarea.id;
                checkbox.name = tarea.id;
                label.setAttribute('for', tarea.id);
                label.textContent = tarea.nombre;
                status.textContent = tarea.estado;
                priority.textContent = tarea.prioridad;

                if (tarea.prioridad === 'alta') {
                    priority.classList.add('tag-danger');
                } else if (tarea.prioridad === 'media') {
                    priority.classList.add('tag-info');
                }

                editButton.id = `edit-${tarea.id}`;
                editButton.addEventListener('click', () => edit_task(tarea.id));
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

function edit_task(task_id) {
    let task = document.getElementById(task_id);
    let taskData = Proyectos.flatMap(proj => proj.tareas).find(tarea => tarea.id === task_id);

    let popupContent = `
        <div class="popup-content">
        <form action = "editarTarea" method = post
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

//document.addEventListener('DOMContentLoaded', function() {
//    create_project_list(Datos_incompletos);
//    show_project_blocks();
//    set_active(document.getElementById(active_project_id));
//    show_project_tasks(active_project_id);
//});