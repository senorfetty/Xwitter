showPassW = () => {
    pass = document.getElementById('password');
    if (pass.type === 'password') {
        pass.type = 'text';
    } else {
        pass.type = 'password';
    }
}

// showPass2 = () => {
//     pass = document.getElementById('password2');
//     if (pass.type === 'password') {
//         pass.type = 'text';
//     } else {
//         pass.type = 'password';
//     }
// }

showPass = () => {
    pass1 = document.getElementById('id_new_password1')
    pass2 = document.getElementById('id_new_password2')

    if (pass1.type === "password" && pass2.type === 'password'){
        pass1.type = 'text';
        pass2.type = 'text';
    } else {
        pass1.type = 'password';
        pass2.type = 'password';
    }
}

showPassword = () => {
    pass1 = document.getElementById('password1')
    pass2 = document.getElementById('password2')

    if (pass1.type === "password" && pass2.type === 'password'){
        pass1.type = 'text';
        pass2.type = 'text';
    } else {
        pass1.type = 'password';
        pass2.type = 'password';
    }
}

const remember = document.getElementById('rememberMe');
const uName= document.getElementById('username');

if (localStorage.checkbox && localStorage.checkbox !== '') {
    remember.setAttribute('checked',true)
    uName.value=localStorage.username; 
} else {
    remember.removeAttributeAttribute('checked');
    uName.value='';
}

 function IsRememberMe() {
    if (remember.checked && uName.value !== '' ) {
        localStorage.username=uName.value;
        localStorage.checkbox = remember.value;
    } else {
        localStorage.uName= '';
        localStorage.checkbox= '';
    }
}

document.addEventListener('DOMContentLoaded', function() {
    var datePicker = document.getElementById('datepicker');

    datePicker.addEventListener('input', function() {
        var selectedDate = new Date(this.value);
        var minDate = new Date('01-01-1924');
        var maxDate = new Date('31-12-2014');

        // Check if selectedDate is within the allowed range
        if (selectedDate < minDate || selectedDate > maxDate) {
            this.value = ''; // Clear the input if the selected date is outside the allowed range
            alert('Please select a date between 1924 and 2014.');
        }
    });
});
