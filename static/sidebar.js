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
function openContact() {
    document.getElementById("Contact").style.width = "300px";
}
function closeContact() {
    document.getElementById("Contact").style.width = "0";
}

var dropdown = document.getElementsByClassName("dropdown-btn");
var i;

for (i = 0; i < dropdown.length; i++) {
  dropdown[i].addEventListener("click", function() {
    this.classList.toggle("active");
    var dropdownContent = this.nextElementSibling;
    if (dropdownContent.style.display === "block") {
      dropdownContent.style.display = "none";
    } else {
      dropdownContent.style.display = "block";
    }
  });
 }