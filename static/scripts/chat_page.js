document.addEventListener('DOMContentLoaded', () => {
    //Make 'enter' key submit message
    let msg = document.querySelector('#user-message');
    msg.addEventListener('keyup', event => {
        if (event.keyCode === 13) {
            document.querySelector('#send-message'). click();
        } 
    })
})