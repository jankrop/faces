const button = '<button class="load-posts-button" onclick="getNextPosts()">More</button>'

function getFeed(start, count, target, addButton) {
    $.ajax({
        url: '/feed?start=' + start + '&end=' + (start + count),
        success: (response) => {
            const targetHandle = $(target);
            targetHandle.append(response);
            if (response) { targetHandle.append(button) }
        }
    })
}

const batchSize = 10;
let postsLoaded = 0;
function getNextPosts() {
    $('.load-posts-button').remove()
    getFeed(postsLoaded, batchSize, '#feed');
    postsLoaded += batchSize;
}
getNextPosts();
