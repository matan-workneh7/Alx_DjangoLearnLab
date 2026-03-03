// Blog JavaScript Functions

// DOM Content Loaded Event
document.addEventListener('DOMContentLoaded', function() {
    // Initialize any interactive elements
    initializeSearch();
    initializeComments();
    initializeForms();
});

// Search Functionality
function initializeSearch() {
    const searchInput = document.getElementById('search-input');
    if (searchInput) {
        searchInput.addEventListener('input', function(e) {
            const query = e.target.value.trim();
            if (query.length > 2) {
                // Optional: Implement live search suggestions
                performLiveSearch(query);
            }
        });
    }
}

function performLiveSearch(query) {
    // This could be implemented to show live search suggestions
    console.log('Searching for:', query);
}

// Comment Functionality
function initializeComments() {
    // Add event listeners for comment forms
    const commentForms = document.querySelectorAll('.comment-form');
    commentForms.forEach(form => {
        form.addEventListener('submit', handleCommentSubmit);
    });
    
    // Add event listeners for edit/delete buttons
    document.addEventListener('click', function(e) {
        if (e.target.classList.contains('edit-comment')) {
            handleCommentEdit(e.target);
        } else if (e.target.classList.contains('delete-comment')) {
            handleCommentDelete(e.target);
        }
    });
}

function handleCommentSubmit(e) {
    e.preventDefault();
    const form = e.target;
    const formData = new FormData(form);
    const submitBtn = form.querySelector('button[type="submit"]');
    
    // Disable submit button to prevent double submission
    submitBtn.disabled = true;
    submitBtn.textContent = 'Posting...';
    
    // Submit the form using fetch API
    fetch(form.action, {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Add the new comment to the comments list
            addCommentToList(data.comment);
            form.reset();
            showMessage('Comment posted successfully!', 'success');
        } else {
            showMessage('Error posting comment: ' + data.error, 'error');
        }
    })
    .catch(error => {
        showMessage('Error posting comment: ' + error.message, 'error');
    })
    .finally(() => {
        submitBtn.disabled = false;
        submitBtn.textContent = 'Post Comment';
    });
}

function handleCommentEdit(button) {
    const commentId = button.dataset.commentId;
    const commentElement = document.getElementById(`comment-${commentId}`);
    const contentElement = commentElement.querySelector('.comment-content');
    const currentContent = contentElement.textContent.trim();
    
    // Create edit form
    const editForm = document.createElement('form');
    editForm.className = 'comment-edit-form';
    editForm.innerHTML = `
        <div class="form-group">
            <textarea name="content" class="form-control" rows="3" required>${currentContent}</textarea>
        </div>
        <div class="form-group">
            <button type="submit" class="btn btn-primary">Save</button>
            <button type="button" class="btn btn-secondary cancel-edit">Cancel</button>
        </div>
    `;
    
    // Replace content with edit form
    contentElement.style.display = 'none';
    contentElement.parentNode.insertBefore(editForm, contentElement.nextSibling);
    
    // Handle form submission
    editForm.addEventListener('submit', function(e) {
        e.preventDefault();
        saveCommentEdit(commentId, editForm, contentElement);
    });
    
    // Handle cancel button
    editForm.querySelector('.cancel-edit').addEventListener('click', function() {
        editForm.remove();
        contentElement.style.display = 'block';
    });
}

function saveCommentEdit(commentId, form, contentElement) {
    const formData = new FormData(form);
    const submitBtn = form.querySelector('button[type="submit"]');
    
    submitBtn.disabled = true;
    submitBtn.textContent = 'Saving...';
    
    fetch(`/comments/${commentId}/edit/`, {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            contentElement.textContent = data.content;
            contentElement.style.display = 'block';
            form.remove();
            showMessage('Comment updated successfully!', 'success');
        } else {
            showMessage('Error updating comment: ' + data.error, 'error');
        }
    })
    .catch(error => {
        showMessage('Error updating comment: ' + error.message, 'error');
    })
    .finally(() => {
        submitBtn.disabled = false;
        submitBtn.textContent = 'Save';
    });
}

function handleCommentDelete(button) {
    if (confirm('Are you sure you want to delete this comment?')) {
        const commentId = button.dataset.commentId;
        const commentElement = document.getElementById(`comment-${commentId}`);
        
        fetch(`/comments/${commentId}/delete/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                commentElement.remove();
                showMessage('Comment deleted successfully!', 'success');
            } else {
                showMessage('Error deleting comment: ' + data.error, 'error');
            }
        })
        .catch(error => {
            showMessage('Error deleting comment: ' + error.message, 'error');
        });
    }
}

// Form Functionality
function initializeForms() {
    // Add character counters for textareas
    const textareas = document.querySelectorAll('textarea[maxlength]');
    textareas.forEach(textarea => {
        addCharacterCounter(textarea);
    });
    
    // Add form validation
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!validateForm(form)) {
                e.preventDefault();
            }
        });
    });
}

function addCharacterCounter(textarea) {
    const maxLength = parseInt(textarea.getAttribute('maxlength'));
    const counter = document.createElement('div');
    counter.className = 'character-counter';
    counter.textContent = `0 / ${maxLength}`;
    
    textarea.parentNode.insertBefore(counter, textarea.nextSibling);
    
    textarea.addEventListener('input', function() {
        const currentLength = textarea.value.length;
        counter.textContent = `${currentLength} / ${maxLength}`;
        
        if (currentLength > maxLength * 0.9) {
            counter.style.color = 'red';
        } else {
            counter.style.color = '#666';
        }
    });
}

function validateForm(form) {
    let isValid = true;
    const requiredFields = form.querySelectorAll('[required]');
    
    requiredFields.forEach(field => {
        if (!field.value.trim()) {
            isValid = false;
            field.classList.add('error');
            
            // Remove error class on input
            field.addEventListener('input', function() {
                field.classList.remove('error');
            }, { once: true });
        }
    });
    
    if (!isValid) {
        showMessage('Please fill in all required fields.', 'error');
    }
    
    return isValid;
}

// Tag Management
function initializeTagManager() {
    const tagInput = document.getElementById('tag-input');
    const tagContainer = document.getElementById('tag-container');
    
    if (tagInput && tagContainer) {
        tagInput.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' || e.key === ',') {
                e.preventDefault();
                addTag(tagInput.value.trim());
                tagInput.value = '';
            }
        });
    }
}

function addTag(tagName) {
    if (!tagName) return;
    
    const tagContainer = document.getElementById('tag-container');
    const existingTags = Array.from(tagContainer.querySelectorAll('.tag')).map(tag => tag.textContent);
    
    if (existingTags.includes(tagName)) {
        showMessage('Tag already exists!', 'warning');
        return;
    }
    
    const tagElement = document.createElement('span');
    tagElement.className = 'tag';
    tagElement.innerHTML = `
        ${tagName}
        <button type="button" class="remove-tag">&times;</button>
    `;
    
    tagContainer.appendChild(tagElement);
    
    // Add remove functionality
    tagElement.querySelector('.remove-tag').addEventListener('click', function() {
        tagElement.remove();
    });
}

// Utility Functions
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

function showMessage(message, type) {
    const messagesContainer = document.querySelector('.messages') || createMessagesContainer();
    
    const messageElement = document.createElement('div');
    messageElement.className = `message ${type}`;
    messageElement.textContent = message;
    
    messagesContainer.appendChild(messageElement);
    
    // Auto-remove message after 5 seconds
    setTimeout(() => {
        messageElement.remove();
    }, 5000);
}

function createMessagesContainer() {
    const container = document.createElement('div');
    container.className = 'messages';
    document.querySelector('main').prepend(container);
    return container;
}

function addCommentToList(comment) {
    const commentsList = document.querySelector('.comments-list');
    if (!commentsList) return;
    
    const commentElement = document.createElement('div');
    commentElement.className = 'comment';
    commentElement.id = `comment-${comment.id}`;
    commentElement.innerHTML = `
        <div class="comment-header">
            <span class="comment-author">${comment.author}</span>
            <span class="comment-date">${comment.created_at}</span>
        </div>
        <div class="comment-content">${comment.content}</div>
        <div class="comment-actions">
            <button class="btn btn-sm btn-secondary edit-comment" data-comment-id="${comment.id}">Edit</button>
            <button class="btn btn-sm btn-danger delete-comment" data-comment-id="${comment.id}">Delete</button>
        </div>
    `;
    
    commentsList.appendChild(commentElement);
}

// Smooth scrolling for anchor links
document.addEventListener('click', function(e) {
    if (e.target.tagName === 'A' && e.target.getAttribute('href').startsWith('#')) {
        e.preventDefault();
        const targetId = e.target.getAttribute('href');
        const targetElement = document.querySelector(targetId);
        
        if (targetElement) {
            targetElement.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    }
});

// Back to top button
function addBackToTopButton() {
    const button = document.createElement('button');
    button.className = 'back-to-top';
    button.innerHTML = '&uarr;';
    button.textContent = '↑';
    button.style.cssText = `
        position: fixed;
        bottom: 20px;
        right: 20px;
        background-color: var(--primary-color);
        color: white;
        border: none;
        border-radius: 50%;
        width: 50px;
        height: 50px;
        font-size: 20px;
        cursor: pointer;
        display: none;
        z-index: 1000;
    `;
    
    document.body.appendChild(button);
    
    // Show/hide button based on scroll position
    window.addEventListener('scroll', function() {
        if (window.pageYOffset > 300) {
            button.style.display = 'block';
        } else {
            button.style.display = 'none';
        }
    });
    
    // Scroll to top when clicked
    button.addEventListener('click', function() {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
}

// Initialize back to top button
addBackToTopButton();
