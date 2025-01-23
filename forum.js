document.addEventListener("DOMContentLoaded", () => {
    const forumPostsContainer = document.getElementById("forumPosts");
    const postPopup = document.getElementById("postPopup");
    const openPostButton = document.getElementById("openPostButton");
    const closePostButton = document.getElementById("closePostButton");
    const postForm = document.getElementById("postForm");
    const postTemplate = document.getElementById("postTemplate");
    if (!postTemplate || !('content' in document.createElement('template'))) {
        console.error("Your browser doesn't support HTML template elements.");
        return;
    }
    const categoryFilter = document.getElementById("categoryFilter");
    const sortOrder = document.getElementById("sortOrder");

    const API_BASE_URL = "http://localhost:5000"; // Update with your backend URL

    // Fetch all posts from the backend
    async function fetchPosts() {
        try {
            const response = await fetch(`${API_BASE_URL}/posts`);
            const posts = await response.json();

            // Clear existing posts
            forumPostsContainer.innerHTML = "";

            // Render posts
            posts.forEach(renderPost);
        } catch (error) {
            console.error("Error fetching posts:", error);
        }
    }

    // Render a single post using the template
    function renderPost(post) {
        const postElement = postTemplate.content.cloneNode(true);
        const postContainer = postElement.querySelector(".post");

        postContainer.setAttribute("data-post-id", post._id || "");

        postElement.querySelector(".post-title").textContent = post.title;
        postElement.querySelector(".post-content").textContent = post.content;
        postElement.querySelector(".post-tags").textContent = post.tags ? post.tags.join(", ") : "";

        const mediaContainer = postElement.querySelector(".post-media");
        if (post.image_url) {
            const img = document.createElement("img");
            img.src = post.image_url;
            img.alt = "Post Image";
            img.style.width = "100%";
            mediaContainer.appendChild(img);
        }
        if (post.video_url) {
            const video = document.createElement("video");
            video.src = post.video_url;
            video.controls = true;
            video.style.width = "100%";
            mediaContainer.appendChild(video);
        }

        forumPostsContainer.appendChild(postElement);
    }

    // Show the "Create New Post" popup
    openPostButton.addEventListener("click", () => {
        postPopup.style.display = "block";
    });

    // Close the "Create New Post" popup
    closePostButton.addEventListener("click", () => {
        postPopup.style.display = "none";
    });

        const formData = new FormData(postForm);
        if (!formData.has('title') || !formData.has('content')) {
            alert("Please fill in all required fields.");
            return;
        }
    postForm.addEventListener("submit", async (event) => {
        event.preventDefault();

        const formData = new FormData(postForm);

        try {
            const response = await fetch(`${API_BASE_URL}/add_post`, {
                method: "POST",
                body: formData,
            });

            if (response.ok) {
                alert("Post created successfully!");
                postPopup.style.display = "none";
                postForm.reset();
                fetchPosts(); // Reload posts
            } else {
                const errorData = await response.json();
                alert(`Error creating post: ${errorData.message}`);
            }
        } catch (error) {
            console.error("Error creating post:", error);
            alert("Failed to create post. Please try again.");
        }
    });

    // Filter posts by category
    categoryFilter.addEventListener("change", async () => {
        const selectedCategory = categoryFilter.value;
        const allPosts = await fetch(`${API_BASE_URL}/posts`).then((res) => res.json());

        const filteredPosts = selectedCategory
            ? allPosts.filter((post) => post.tags && post.tags.includes(selectedCategory))
            : allPosts;

        forumPostsContainer.innerHTML = "";
        filteredPosts.forEach(renderPost);
    });

    // Sort posts
    sortOrder.addEventListener("change", async () => {
        const selectedOrder = sortOrder.value;
        const allPosts = await fetch(`${API_BASE_URL}/posts`).then((res) => res.json());

        const sortedPosts = allPosts.sort((a, b) => {
            if (selectedOrder === "latest") {
                return new Date(b.created_at) - new Date(a.created_at);
            } else if (selectedOrder === "upvotes") {
                return (b.upvotes || 0) - (a.upvotes || 0);
            }
        });

        forumPostsContainer.innerHTML = "";
        sortedPosts.forEach(renderPost);
    });

    // Fetch initial posts
    fetchPosts();
});
