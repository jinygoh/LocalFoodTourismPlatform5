document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.favorite-btn').forEach(button => {
        button.addEventListener('click', function (e) {
            e.preventDefault();

            const model = this.dataset.model;
            const id = this.dataset.id;
            const icon = this.querySelector('.material-symbols-outlined');

            fetch(`/api/toggle_favorite/${model}/${id}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'Content-Type': 'application/json'
                }
            })
                .then(response => response.json())
                .then(data => {
                    if (data.status === 'added') {
                        icon.textContent = 'favorite';
                    } else if (data.status === 'removed') {
                        icon.textContent = 'favorite_border';
                    }
                });
        });
    });
});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
