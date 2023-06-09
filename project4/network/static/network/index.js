document.addEventListener('DOMContentLoaded', () => {

    // Toggle menu
    document.querySelector("#menu").addEventListener('click', () => toggle_menu());

    // Load all posts
    window.onload = () => {
        if (window.location.pathname === '/') {
            load_all_posts();
        }
    };
});

function toggle_menu() {

    console.log("Toggled menu")

    const userInfo = document.querySelector('#user-info');
    const networkContent = document.querySelector("#network-content")
    if (userInfo.style.display === '' || userInfo.style.display === 'block'){
        console.log("Unactivated menu")
        userInfo.style.display = 'none';
        networkContent.classList.remove('col-sm-9');
        networkContent.classList.add('col-sm-12');
    } else {
        console.log("Activated menu")
        userInfo.style.display = 'block';
        networkContent.classList.remove('col-sm-12');
        networkContent.classList.add('col-sm-9');
    }

}

function load_all_posts(page_number=1, posts_per_page=10, specification='all', user_id=null) {

    console.log(`Loading ${posts_per_page} posts to page ${page_number}...`);

    const data = {
        page_number: page_number,
        posts_per_page: posts_per_page,
        specification: specification,
        user_id: user_id
    };

    fetch('/posts-page', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        // Handle the JSON response
        console.log(data);
    })
    .catch(error => {
        // Handle any errors
        console.error('Error:', error);
    });

}