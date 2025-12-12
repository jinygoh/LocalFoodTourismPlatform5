/**
 * This script handles the client-side logic for the "favorite" functionality.
 * It adds an event listener to all elements with the class 'favorite-btn'.
 * When a button is clicked, it sends an asynchronous request to the server
 * to add or remove the item from the user's favorites and updates the UI
 * without a full page reload.
 */
document.addEventListener('DOMContentLoaded', function () {
    // Select all elements with the class 'favorite-btn'.
    document.querySelectorAll('.favorite-btn').forEach(button => {
        // Add a click event listener to each button.
        button.addEventListener('click', function (e) {
            // Prevent the default action (e.g., following a link if the button is an 'a' tag).
            e.preventDefault();

            // Retrieve the model type (e.g., 'shop', 'dish') and the object's ID
            // from the button's data attributes (data-model and data-id).
            const model = this.dataset.model;
            const id = this.dataset.id;
            // Find the icon element within the button to update its appearance.
            const icon = this.querySelector('.material-symbols-outlined');

            // Send an asynchronous POST request to the server's API endpoint.
            fetch(`/api/toggle_favorite/${model}/${id}/`, {
                method: 'POST',
                headers: {
                    // Include the CSRF token in the request headers for security.
                    // The getCookie function retrieves the token from the document's cookies.
                    'X-CSRFToken': getCookie('csrftoken'),
                    'Content-Type': 'application/json'
                }
            })
            // Parse the JSON response from the server.
            .then(response => response.json())
            // Process the data returned from the server.
            .then(data => {
                // If the item was added to favorites:
                if (data.status === 'added') {
                    // Change the icon to a solid heart.
                    icon.textContent = 'favorite';
                    // Add the 'favorited' class for styling (e.g., to make it red).
                    button.classList.add('favorited');
                }
                // If the item was removed from favorites:
                else if (data.status === 'removed') {
                    // Change the icon back to a bordered heart.
                    icon.textContent = 'favorite_border';
                    // Remove the 'favorited' class.
                    button.classList.remove('favorited');
                }
            });
        });
    });
});

/**
 * A utility function to retrieve a specific cookie by name.
 * This is necessary to get the CSRF token required for POST requests in Django.
 * @param {string} name - The name of the cookie to retrieve.
 * @returns {string|null} The value of the cookie, or null if not found.
 */
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
