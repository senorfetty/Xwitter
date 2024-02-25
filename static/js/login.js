showPass= () => {
    pass= document.getElementById( "password" )  
    if (pass.type === 'password') {
        pass.type='text';
    } else {
        pass.type = 'password'; 
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



