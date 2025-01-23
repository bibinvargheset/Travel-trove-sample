// Function to upvote a post
function upvote(button) {
    button.style.backgroundColor = '#d77a61'; // Change color to indicate upvote
    button.innerText = 'Upvoted';
}

// Function to downvote a post
function downvote(button) {
    button.style.backgroundColor = '#dbd3d8'; // Change color to indicate downvote
    button.innerText = 'Downvoted';
}

// Function to share a link
function shareLink(button) {
    const postLink = window.location.href; // Get current URL
    navigator.clipboard.writeText(postLink).then(() => {
        alert('Link copied to clipboard!');
    });
}

// Function to show reply section
function replyToPost(button) {
    const replySection = button.parentElement.nextElementSibling;
    replySection.style.display = replySection.style.display === 'none' ? 'block' : 'none';
}

// Function to handle new forum post submission
function postNewTopic() {
    // Logic to submit a new topic (placeholder)
    alert('New topic posted!');
}

// Function to submit a reply
function submitReply(button) {
    const replyText = button.previousElementSibling.value;
    if (replyText) {
        // Logic to handle reply submission (placeholder)
        alert('Reply submitted: ' + replyText);
    }
}
// Function to update profile image
function updateProfileImage(input) {
    const imgElement = document.getElementById("profile-img");
    const file = input.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function (e) {
            imgElement.src = e.target.result;
        }
        reader.readAsDataURL(file);
    }
}

// Function to edit user profile
function editProfile() {

    alert("Edit profile functionality to be implemented!");
}

// Function to update bio in real-time
function updateBio(bio) {
    // In a real application, you would save this data to a database or API
    console.log("Bio updated:", bio);
}

// Function to update preferences in real-time
function updatePreferences(preferenceElement) {
    const updatedPreference = preferenceElement.innerText;
    // In a real application, you would save this data to a database or API
    console.log("Preference updated:", updatedPreference);
}