$(document).ready(function() {
    // Function to get CSRF token
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // CSRF token
    var csrftoken = getCookie('csrftoken');

    // Event listener for like button click
    $('.like-btn').click(function(e) {
        e.preventDefault();
        var postId = $(this).data('post-id');
        var likeButton = $(this); // Store reference to the clicked button
        $.ajax({
            type: 'POST',
            url: '/like/' + postId + '/',
            data: {
                'csrfmiddlewaretoken': csrftoken
            },
            success: function(response) {
                if (response.success) {
                    // Update UI to reflect that the post was liked
                    var action = response.action;
                    var likeCount = parseInt(likeButton.find('span').text()); // Use the stored reference
                    if (action === 'like') {
                        likeCount += 1;
                    } else if (action === 'unlike') {
                        likeCount -= 1;
                    }
                    likeButton.find('span').text(likeCount);
                }
            }
        });
    });

    // Event listener for dislike button click
    $('.dislike-btn').click(function(e) {
        e.preventDefault();
        var postId = $(this).data('post-id');
        var dislikeButton = $(this); // Store reference to the clicked button
        $.ajax({
            type: 'POST',
            url: '/dislike/' + postId + '/',
            data: {
                'csrfmiddlewaretoken': csrftoken
            },
            success: function(response) {
                if (response.success) {
                    // Update UI to reflect that the post was disliked
                    var action = response.action;
                    var dislikeCount = parseInt(dislikeButton.find('span').text()); // Use the stored reference
                    if (action === 'dislike') {
                        dislikeCount += 1;
                    } else if (action === 'undislike') {
                        dislikeCount -= 1;
                    }
                    dislikeButton.find('span').text(dislikeCount);
                }
            }
        });
    });
});
