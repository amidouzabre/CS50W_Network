// Get editables posts
posts_editables = document.querySelectorAll('.post-box [data-post-editable]');

// Get like
post_like_btns = document.querySelectorAll('.like');



// Get the authenticated user
const authenticatedUser = document.querySelector('#user-authenticated');

if(authenticatedUser){


    posts_editables.forEach(post => {

        
        const postId = post.getAttribute('data-post-id');
        const edit_btn = document.querySelector(`#edit-btn-${postId}`); // Remove 'button ' to directly target the button by ID
        const post_content = document.querySelector(`#post-content-${postId}`);
        const post_form = document.querySelector(`#post-form-${postId}`);
        const textarea = post_form.querySelector('textarea');

        // If click on edit button
        edit_btn?.addEventListener('click', function() { 
            showHideForm(post, post_form, post_content, textarea);
        });


        // Make post content clickable
        post_content?.addEventListener('click', function() {
            showHideForm(post, post_form, post_content, textarea);
        });


        // Add event listener that uses the function
        post_form?.addEventListener('submit', function(event) {
            event.preventDefault();
            updatePost(post_form, post);
        });
    
    });
   
   

    // Like or Dislike
    
    post_like_btns.forEach(btn => {
        btn?.addEventListener('click', function (event){
            event.preventDefault;
            const postId = this.getAttribute('data-post-id');

            fetchJSON(`/post/like/${postId}`, {
                method: 'GET',
                headers: {'Content-Type': 'application/json'}
            })
            .then(result => {
                const likesCount = this.querySelector('.likes-count');

                if (result.content === "liked") {
                    likesCount.textContent = parseInt(likesCount.textContent) + 1;
                    this.classList.add('fas');
                    this.classList.remove('far');
                } else if (result.content === "disliked") {
                    likesCount.textContent = parseInt(likesCount.textContent) - 1;
                    this.classList.add('far');
                    this.classList.remove('fas');
                }
            })
            .catch(error => {
                console.log(error);
                return null});

        })
    })


    // Follow or Unfollow
    const followBtn = document.querySelector('.follow');
    followBtn?.addEventListener('click', function(event){
        event.preventDefault();
        const userId = this.getAttribute('data-user-id');

        console.log(userId)
        
        fetchJSON(`follow/${userId}`, {
            method: 'GET',
            headers: {'Content-Type': 'application/json'}
        })
        .then(result => {

            const followersCount = document.querySelector('.followers');

            if (result.content === "followed") {
                followersCount.textContent = parseInt(followersCount.textContent) + 1;
                this.textContent = 'Unfollow';
                this.classList.remove('btn-dark');
                this.classList.add('btn-danger');
            } else if (result.content === "unfollowed") {
                followersCount.textContent = parseInt(followersCount.textContent) - 1;
                this.textContent = 'Follow';
                this.classList.remove('btn-danger');
                this.classList.add('btn-dark');
            }
        })
        .catch(error => {
            console.log(error);
            return null
        });
    });
};


/**
 * Fecth JSON
 * @param {string} url 
 * @param {object} options 
 * @returns 
 */
async function fetchJSON(url, options = {}) {
    const headers = {Accept: 'application/json', ...options.headers}
    return fetch(url, {...options, headers}).then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    });
}


// Define the update post function
async function updatePost(form, post) {
    const content = form.querySelector('textarea').value;
    try {
    const result = await fetchJSON(`/post/edit/${post.getAttribute('data-post-id')}`, {
        method: 'POST',
        body: JSON.stringify({ content }),
        headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': form.querySelector('[name=csrfmiddlewaretoken]').value
        }
    });

    if (result) {
        post.textContent = content;
        post.hidden = false;
        form.hidden = true;
    } else {
        alert('An error occurred while updating the post.');
    }
    } catch (error) {
    console.log(error);
    return null;
    }
}


/**
 * Show or Hide form
 * @param {HTMLElement} post 
 * @param {HTMLElement} form 
 * @param {HTMLElement} content 
 * @param {HTMLElement} textarea 
 */
function showHideForm(post, form, content, textarea) {
    form.hidden = !form.hidden;
    content.hidden = !content.hidden;
    if (!form.hidden) {
        textarea.focus();

        // Cancel button    
        if (form.oncancel === null) {
            form.oncancel = function() {
                form.hidden = true;
                post.hidden = false;
            }
        }

        const cancelButton = form.querySelector('input[type="button"]');
        cancelButton.addEventListener('click', form.oncancel);
    } else {
        form.hidden = true;
        post.hidden = false
    }
}

