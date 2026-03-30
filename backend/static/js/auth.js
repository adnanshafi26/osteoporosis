let slides = document.getElementById("slides")

function showSignup(){

slides.style.transform="translateX(-100%)"

}

function showSignin(){

slides.style.transform="translateX(-200%)"

}

function showInfo(){

slides.style.transform="translateX(100%)"

}


// Register

function register(){

fetch("/register",{

method:"POST",

headers:{
"Content-Type":"application/json"
},

body:JSON.stringify({

name:document.getElementById("name").value,
email:document.getElementById("email").value,
password:document.getElementById("password").value

})

})

.then(res=>res.json())

.then(data=>{

alert("Registered successfully")

})

}


// Login

function login(){

fetch("/login",{

method:"POST",

headers:{
"Content-Type":"application/json"
},

body:JSON.stringify({

email:document.getElementById("login_email").value,
password:document.getElementById("login_password").value

})

})

.then(res=>res.json())

.then(data=>{

if(data.status=="success"){

window.location="/"

}

else{

alert("Invalid login")

}

})

}