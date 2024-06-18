document.addEventListener('DOMContentLoaded', () => {
    const url = window.location.pathname;
    let apiEndpoint = '';

    if (url === '/users') {
        apiEndpoint = '/api/users';
    } else if (url === '/rooms') {
        apiEndpoint = '/api/rooms';
    } else if (url === '/meetings') {
        apiEndpoint = '/api/meetings';
    } else if (url === '/participants') {
        apiEndpoint = '/api/participants';
    }

    if (apiEndpoint) {
        fetch(apiEndpoint)
            .then(response => response.json())
            .then(data => {
                const list = document.querySelector('ul');
                data.forEach(item => {
                    const listItem = document.createElement('li');
                    listItem.textContent = JSON.stringify(item);
                    list.appendChild(listItem);
                });
            });
    }
});
