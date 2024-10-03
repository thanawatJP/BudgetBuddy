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

// start: Popper
const popperInstance = {}
document.querySelectorAll('.dropdown').forEach(function (item, index) {
    const popperId = 'popper-' + index
    const toggle = item.querySelector('.dropdown-toggle')
    const menu = item.querySelector('.dropdown-menu')
    menu.dataset.popperId = popperId
    popperInstance[popperId] = Popper.createPopper(toggle, menu, {
        modifiers: [
            {
                name: 'offset',
                options: {
                    offset: [0, 8],
                },
            },
            {
                name: 'preventOverflow',
                options: {
                    padding: 24,
                },
            },
        ],
        placement: 'bottom-end'
    });
})
document.addEventListener('click', function (e) {
    const toggle = e.target.closest('.dropdown-toggle')
    const menu = e.target.closest('.dropdown-menu')
    if (toggle) {
        const menuEl = toggle.closest('.dropdown').querySelector('.dropdown-menu')
        const popperId = menuEl.dataset.popperId
        if (menuEl.classList.contains('hidden')) {
            hideDropdown()
            menuEl.classList.remove('hidden')
            showPopper(popperId)
        } else {
            menuEl.classList.add('hidden')
            hidePopper(popperId)
        }
    } else if (!menu) {
        hideDropdown()
    }
})

function hideDropdown() {
    document.querySelectorAll('.dropdown-menu').forEach(function (item) {
        item.classList.add('hidden')
    })
}
function showPopper(popperId) {
    popperInstance[popperId].setOptions(function (options) {
        return {
            ...options,
            modifiers: [
                ...options.modifiers,
                { name: 'eventListeners', enabled: true },
            ],
        }
    });
    popperInstance[popperId].update();
}
function hidePopper(popperId) {
    popperInstance[popperId].setOptions(function (options) {
        return {
            ...options,
            modifiers: [
                ...options.modifiers,
                { name: 'eventListeners', enabled: false },
            ],
        }
    });
}
// end: Popper