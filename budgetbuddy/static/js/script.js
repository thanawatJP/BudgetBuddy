function generateRandomData(n) {
    const data = [];
    for (let i = 0; i < n; i++) {
        const randomValue = Math.floor(Math.random() * (99999 - 10000 + 1)) + 10000;
        data.push(randomValue);
    }
    return data;
}

// เรียกใช้เมื่อคลิกปุ่มเพื่อเปิด/ปิด sidebar
document.querySelector('[data-drawer-toggle]').addEventListener('click', function() {
    const sidebar = document.getElementById('default-sidebar');
    sidebar.classList.toggle('-translate-x-full'); // ใช้ toggle เพื่อเลื่อน sidebar เข้า/ออก
});

// เรียกใช้เมื่อคลิกนอก sidebar
document.addEventListener('click', function(event) {
    const sidebar = document.getElementById('default-sidebar');
    const toggleButton = document.querySelector('[data-drawer-toggle]');

    // ตรวจสอบว่าไม่ได้คลิกที่ sidebar และไม่ได้คลิกที่ปุ่ม toggle
    if (!sidebar.contains(event.target) && !toggleButton.contains(event.target)) {
        // ถ้า sidebar ยังเปิดอยู่ ก็ปิด sidebar
        if (!sidebar.classList.contains('-translate-x-full')) {
            sidebar.classList.add('-translate-x-full');
        }
    }
});