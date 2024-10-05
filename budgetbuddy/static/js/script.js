//start: sidebar
// document.querySelectorAll('.sidebar-dropdown').forEach(function(item){
    
// })
//end: sidebar

// new Chart(document.getElementById('doughnut-chart'), {
//     type: 'doughnut',
//     data: {
//         labels: ['Income', 'Expense'], // ระบุชื่อข้อมูล
//         datasets: [{
//             data: [179200, 128500], // ข้อมูลของ Income และ Expense
//             backgroundColor: ['rgb(34, 197, 94)', 'rgb(244, 63, 94)'], // สีเขียวสำหรับ Income, สีแดงสำหรับ Expense
//             borderColor: ['rgb(34, 197, 94)', 'rgb(244, 63, 94)'], // สีขอบ
//             borderWidth: 1 // ความกว้างของเส้นขอบ
//         }]
//     },
//     options: {
//         responsive: true, // ทำให้กราฟตอบสนองต่อขนาดหน้าจอ
//         plugins: {
//             legend: {
//                 position: 'top', // กำหนดตำแหน่งของตำนาน (legend)
//             },
//             tooltip: {
//                 enabled: true, // เปิดการแสดง tooltip เมื่อ hover บนชิ้นกราฟ
//             }
//         }
//     }
// });

// new Chart(document.getElementById('order-chart'), {
//     type: 'line',
//     data: {
//         labels: generateNMonths(7),
//         datasets: [
//             {
//                 label: 'Income',
//                 data: generateRandomData(7),
//                 borderWidth: 1,
//                 fill: true,
//                 pointBackgroundColor: 'rgb(34, 197, 94)',
//                 borderColor: 'rgb(34, 197, 94)',
//                 backgroundColor: 'rgba(34, 197, 94, 0.1)',
//                 tension: .2
//             },
//             {
//                 label: 'Expense',
//                 data: generateRandomData(7),
//                 borderWidth: 1,
//                 fill: true,
//                 pointBackgroundColor: 'rgb(255, 99, 132)',
//                 borderColor: 'rgb(255, 99, 132)',    
//                 backgroundColor: 'rgba(255, 99, 132, 0.1)',
//                 tension: .2
//             }
//         ]
//     },
//     options: {
//         scales: {
//             y: {
//                 beginAtZero: true
//             }
//         }
//     }
// });

function generateRandomData(n) {
    const data = [];
    for (let i = 0; i < n; i++) {
        const randomValue = Math.floor(Math.random() * (99999 - 10000 + 1)) + 10000;
        data.push(randomValue);
    }
    return data;
}

// // start: Popper
// ย้ายไป popperScript.js
// // end: Popper