class Proyecto {
    constructor(id, nombre, resumen, fecha_inicio, fecha_fin, estado, prioridad, responsable) {
        this.id = id; // ID del proyecto, relacionada a su posición en el arreglo de proyectos
        this.nombre = nombre;
        this.resumen = resumen;
        this.fecha_inicio = fecha_inicio;
        this.fecha_fin = fecha_fin;
        this.estado = estado;
        this.prioridad = prioridad;
        this.tareas = [];
        this.responsable = responsable;
        this.personas = [];
    }
}

class Tarea {
    constructor(id, nombre, proyecto, persona, inicio, termino, prioridad, estado, resumen, sprint) {
        this.id = id; // ID de la tarea, combinación de la ID del proyecto y la posición de la tarea en el arreglo de tareas
        this.nombre = nombre;
        this.proyecto = proyecto; // La ID del proyecto al que pertenecen
        this.persona = persona;
        this.sprint = sprint;
        this.inicio = inicio;
        this.termino = termino;
        this.prioridad = prioridad;
        this.estado = estado;
        this.resumen = resumen;
    }
}

class Sprint {
    constructor(id, nombre, fecha_inicio, fecha_fin, estado) {
        this.id = id; // ID del proyecto, relacionada a su posición en el arreglo de proyectos
        this.nombre = nombre;
        this.fecha_inicio = fecha_inicio;
        this.fecha_fin = fecha_fin;
        this.estado = estado;
        this.tareas = [];
        this.personas = [];
    }
}
active_project_id = "Project-0";

// Arreglo de proyectos, con el proyecto para guardar las tareas sin proyecto en la primer posición
let Proyectos = [
    new Proyecto("Project-0", "Tareas sin proyecto", "Proyecto para guardar tareas sin un nombre de proyecto", "2024-12-07", "2024-12-08", "alta", "Karina")
];



let Sprints = [
    new Sprint("Project-0", "Tareas sin sprints", "2024-12-07", "2024-12-08","Current")
];
Personas = [];
num_proyectos_sin_nombre = 0;

function create_project_list(data) {
    
    data.forEach((item, index) => {

        if (item.tipo === 'proyecto') {
            let projectExists = Proyectos.some(proj => proj.nombre === item.nombre_proyecto);
            if (!projectExists) {
                let projectId = item.id_proyecto;
                let projectName = item.nombre_proyecto || `${projectId} Proyecto sin nombre`;
                let newProject = new Proyecto(projectId, projectName, "nohay", item.fecha_inicio, item.fecha_fin, item.estado, item.prioridad, item.responsable);
                Proyectos.push(newProject);
            }
        }
        if (item.tipo === 'sprint'){
            let sprintExists = Sprints.some(spri => spri.nombre === item.nombre_sprint);
            if(!sprintExists){
                let sprintId = item.id_sprint;
                let sprintName = item.nombre_sprint || `${projectId} Sprint sin nombre`
                let newSprint = new Sprint(sprintId, sprintName, item.fecha_inicio, item.fecha_fin, item.estado);
                Sprints.push(newSprint);
            }
        }
    });

    data.forEach((item) => {
        if (item.tipo === 'tarea') {
            
            let project = Proyectos.find(proj => proj.id === item.id_proyecto) || Proyectos[0];
            let sprint = Sprints.find(spri => spri.id === item.id_sprint) || Sprints[0];

            let taskId = `${project.id}-Task-${project.tareas.length}`;
            let newTask = new Tarea(taskId, item.nombre_tarea, item.id_proyecto, item.nombre_persona, item.fecha_inicio, item.fecha_fin, item.prioridad, item.estado, item.resumen, item.id_sprint);
            sprint.tareas.push(newTask);
            project.tareas.push(newTask);
            
            let persona = item.nombre_persona;

            if (!project.personas.includes(persona) && project.id===item.id_proyecto) {
                project.personas.push(persona);
            } else if (!Proyectos[0].personas.includes(persona) && item.id_proyecto==="") {
                Proyectos[0].personas.push(persona);
            }

            if (!sprint.personas.includes(persona) && sprint.id===item.id_sprint) {
                sprint.personas.push(persona);
            } else if (!Sprints[0].personas.includes(persona) && item.id_sprint==="") {
                Sprints[0].personas.push(persona);
            }
        
        }
    });

    Proyectos[0].personas.pop();
    Sprints[0].personas.pop();
}

function show_project_tasks(project_id) {
    let project = Sprints.find(proj => proj.id === project_id);
    let project_detail = document.querySelector('.project-detail');
    let header = document.createElement('h1');
    header.textContent = project.nombre;
    
    if (project.id == "Project-0"){
        let summary = document.createElement('p');
        summary.textContent = "Sprint para guardar tareas sin sprint relacionado";
        project_detail.innerHTML = '';
        project_detail.appendChild(header);
        project_detail.appendChild(summary);
    }else{
        let summary = document.createElement('p');
        summary.textContent = "Responsable: "+project.responsable;
        let summary2 = document.createElement('p');
        summary2.textContent = "Estado: "+project.estado;
        let summary4 = document.createElement('p');
        summary4.textContent = "Fecha: "+project.fecha_inicio+" - "+project.fecha_fin;
        project_detail.innerHTML = '';
        project_detail.appendChild(header);
        project_detail.appendChild(summary);
        project_detail.appendChild(summary2);
        project_detail.appendChild(summary4);

        let taskTemplate = document.getElementById('tem-task-item');
        let taskItem = taskTemplate.content.cloneNode(true);
        let task = taskItem.querySelector('.task-list__item');

        let priority = task.querySelector('.tag-priority');
        let editButton = task.querySelector('.tag-edit');
        let crear = task.querySelector('.tag-status');

        crear.textContent = "Crear Tarea";
        crear.style = "width: 20%; inline-block";
           
        priority.textContent = "Editar Sprint";
        priority.classList.add('tag-info');
        priority.style = "width: 20%; inline-block";
        editButton.textContent = "Eliminar Sprint";
        editButton.classList.add('tag-danger');
        editButton.style = "width: 20%; inline-block";
        
                
        editButton.addEventListener('click', () => delete_project(project.nombre));
        priority.addEventListener('click', () => edit_project(project.id));
        crear.addEventListener('click', () => create_task(project.nombre));

        const project_detail2 = document.createElement('div');
        project_detail2.appendChild(crear);
        project_detail2.appendChild(priority);
        project_detail2.appendChild(editButton);
        project_detail.appendChild(project_detail2);
    }
    
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
                checkbox.disabled = true;
                label.setAttribute('for', tarea.id);
                label.textContent = tarea.nombre;
                status.textContent = "Consultar";
                
                priority.textContent = "Editar";
                priority.classList.add('tag-info');
                editButton.classList.add('tag-danger');
                
                editButton.id = `edit-${tarea.id}`;
                editButton.addEventListener('click', () => delete_task(tarea.nombre));

                status.addEventListener('click', () => read_task(tarea.id));
                priority.addEventListener('click', () => edit_task(tarea.id));

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
            let status = task.querySelector('.tag-status');
            let priority = task.querySelector('.tag-priority');
            let editButton = task.querySelector('.tag-edit');

            task.id = tarea.id;
            checkbox.id = tarea.id;
            checkbox.name = tarea.id;
            checkbox.disabled = true;
            label.setAttribute('for', tarea.id);
            label.textContent = tarea.nombre;
            status.textContent = "Consultar";
            
            priority.textContent = "Editar";
            priority.classList.add('tag-info');
            editButton.classList.add('tag-danger');
            
            editButton.id = `edit-${tarea.id}`;
            editButton.addEventListener('click', () => delete_task(tarea.id));

            status.addEventListener('click', () => read_task(tarea.id));
            priority.addEventListener('click', () => edit_task(tarea.id));
            unassignedTaskList.appendChild(taskItem);
        });
    } else {
        unassignedTaskList.innerHTML = '<li>Sin tareas no asignadas</li>';
    }

    project_detail.appendChild(unassignedSectionItem);
}

function show_project_blocks() {
    
    Sprints.forEach((project, index) => {
        let template = document.getElementById('tem-project-list-item');
        let projectItem = template.content.cloneNode(true);
        let projectBlock = projectItem.querySelector('.project-list__item');
        projectBlock.id = project.id;
        projectBlock.querySelector('.project-name').textContent =project.nombre;
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


function create_task(project_nombre) {

    let popupContent = `<form action = "/CrearTarea/" method = "POST">
            <input type = "hidden" name ="tipo" value="proyecto">
            <label>Nombre: <input required type="text" name="nombre_tarea" ></label>
            <label>Persona: <input required type="text" name="nombre_persona" ></label>
            <label>Proyecto: <select required name="nombre_proyecto">
                ${Proyectos.map(proj => `<option value="${proj.nombre}" ${proj.id === taskData.proyecto ? 'selected' : 'true'}>${proj.nombre}</option>`).join('')}</select></label>
            <label>Sprint: <input required type="text" name="nombre_sprint" value="${project_nombre}" readonly></label>
            <label>Fecha Inicio: <input required type="text" name="fecha_inicio"></label>
            <label>Fecha Fin: <input required type="text" name="fecha_fin" ></label>
            <label>Prioridad: <select required name="prioridad">
                    <option value="alta" >Alta</option>
                    <option value="media">Media</option>
                    <option value="baja">Baja</option>
                </select>
            </label>
            <label>Estado: <select required name="estado">
                    <option value="en curso">En curso</option>
                    <option value="hecho" >Hecho</option>
                    <option value="sin empezar">Sin empezar</option>
                </select>
            </label>
            <label>Resumen: 
                <textarea id="summary-textarea" required name="resumen" style="height: 60px;"></textarea>
                <button type="button" name="expand-resumen-btn" class="expand-btn">Expandir</button>
            </label>
            <button class="pop-btn-submit" type="submit">Guardar</button>
        </form>
    `;

    let popup = new Popup({
        content: popupContent, 
        width: '60%',
        height: 'auto',
        title: 'Crear Tarea',
        fontSizeMultiplier: 0.8
    });

    popup.show();

    document.querySelector('.popup-title').style.fontSize = '15px';


    const buttons2 = document.getElementsByName('expand-resumen-btn');
    const textareas = document.getElementsByName('resumen');

    for (let i = 0; i < buttons2.length; i++) {
        buttons2[i].addEventListener('click', () => {
            let textarea = textareas[i];
            let butto = buttons2[i];
            if (textarea.classList.contains('expanded')) {
                textarea.classList.remove('expanded');
                textarea.style.height = '60px'; // Altura contraída
                butto.textContent = 'Expandir'; // Texto del botón
            } else {
                textarea.classList.add('expanded');
                textarea.style.height = '150px'; // Altura expandida
                butto.textContent = 'Contraer'; // Texto del botón
            }
        });
    }

}



function edit_task(task_id) {
    let taskData = Proyectos.flatMap(proj => proj.tareas).find(tarea => tarea.id === task_id);

    let popupContent = `<form action = "/EditarTarea/" method = "POST">
            <input type = "hidden" name ="tipo" value="proyecto">
            <label>Nombre: <input required type="text" name="nombre_tarea" value="${taskData.nombre}"></label>
            <label>Persona: <input required type="text" name="nombre_persona" value="${taskData.persona}"></label>
            <label>Proyecto: <select required name="nombre_proyecto">
                ${Proyectos.map(proj => `<option value="${proj.nombre}" ${proj.id === taskData.proyecto ? 'selected' : 'true'}>${proj.nombre}</option>`).join('')}</select></label>
            <label>Sprint: <select required name="nombre_sprint">
                ${Sprints.map(proj => `<option value="${proj.nombre}" ${proj.id === taskData.sprint ? 'selected' : 'true'}>${proj.nombre}</option>`).join('')}</select></label>
            <label>Fecha Inicio: <input required type="text" name="fecha_inicio" value="${taskData.inicio}"></label>
            <label>Fecha Fin: <input required type="text" name="fecha_fin" value="${taskData.termino}"></label>
            <label>Prioridad: <select required name="prioridad">
                    <option value="alta" ${taskData.prioridad === 'alta' ? 'selected' : 'true'}>Alta</option>
                    <option value="media" ${taskData.prioridad === 'media' ? 'selected' : 'true'}>Media</option>
                    <option value="baja" ${taskData.prioridad === 'baja' ? 'selected' : 'true'}>Baja</option>
                </select>
            </label>
            <label>Estado: <select required name="estado">
                    <option value="en curso" ${taskData.estado === 'en curso' ? 'selected' : 'true'}>En curso</option>
                    <option value="hecho" ${taskData.estado === 'hecho' ? 'selected' : 'true'}>Hecho</option>
                    <option value="sin empezar" ${taskData.estado === 'sin empezar' ? 'selected' : 'true'}>Sin empezar</option>
                </select>
            </label>
            <label>Resumen: <textarea required id="summary-textarea" name="resumen" style="height: 60px;">${taskData.resumen}</textarea>
                <button type="button" name="expand-resumen-btn" class="expand-btn">Expandir</button>
            </label>
            <button class="pop-btn-submit" type="submit">Guardar</button>
        </form>
    `;

    let popup = new Popup({
        content: popupContent, 
        width: '60%',
        height: 'auto',
        title: 'Editar tarea',
        fontSizeMultiplier: 0.8
    });

    popup.show();

    const buttons2 = document.getElementsByName('expand-resumen-btn');
    const textareas = document.getElementsByName('resumen');

    for (let i = 0; i < buttons2.length; i++) {
        buttons2[i].addEventListener('click', () => {
            let textarea = textareas[i];
            let butto = buttons2[i];
            if (textarea.classList.contains('expanded')) {
                textarea.classList.remove('expanded');
                textarea.style.height = '60px'; // Altura contraída
                butto.textContent = 'Expandir'; // Texto del botón
            } else {
                textarea.classList.add('expanded');
                textarea.style.height = '150px'; // Altura expandida
                butto.textContent = 'Contraer'; // Texto del botón
            }
        });
    }
}

function create_project() {

    let popupContent = `<form action = "/CrearSprint/" method = "POST">
            <label>Nombre: <input required type="text" name="nombre_sprint" ></label>
            <label>Fecha Inicio: <input required type="text" name="fecha_inicio" ></label>
            <label>Fecha Fin: <input required type="text" name="fecha_fin" ></label>
            <label>Estado: <select required name="estado">
                    <option value="Current" >En curso</option>
                    <option value="Next" }>Hecho</option>
                    <option value="Future" >Atraso</option>
                    <option value="Past">Planificación</option>
                    <option value="Last">En pausa</option>
                </select>
            </label>
            <button class="pop-btn-submit" type="submit">Guardar</button>
        </form>
    `;

    let popup = new Popup({
        content: popupContent, 
        width: '60%',
        height: 'auto',
        title: 'Crear Sprint',
        fontSizeMultiplier: 0.8
    });

    popup.show();

    const buttons2 = document.getElementsByName('expand-resumen-btn');
    const textareas = document.getElementsByName('resumen');

    for (let i = 0; i < buttons2.length; i++) {
        buttons2[i].addEventListener('click', () => {
            let textarea = textareas[i];
            let butto = buttons2[i];
            if (textarea.classList.contains('expanded')) {
                textarea.classList.remove('expanded');
                textarea.style.height = '60px'; // Altura contraída
                butto.textContent = 'Expandir'; // Texto del botón
            } else {
                textarea.classList.add('expanded');
                textarea.style.height = '150px'; // Altura expandida
                butto.textContent = 'Contraer'; // Texto del botón
            }
        });
    }
    
}

function edit_project(project_name) {

    let projectData = Proyectos.find(proj => proj.id === project_name);

    let popupContent = `<form action = "/EditarSprint/" method = "POST">
            <label>Nombre: <input required type="text" name="nombre_sprint" value="${projectData.nombre}"></label>
            <label>Fecha Inicio: <input required type="text" name="fecha_inicio" value="${projectData.fecha_inicio}"></label>
            <label>Fecha Fin: <input required type="text" name="fecha_fin" value="${projectData.fecha_fin}"></label>
            <label>Estado: <select required name="estado">
                    <option value="Current" ${projectData.estado === 'Current' ? 'selected' : 'true'}>En curso</option>
                    <option value="Next" ${projectData.estado === 'Next' ? 'selected' : 'true'}>Next</option>
                    <option value="Future" ${projectData.estado === 'Future' ? 'selected' : 'true'}>Future</option>
                    <option value="Past" ${projectData.estado === 'Past' ? 'selected' : 'true'}>Past</option>
                    <option value="Last" ${projectData.estado === 'Last' ? 'selected' : 'true'}>Last</option>
                </select>
            </label>
            <button class="pop-btn-submit" type="submit">Guardar</button>
        </form>
    `;

    let popup = new Popup({
        content: popupContent, 
        width: '60%',
        height: 'auto',
        title: 'Editar Proyecto',
        fontSizeMultiplier: 0.8
    });

    popup.show();

    const buttons2 = document.getElementsByName('expand-resumen-btn');
    const textareas = document.getElementsByName('resumen');

    for (let i = 0; i < buttons2.length; i++) {
        buttons2[i].addEventListener('click', () => {
            let textarea = textareas[i];
            let butto = buttons2[i];
            if (textarea.classList.contains('expanded')) {
                textarea.classList.remove('expanded');
                textarea.style.height = '60px'; // Altura contraída
                butto.textContent = 'Expandir'; // Texto del botón
            } else {
                textarea.classList.add('expanded');
                textarea.style.height = '150px'; // Altura expandida
                butto.textContent = 'Contraer'; // Texto del botón
            }
        });
    }
    
}

function edit_task(task_id) {
    let task = document.getElementById(task_id);
    let taskData = Proyectos.flatMap(proj => proj.tareas).find(tarea => tarea.id === task_id);

    let popupContent = `
        <div class="popup-content">
        <form action = "/EditarTarea/" method = "POST">
            <input type="hidden" name="id" value="${task_id}">
            <input type="hidden" name="nombre_sprint" value="${task_id}">
            <label>Nombre: <input type="text" name="nombre_tarea" value="${taskData.nombre}"></label>
            <label>Persona: <input type="text" name="nombre_persona" value="${taskData.persona}">
                <button class="icon" id="edit-persona-btn"><img class="icon" src="/static/edit.png" alt="edit"></button>
            </label>
            <label>Proyecto: <select name="nombre_proyecto">
                    ${Proyectos.map(proj => `<option value="${proj.nombre}" ${proj.id === taskData.proyecto ? 'selected' : 'true'}>${proj.nombre}</option>`).join('')}
                </select>
            </label>
            <label>Sprint: <select name="nombre_sprint">
                    ${Sprints.map(proj => `<option value="${proj.nombre}" ${proj.id === taskData.sprint ? 'selected' : 'true'}>${proj.nombre}</option>`).join('')}
                </select>
            </label>
            <label>Fecha Inicio: <input type="text" name="fecha_inicio" value="${taskData.inicio}"></label>
            <label>Fecha Fin: <input type="text" name="fecha_fin" value="${taskData.termino}"></label>
            <label>Prioridad: <select name="prioridad">
                    <option value="alta" ${taskData.prioridad === 'alta' ? 'selected' : 'true'}>Alta</option>
                    <option value="media" ${taskData.prioridad === 'media' ? 'selected' : 'true'}>Media</option>
                    <option value="baja" ${taskData.prioridad === 'baja' ? 'selected' : 'true'}>Baja</option>
                </select>
            </label>
            <label>Estado: <select name="estado">
                    <option value="en curso" ${taskData.estado === 'en curso' ? 'selected' : ''}>En curso</option>
                    <option value="hecho" ${taskData.estado === 'hecho' ? 'selected' : ''}>Hecho</option>
                    <option value="sin empezar" ${taskData.estado === 'sin empezar' ? 'selected' : ''}>Hecho</option>
                </select>
            </label>
            <label>Resumen: <input type="text" name="resumen" value="${taskData.resumen}"></label>
            </label>
            <button type="submit">Guardar</button>
        </form>
        <button name="cancel-task-btn">Cancelar</button>

        </div>
    `;

    let popup = new Popup({
        content: popupContent, 
        width: '60%',
        height: 'auto',
        title: 'Editar tarea',
        fontSizeMultiplier: 0.8
    });

    popup.show();

    const buttons = document.getElementsByName('cancel-task-btn');

    buttons.forEach(button => {
        button.addEventListener('click', () => {
            popup.hide();
        });
    });
}

function read_task(task_id) {
    
    let task = document.getElementById(task_id);
    let taskData = Proyectos.flatMap(proj => proj.tareas).find(tarea => tarea.id === task_id);
    let project = Proyectos.find(proj => proj.id === taskData.id_proyecto) || Proyectos[0];
    let sprint = Sprints.find(spri => spri.id === taskData.id_sprint) || Sprints[0];
    let popupContent = `
        <div class="popup-content">
            <h2>Detalles de la Tarea</h2>
            <strong>Nombre:</strong> ${taskData.nombre}
            <strong>Persona:</strong> ${taskData.persona}
            <strong>Proyecto:</strong> ${project.nombre}
            <strong>Sprint:</strong> ${sprint.nombre}
            <strong>Fecha Inicio:</strong> ${taskData.inicio}
            <strong>Fecha Fin:</strong> ${taskData.termino}
            <strong>Prioridad:</strong> ${taskData.prioridad}
            <strong>Estado:</strong> ${taskData.estado}
            <strong>Resumen:</strong> ${taskData.resumen}
            <button class ="regresar-task-btn-cla" name="regresar-task-btn">Regresar</button>

        </div>
    `;

    let popup = new Popup({
        content: popupContent, 
        width: '60%',
        height: 'auto',
        title: 'Editar tarea',
        fontSizeMultiplier: 0.8
    });

    popup.show();

    const buttons = document.getElementsByName('regresar-task-btn');

    buttons.forEach(button => {
        button.addEventListener('click', () => {
            popup.hide();
        });
    });
}

function delete_task(task_id){
    if (confirm('¿Estás seguro de que deseas eliminar esta tarea?')) {
        location.href =`/EliminarTarea/?nombre_tarea=${task_id}`
    }
}

function delete_project(task_id){
    if (confirm('¿Estás seguro de que deseas eliminar este sprint?')) {
        location.href =`/EliminarSprint/?nombre_proyecto=${task_id}`
    }
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


function edit_task_details(task_id) {
    //TODO: Implementar la edición de tareas
}

//document.addEventListener('DOMContentLoaded', function() {
//    create_project_list(Datos_incompletos);
//    show_project_blocks();
//    set_active(document.getElementById(active_project_id));
//    show_project_tasks(active_project_id);
//});