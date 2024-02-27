// showPass = () => {
//     pass = document.getElementById('password');
//     if (pass.type === 'password') {
//         pass.type = 'text';
//     } else {
//         pass.type = 'password';
//     }
// }

// showPass2 = () => {
//     pass = document.getElementById('password2');
//     if (pass.type === 'password') {
//         pass.type = 'text';
//     } else {
//         pass.type = 'password';
//     }
// }

showPass = () => {
    pass1 = document.getElementById('password')
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



