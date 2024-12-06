function showEditForm(choreographerId) {
    let form = document.getElementById('edit-form-' + choreographerId);
    form.classList.toggle('form-hidden');
}

function showAddForm() {
    let form = document.getElementById('add-form');
    form.classList.toggle('form-hidden');
}

function changeTheme() {
    let container = document.getElementById('body');
    container.classList.toggle('light');
    container.classList.toggle('dark');
}
