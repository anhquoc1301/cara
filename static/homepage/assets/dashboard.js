
// const dashboardSlug = document.getElementById('dashboard-slug').textContent.trim()
// const user = document.getElementById('user').textContent.trim()
// const submitBtn = document.getElementById('submit-btn')
// const dataInput = document.getElementById('data-input')
// const dataBox = document.getElementById('data-box')

const socket = new WebSocket(`ws://${window.location.host}/ws/main/`)
console.log(socket)

// socket.onmessage = function(e) {
//                   const {sender, message} = JSON.parse(e.data)
//                   dataBox.innerHTML += `<p>${sender}: ${message}</p>`          
// };
socket.onmessage = function(e) {
                  let data = JSON.parse(e.data)
                  console.log('checkkk')
                  console.log('Data:', data)
};

// submitBtn.addEventListener('click', ()=>{
//                   const dataValue = dataInput.value
//                   socket.send(JSON.stringify({
//                                     'message': dataValue,
//                                     'sender': user
//                   }));
// })

// const ctx = document.getElementById('myChart').getContext("2d");
// let chart

// const fetchChartData = async() =>{
//                   const response = await fetch(window.location.href + 'chart/')
//                   const data = await response.json()
//                   console.log(data)
//                   return data
// }

// const drawChart = async() => {
//                   const data = await fetchChartData()
//                   const {chartData, chartLabels} = data

//                   chart = new Chart(ctx, {
//                                     type:'pie',
//                                     data: {
//                                                       labels: chartLabels,
//                                                       datasets:[{
//                                                                         label: '% of contribution',
//                                                                         data: chartData,
//                                                                         borderWidth: 1
//                                                       }]

//                                     },
//                                     option:{
//                                                       scales:{
//                                                                         y:{
//                                                                                           beginAtZero: true
//                                                                         }
//                                                       }
//                                     }
//                   });
// }
// const updateChart = async() =>{
//                   if (chart){
//                                     chart.destroy()
//                   }

//                   await drawChart()
// }
