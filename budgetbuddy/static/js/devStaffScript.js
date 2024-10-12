function addStaff(csrf_token){

    const user_id = document.getElementById('user-select').value;

    // กำหนด path ให้ถูกต้อง
    fetch(`add/${user_id}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrf_token
        },
    })
    .then(data => {
        console.log('Item updated successfully')
        window.location.reload()
    })
    .catch(error => console.error('Error:', error));
}

function deleteStaff(staff_id, csrf_token) {
    // กำหนด path ให้ถูกต้อง
    fetch(`delete/${staff_id}/`, {
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
