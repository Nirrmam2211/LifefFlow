document.addEventListener('DOMContentLoaded', function() {
    // Helper to get session token (for context, not used in fetch)
    function getSessionToken() {
        // The fetch calls below will work because the browser automatically sends the session cookie.
        // This function is here for clarity if you were to build a pure Single-Page Application (SPA).
        return 'dummy-token-for-client-side-logic-if-needed';
    }

    // Fetch and display dashboard stats
    function fetchDashboardStats() {
        fetch('/api/dashboard/stats')
        .then(response => {
            // Check if the server response is not OK (e.g., 404, 500)
            if (!response.ok) {
                // If the user is not authorized, redirect them to the login page.
                if (response.status === 401) {
                    window.location.href = '/login';
                }
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            if (data.error) {
                console.error('Error fetching stats:', data.error);
                return;
            }
            // Update the dashboard cards with the fetched data safely
            const totalDonorsEl = document.getElementById('total-donors');
            if (totalDonorsEl) totalDonorsEl.textContent = data.total_donors ?? 0;
            
            const totalRecipientsEl = document.getElementById('total-recipients');
            if (totalRecipientsEl) totalRecipientsEl.textContent = data.total_recipients ?? 0;
            
            const unitsAvailableEl = document.getElementById('units-available');
            if (unitsAvailableEl) unitsAvailableEl.textContent = data.units_available ?? 0;
        })
        .catch(error => {
            console.error('Error fetching dashboard stats:', error);
        });
    }

    // Fetch and render blood stock chart
    function renderBloodStockChart() {
        const chartCanvas = document.getElementById('bloodStockChart');
        if (!chartCanvas) return; // Don't run if the canvas element isn't on the page
        const ctx = chartCanvas.getContext('2d');
        if (!ctx) return;

        fetch('/api/dashboard/blood_stock')
        .then(response => {
             if (!response.ok) {
                if (response.status === 401) {
                    window.location.href = '/login';
                }
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            if (data.error) {
                console.error('Error fetching stock data:', data.error);
                return;
            }

            const labels = data.map(item => item.blood_group);
            const values = data.map(item => item.total_units);

            new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'Units Available',
                        data: values,
                        backgroundColor: 'rgba(220, 38, 38, 0.6)',
                        borderColor: 'rgba(220, 38, 38, 1)',
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    },
                    plugins: {
                        legend: {
                            display: false
                        }
                    }
                }
            });
        })
        .catch(error => console.error('Error fetching blood stock data:', error));
    }
    
    // Only run these functions if we are on the admin dashboard page.
    if (document.getElementById('total-donors') || document.getElementById('bloodStockChart')) {
        fetchDashboardStats();
        renderBloodStockChart();
    }
});

