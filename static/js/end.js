// A script resizing textareas, so they fit to content
// Credit to user DreamTeK from StackOverflow
console.log('end.js works');
$("textarea").each(function () {
  this.setAttribute("style", "height:" + (this.scrollHeight) + "px;overflow-y:hidden;");
  console.log(this);
}).on("input", function () {
  this.style.height = 0;
  this.style.height = (this.scrollHeight) + "px";
});