document.getElementById("predictionForm").addEventListener("submit", function(e){

e.preventDefault();

/* Selected bone */

let boneType = document.getElementById("boneType").value;

/* Patient inputs */

let age = document.getElementById("age").value;
let gender = document.getElementById("gender").value;
let bmi = document.getElementById("bmi").value;
let boneDensity = document.getElementById("boneDensity").value;
let calcium = document.getElementById("calcium").value;
let vitaminD = document.getElementById("vitaminD").value;


/* Send data to backend */

fetch("/predict",{

method:"POST",

headers:{
"Content-Type":"application/json"
},

body:JSON.stringify({

features:[
Number(age),
Number(gender),
Number(bmi),
Number(boneDensity),
Number(calcium),
Number(vitaminD)
],

bone: boneType

})

})

.then(res => res.json())

.then(data => {

/* Store prediction */

localStorage.setItem("predictionResult", data.prediction);
localStorage.setItem("fractureRisk", data.fracture_risk);
localStorage.setItem("selectedBone", boneType);
localStorage.setItem("boneDiseases", JSON.stringify(data.diseases));


/* Multi bone simulation */

let hipRisk = data.prediction;
let spineRisk = data.prediction;
let wristRisk = data.prediction;
let kneeRisk = data.prediction;

localStorage.setItem("hipRisk", hipRisk);
localStorage.setItem("spineRisk", spineRisk);
localStorage.setItem("wristRisk", wristRisk);
localStorage.setItem("kneeRisk", kneeRisk);


/* Overall bone health */

let highCount = 0;

[hipRisk,spineRisk,wristRisk,kneeRisk].forEach(r => {

if(r.includes("High")){
highCount++;
}

});

let overall;

if(highCount >= 3){
overall = "Severe Bone Weakness";
}
else if(highCount >= 2){
overall = "Moderate Bone Weakness";
}
else if(highCount === 1){
overall = "Mild Bone Weakness";
}
else{
overall = "Healthy Bone Condition";
}

localStorage.setItem("overallBoneHealth", overall);


/* Go to result page */

window.location.href="/result";

})

.catch(err=>{
alert("Prediction failed");
console.log(err);
});

});