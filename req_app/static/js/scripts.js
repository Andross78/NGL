document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM LOADED')

    let resetBtn = document.querySelector('#reset-btn');
        authorNameField = document.querySelector('#author-name');
    
    resetBtn.addEventListener('click', function() {
        authorNameField.value = ''
    })
})