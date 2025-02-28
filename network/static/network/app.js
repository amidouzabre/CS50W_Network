// Get editables posts
posts_editables = document.querySelectorAll('.post-box p[data-post-editable]');

// Get like
post_like_btns = document.querySelectorAll('.like');



// Get the authenticated user
const authenticatedUser = document.querySelector('#user-authenticated');

if(authenticatedUser){
   
    // Edit post
    posts_editables.forEach(post => {
        post.addEventListener('click', function() {
            const postId = this.getAttribute('data-post-id');

            const postForm = document.querySelector(`#post-form-${postId}`);
            postForm.hidden = !postForm.hidden;
            post.hidden = !post.hidden;

            if (!postForm.hidden) {
                const textarea = postForm.querySelector('textarea');
                textarea.focus();


                // Cancel button    
                if(postForm.oncancel === null) {
                    postForm.oncancel = function() {
                        postForm.hidden = true;
                        post.hidden = false;
                    }
                }

                const cancelButton = postForm.querySelector('input[type="button"]');
                cancelButton.addEventListener('click', postForm.oncancel);
            }
        });


        const form = document.querySelector(`#post-form-${post.getAttribute('data-post-id')}`);
        form.addEventListener('submit', function(event) {
            event.preventDefault();
            const content = form.querySelector('textarea').value;

            try {
                const result =  fetchJSON(`/post/edit/${post.getAttribute('data-post-id')}`, {
                    method: 'POST',
                    body: JSON.stringify({
                        content: content
                    }),
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
        });
    });


    // Like or Dislike
    
    post_like_btns.forEach(btn => {
        btn.addEventListener('click', function (event){
            event.preventDefault;
            const postId = this.getAttribute('data-post-id');
            console.log(postId)
        })
    })




};

/**
 * Fecth JSON
 * @param {string} url 
 * @param {object} options 
 * @returns 
 */
async function fetchJSON(url, options = {}) {
    const headers = {Accept: 'application/json', ...options.headers}
    const r = await fetch(url, {...options, headers})
    if (r.ok) {
      return r.json()
    }
    
    throw new Error("Impossble to get json", {cause: r})
  }