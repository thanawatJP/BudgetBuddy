function deleteTransaction(transaction_id, csrf_token) {
    // กำหนด path ให้ถูกต้อง
    fetch(`delete/${transaction_id}/`, {
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

