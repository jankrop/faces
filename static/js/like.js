function mark_like(response, locator) {
    const likes = $('#likes-' + locator);
    const star = $('#star-' + locator);
    if (response.actionType == 'like') {
        likes.html(parseInt(likes.html()) + 1)
        star.html('<i class="bi bi-star-fill"></i>')
    } else if (response.actionType == 'dislike') {
        likes.html(parseInt(likes.html()) - 1)
        star.html('<i class="bi bi-star"></i>')
    }
}

class Like {
    constructor(username, id) {
        this.username = username;
        this.id = id;
    }

    like() {
        $.ajax({
            // I had to hardcode the URL to pass the arguments
            // I really want to follow DRY, so I made the Like class
            url: "/@" + this.username + '/' + this.id + '/like',
            success: (response) => {
                const locator = this.username + '-' + this.id;
                mark_like(response, locator);
            },
            error: (response) => {
                console.error('An error occurred while sending the like.')
            }
        })
    }
}

class CommentLike {
    constructor(username, post, id) {
        this.username = username;
        this.post = post;
        this.id = id;
    }

    like() {
        $.ajax({
            url: "/@" + this.username + '/' + this.post + '/' + this.id + '/like',
            success: (response) => {
                const locator = this.username + '-' + this.post + '-' + this.id;
                mark_like(response, locator);
            },
            error: (response) => {
                console.error('An error occurred while sending the like.')
            }
        })
    }
}
