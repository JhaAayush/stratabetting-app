// Custom JavaScript for Stratabetting

document.addEventListener('DOMContentLoaded', function () {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Auto-dismiss alerts after 5 seconds
    setTimeout(function () {
        var alerts = document.querySelectorAll('.alert');
        alerts.forEach(function (alert) {
            var bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);

    // Form validation
    initializeFormValidation();

    // Betting calculations
    initializeBettingCalculations();

    // Real-time updates
    initializeRealTimeUpdates();
});

function initializeFormValidation() {
    const forms = document.querySelectorAll('form');

    forms.forEach(form => {
        form.addEventListener('submit', function (event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }

            form.classList.add('was-validated');
        });
    });
}

function initializeBettingCalculations() {
    const amountInputs = document.querySelectorAll('input[name="amount"]');
    const optionInputs = document.querySelectorAll('input[name="option"]');

    amountInputs.forEach(amountInput => {
        amountInput.addEventListener('input', updatePotentialWinnings);
    });

    optionInputs.forEach(optionInput => {
        optionInput.addEventListener('change', updatePotentialWinnings);
    });
}

function updatePotentialWinnings() {
    const amountInput = document.querySelector('input[name="amount"]');
    const selectedOption = document.querySelector('input[name="option"]:checked');

    if (!amountInput || !selectedOption) return;

    const amount = parseInt(amountInput.value) || 0;
    const optionText = selectedOption.value;

    // Find the odds for the selected option
    const oddsElements = document.querySelectorAll('.odds-badge');
    let odds = 1;

    oddsElements.forEach(el => {
        const optionElement = el.closest('.option-item').querySelector('input[name="option"]');
        if (optionElement && optionElement.value === optionText) {
            odds = parseFloat(el.textContent);
        }
    });

    const winnings = Math.floor(amount * odds);

    // Update or create winnings display
    let winningsDisplay = document.getElementById('potential-winnings');
    if (!winningsDisplay) {
        winningsDisplay = document.createElement('div');
        winningsDisplay.id = 'potential-winnings';
        winningsDisplay.className = 'alert alert-info mt-3';
        amountInput.closest('.mb-3').appendChild(winningsDisplay);
    }

    if (amount > 0) {
        winningsDisplay.innerHTML = `
            <i class="fas fa-calculator"></i>
            <strong>Potential Winnings:</strong> ${winnings} coins (${odds}x odds)
        `;
        winningsDisplay.style.display = 'block';
    } else {
        winningsDisplay.style.display = 'none';
    }
}

function initializeRealTimeUpdates() {
    // Update balance display if user is logged in
    if (document.querySelector('.balance-amount')) {
        updateBalanceDisplay();
    }
}

function updateBalanceDisplay() {
    // This would typically make an AJAX call to get updated balance
    // For now, we'll just ensure the display is current
    const balanceElement = document.querySelector('.balance-amount');
    if (balanceElement) {
        // Add a subtle animation when balance changes
        balanceElement.style.transition = 'color 0.3s ease';
        setTimeout(() => {
            balanceElement.style.color = '';
        }, 100);
    }
}

// Utility functions
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-IN', {
        style: 'currency',
        currency: 'INR',
        minimumFractionDigits: 0
    }).format(amount);
}

function formatNumber(num) {
    return new Intl.NumberFormat('en-IN').format(num);
}

// AJAX helper functions
function makeRequest(url, method = 'GET', data = null) {
    return fetch(url, {
        method: method,
        headers: {
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest'
        },
        body: data ? JSON.stringify(data) : null
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        });
}

// Betting specific functions
function placeBet(questionId, option, amount) {
    const formData = new FormData();
    formData.append('option', option);
    formData.append('amount', amount);

    return fetch(`/student/bet/${questionId}`, {
        method: 'POST',
        body: formData
    })
        .then(response => response.text())
        .then(html => {
            // Handle response
            if (response.ok) {
                showNotification('Bet placed successfully!', 'success');
                // Redirect or update page
                window.location.reload();
            } else {
                showNotification('Failed to place bet. Please try again.', 'error');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showNotification('An error occurred. Please try again.', 'error');
        });
}

function toggleQuestionStatus(questionId) {
    return makeRequest(`/admin/question/${questionId}/toggle`, 'POST')
        .then(data => {
            showNotification('Question status updated', 'success');
            window.location.reload();
        })
        .catch(error => {
            console.error('Error:', error);
            showNotification('Failed to update question status', 'error');
        });
}

function settleBet(betId, isWinner) {
    const formData = new FormData();
    formData.append('is_winner', isWinner);

    return fetch(`/admin/settle_bet/${betId}`, {
        method: 'POST',
        body: formData
    })
        .then(response => response.text())
        .then(html => {
            showNotification('Bet settled successfully!', 'success');
            window.location.reload();
        })
        .catch(error => {
            console.error('Error:', error);
            showNotification('Failed to settle bet', 'error');
        });
}

// Notification system
function showNotification(message, type = 'info') {
    const alertClass = {
        'success': 'alert-success',
        'error': 'alert-danger',
        'warning': 'alert-warning',
        'info': 'alert-info'
    }[type] || 'alert-info';

    const notification = document.createElement('div');
    notification.className = `alert ${alertClass} alert-dismissible fade show position-fixed`;
    notification.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;

    document.body.appendChild(notification);

    // Auto-remove after 5 seconds
    setTimeout(() => {
        if (notification.parentNode) {
            notification.parentNode.removeChild(notification);
        }
    }, 5000);
}

// Loading states
function showLoading(element) {
    element.innerHTML = '<span class="loading"></span> Loading...';
    element.disabled = true;
}

function hideLoading(element, originalText) {
    element.innerHTML = originalText;
    element.disabled = false;
}

// Export functions
function exportToCSV(data, filename) {
    const csv = convertToCSV(data);
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.setAttribute('hidden', '');
    a.setAttribute('href', url);
    a.setAttribute('download', filename);
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
}

function convertToCSV(data) {
    if (!data || data.length === 0) return '';

    const headers = Object.keys(data[0]);
    const csvContent = [
        headers.join(','),
        ...data.map(row => headers.map(header => `"${row[header] || ''}"`).join(','))
    ].join('\n');

    return csvContent;
}

// Team selection helpers
function updateTeamStats(teamName) {
    // This would fetch and display team statistics
    console.log('Updating stats for team:', teamName);
}

// Search and filter functions
function filterEvents(searchTerm) {
    const events = document.querySelectorAll('.event-card');
    events.forEach(event => {
        const text = event.textContent.toLowerCase();
        const matches = text.includes(searchTerm.toLowerCase());
        event.style.display = matches ? 'block' : 'none';
    });
}

function sortBetsByDate() {
    const bets = document.querySelectorAll('.bet-item');
    const sortedBets = Array.from(bets).sort((a, b) => {
        const dateA = new Date(a.querySelector('.date')?.textContent || 0);
        const dateB = new Date(b.querySelector('.date')?.textContent || 0);
        return dateB - dateA;
    });

    const container = bets[0]?.parentNode;
    if (container) {
        sortedBets.forEach(bet => container.appendChild(bet));
    }
}

// Initialize any additional features
function initializeAdvancedFeatures() {
    // Add keyboard shortcuts
    document.addEventListener('keydown', function (e) {
        // Ctrl/Cmd + Enter to submit forms
        if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
            const form = e.target.closest('form');
            if (form) {
                form.submit();
            }
        }
    });

    // Add smooth scrolling
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// Initialize everything when DOM is ready
document.addEventListener('DOMContentLoaded', initializeAdvancedFeatures);
