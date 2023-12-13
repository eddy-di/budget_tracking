const ctx = document.getElementById('myChart');
  
    new Chart(ctx, {
      type: 'doughnut',
      data: {
        labels: ['Expense', 'Income'],
        datasets: [{
          label: 'Total sum',
          data: {{ data|safe }},
          borderWidth: 1,
          backgroundColor: ['#FF6384', '#36A2EB'],
          hoverBackgroundColor: ['#F54165', '#1D97E9'],
        }]
      },
      options: {
        plugins: {
          legend: {
            position: 'bottom'
          }
        }
      }
    });