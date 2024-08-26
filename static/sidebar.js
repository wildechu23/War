function openNav() {
    document.getElementById("mySidenav").style.width = "200px";
}
function closeNav() {
    document.getElementById("mySidenav").style.width = "0";
}
function openRules() {
    document.getElementById("Rules").style.width = "300px";
}
function closeRules() {
    document.getElementById("Rules").style.width = "0";
}
function openMoveInfo() {
    document.getElementById("MoveInfo").style.width = "300px";
}
function closeMoveInfo() {
    document.getElementById("MoveInfo").style.width = "0";
}
function openAchievements() {
    document.getElementById("Achievements").style.width = "300px";
}
function closeAchievements() {
    document.getElementById("Achievements").style.width = "0";
}
function openStats() {
    document.getElementById("Stats").style.width = "300px";
}
function closeStats() {
    document.getElementById("Stats").style.width = "0";
}
function openContacts() {
    document.getElementById("Contacts").style.width = "300px";
}
function closeContacts() {
    document.getElementById("Contacts").style.width = "0";
}

var dropdown = document.getElementsByClassName("dropdown-btn-resource");
var i;

for (i = 0; i < dropdown.length; i++) {
  dropdown[i].addEventListener("click", function() {
    this.classList.toggle("active-resource");
    var dropdownContent = this.nextElementSibling;
    if (dropdownContent.style.display === "block") {
      dropdownContent.style.display = "none";
    } else {
      dropdownContent.style.display = "block";
    }
  });
 }
 
var dropdown = document.getElementsByClassName("dropdown-btn-attack");
var i;

for (i = 0; i < dropdown.length; i++) {
  dropdown[i].addEventListener("click", function() {
    this.classList.toggle("active-attack");
    var dropdownContent = this.nextElementSibling;
    if (dropdownContent.style.display === "block") {
      dropdownContent.style.display = "none";
    } else {
      dropdownContent.style.display = "block";
    }
  });
 } 
 
var dropdown = document.getElementsByClassName("dropdown-btn-defense");
var i;

for (i = 0; i < dropdown.length; i++) {
  dropdown[i].addEventListener("click", function() {
    this.classList.toggle("active-defense");
    var dropdownContent = this.nextElementSibling;
    if (dropdownContent.style.display === "block") {
      dropdownContent.style.display = "none";
    } else {
      dropdownContent.style.display = "block";
    }
  });
 } 
 
var dropdown = document.getElementsByClassName("dropdown-btn-special");
var i;

for (i = 0; i < dropdown.length; i++) {
  dropdown[i].addEventListener("click", function() {
    this.classList.toggle("active-special");
    var dropdownContent = this.nextElementSibling;
    if (dropdownContent.style.display === "block") {
      dropdownContent.style.display = "none";
    } else {
      dropdownContent.style.display = "block";
    }
  });
 }  
 
var dropdown = document.getElementsByClassName("dropdown-btn-general");
var i;

for (i = 0; i < dropdown.length; i++) {
  dropdown[i].addEventListener("click", function() {
    this.classList.toggle("active-general");
    var dropdownContent = this.nextElementSibling;
    if (dropdownContent.style.display === "block") {
      dropdownContent.style.display = "none";
    } else {
      dropdownContent.style.display = "block";
    }
  });
 } 