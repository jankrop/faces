// A script resizing textareas, so they fit to content
// Credit to user DreamTeK from StackOverflow
$("textarea").each(function () {
    this.setAttribute("style", "height:" + (this.scrollHeight) + "px;overflow-y:hidden;");
}).on("input", function () {
    this.style.height = 0;
    this.style.height = (this.scrollHeight) + "px";
});

// A script for changing themes
function updateTheme() {
    if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
        document.body.setAttribute('data-bs-theme', 'dark');
        $('.bg-light').removeClass('bg-light').addClass('bg-dark')
        $('.bg-white').removeClass('bg-white').addClass('bg-dark')
        $('img[src="/static/img/faces.svg"]').attr('src', '/static/img/faces_dark.svg')

    }
}
updateTheme();
