function deleteAccount(account_id, csrf_token) {
    // กำหนด path ให้ถูกต้อง
    fetch(`delete/${account_id}/`, {
        method: "DELETE",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrf_token,
        },
    })
        .then((data) => {
            console.log("Item deleted successfully");
            window.location.reload();
        })
        .catch((error) => console.error("Error:", error));
}

function closeMessage() {
    const messageDiv = document.getElementById('message-container');
    if (messageDiv) {
        messageDiv.style.display = 'none'; // ซ่อน div
    }
}