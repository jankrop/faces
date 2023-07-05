class Like {
    constructor(username, id) {
        this.username = username
        this.id = id;
    }

    like() {
        $.ajax({
            // I had to hardcode the URL to pass the arguments
            // I really want to follow DRY, so I made the Like class
            url: "/@" + this.username + '/' + this.id + '/like',
            success: (response) => {
                const likes = $('#likes-' + this.username + '-' + this.id)
                if (response.actionType == 'like') {
                    likes.html(parseInt(likes.html()) + 1)
                    $('#like-' + this.username + '-' + this.id).html('Liked!')
                } else if (response.actionType == 'dislike') {
                    likes.html(parseInt(likes.html()) - 1)
                    $('#like-' + this.username + '-' + this.id).html('Like')
                }
            },
            error: (response) => {
                console.error('An error occurred while sending the like.')
            }
        })
    }
}