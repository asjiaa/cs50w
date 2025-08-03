document.addEventListener('DOMContentLoaded', function() {

    document.querySelectorAll('[data-class=edit-post]').forEach(button => {
        button.addEventListener('click', () => edit_post(
            button.dataset.id
        ))
    });

    document.querySelectorAll('[data-class=like-post]').forEach(button => {
        button.addEventListener('click', () => like_post(
            button.dataset.id
        ))
    });
})

// Specification 6 - Edit Post

function edit_post(id) {
    const content = document.querySelector(`[data-id=post-${id}-content]`);
    const post = document.querySelector(`[data-id=post-${id}-text]`).textContent;
    content.innerHTML = "";
    const edit = document.createElement('div');
    edit.innerHTML = `
        <form id=edit-form-${id}>
            <textarea cols="40" rows="5" class="form-control" id="edit-content-${id}"></textarea>
            <input type="submit" class="btn btn-primary mt-1" value="Save"/>
        </form>
    `
    content.append(edit);
    document.querySelector(`#edit-content-${id}`).value = post.trim();
    document.querySelector(`#edit-form-${id}`).onsubmit = (event) => save_post(event, id);
}

async function save_post(event, id) {
    event.preventDefault();
    await fetch(`/posts/${id}`, {
        method: 'PUT',
        body: JSON.stringify({
            content: document.querySelector(`#edit-content-${id}`).value
        })
    })

    const post = await get_post(id);
    const content = document.querySelector(`[data-id=post-${id}-content]`);
    content.innerHTML = "";
    content.innerHTML = `
        <div>
            <button type="button" class="btn btn-link p-0" data-class="edit-post" data-id="${id}">
                Edit
            </button>
        </div>
        <div data-id="post-${id}-text">
            ${post.content}
        </div>
    `;
    document.querySelector(`[data-class="edit-post"][data-id="${id}"]`).addEventListener('click', () => edit_post(id));
}

// Specification 7 - "Like" & "Unlike"

async function like_post(id) {
    await fetch(`/posts/${id}`, {
        method: 'PUT',
        body: JSON.stringify({
            likes: Number(id)
        })
    })

    const post = await get_post(id);
    const icon = document.querySelector(`[data-class="like-post"][data-id="${id}"]`);
    if (icon.classList.contains('bi-heart-fill')) {
        icon.classList.remove('bi-heart-fill');
        icon.classList.add('bi-heart');
    } else {
        icon.classList.remove('bi-heart');
        icon.classList.add('bi-heart-fill');
    }
    document.querySelector(`[data-id=post-${id}-likes]`).innerHTML = "";
    document.querySelector(`[data-id=post-${id}-likes]`).innerHTML = post.likes;
}

async function get_post(id) {
    const response = await fetch(`posts/${id}`);
    const post = await response.json();
    return post;
}