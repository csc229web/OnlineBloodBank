/*
Javascript file for OnlineBloodBank
Authors Lynn & Joshua
V1.0.0
*/

function validateForm() {
    var x = document.forms["donor"]["donor_lastname"].value;
    if (x == "") {
        alert("Name must be filled out");
        return false;
    }
}