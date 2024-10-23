document.getElementById('resource-form').addEventListener('submit', function(event) {
    event.preventDefault();

    const resourceName = document.getElementById('resource-name').value;
    const resourceType = document.getElementById('resource-type').value;

    addResource(resourceName, resourceType);

    document.getElementById('resource-form').reset();
});

function addResource(name, type) {
    const list = document.getElementById('resource-list');

    const listItem = document.createElement('li');
    listItem.textContent = `${name} (${type})`;

    const deleteButton = document.createElement('button');
    deleteButton.textContent = 'Remover';
    deleteButton.classList.add('delete');
    deleteButton.onclick = function() {
        list.removeChild(listItem);
    };

    listItem.appendChild(deleteButton);
    list.appendChild(listItem);
}