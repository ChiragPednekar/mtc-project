// Setup Charts
Chart.defaults.color = '#94a3b8';
Chart.defaults.font.family = 'Inter';

const commonOptions = {
    responsive: true,
    maintainAspectRatio: false,
    animation: {
        duration: 0 // turn off animation for smooth real-time sliding
    },
    scales: {
        x: {
            grid: { color: 'rgba(255, 255, 255, 0.05)' },
            title: { display: true, text: 'Time (s)', color: '#94a3b8' }
        },
        y: {
            grid: { color: 'rgba(255, 255, 255, 0.05)' },
            title: { display: true, text: 'Amplitude', color: '#94a3b8' },
            suggestedMin: -5,
            suggestedMax: 5
        }
    },
    plugins: {
        legend: {
            labels: { color: '#f8fafc', font: { weight: '600', size: 13 } }
        }
    },
    elements: {
        line: { tension: 0.1 } // Slight curve for aesthetics
    }
};

const ctx1 = document.getElementById('signalsChart').getContext('2d');
const signalsChart = new Chart(ctx1, {
    type: 'line',
    data: {
        labels: [],
        datasets: [
            {
                label: 'Signal x (Base)',
                borderColor: '#3b82f6',
                backgroundColor: 'rgba(59, 130, 246, 0.1)',
                borderWidth: 2,
                pointRadius: 0,
                data: [],
                fill: true
            },
            {
                label: 'Signal y (Target)',
                borderColor: '#ec4899',
                backgroundColor: 'rgba(236, 72, 153, 0.1)',
                borderWidth: 2,
                pointRadius: 0,
                data: [],
                fill: true
            }
        ]
    },
    options: { ...commonOptions, plugins: { ...commonOptions.plugins, title: { display: true, text: 'Signal Vectors: x and y', color: '#fff', font: { size: 16 } } } }
});

const ctx2 = document.getElementById('projectionChart').getContext('2d');
const projectionChart = new Chart(ctx2, {
    type: 'line',
    data: {
        labels: [],
        datasets: [
            {
                label: 'Proj_y(x) -> Component of x along y',
                borderColor: '#10b981',
                backgroundColor: 'rgba(16, 185, 129, 0.2)',
                borderWidth: 3,
                pointRadius: 0,
                data: [],
                fill: true
            }
        ]
    },
    options: { ...commonOptions, plugins: { ...commonOptions.plugins, title: { display: true, text: 'Orthogonal Projection Result', color: '#fff', font: { size: 16 } } } }
});

// UI Event Listeners
const inputs = ['type1', 'freq1', 'amp1', 'type2', 'freq2', 'amp2', 'noise'];

inputs.forEach(id => {
    const el = document.getElementById(id);
    el.addEventListener('input', (e) => {
        // Update labels instantly
        if(id === 'freq1' || id === 'amp1' || id === 'freq2' || id === 'amp2' || id === 'noise') {
            const valEl = document.getElementById(`${id}-val`);
            if(id === 'noise' && el.value == 0) {
                valEl.innerText = 'Off';
            } else {
                valEl.innerText = parseFloat(el.value).toFixed(1);
            }
        }
        fetchData();
    });
});

async function fetchData() {
    const payload = {
        type1: document.getElementById('type1').value,
        freq1: parseFloat(document.getElementById('freq1').value),
        amp1: parseFloat(document.getElementById('amp1').value),
        type2: document.getElementById('type2').value,
        freq2: parseFloat(document.getElementById('freq2').value),
        amp2: parseFloat(document.getElementById('amp2').value),
        noise_level: parseFloat(document.getElementById('noise').value),
        duration: 1.0,
        sampling_rate: 400
    };

    try {
        const res = await fetch('/api/analyze', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        
        const data = await res.json();
        
        // Update Metrics
        document.getElementById('val-dot').innerText = data.metrics.dot_product.toFixed(3);
        document.getElementById('val-norm1').innerText = data.metrics.norm_sig1.toFixed(3);
        document.getElementById('val-norm2').innerText = data.metrics.norm_sig2.toFixed(3);
        
        const orthoBadge = document.getElementById('val-ortho');
        if (data.metrics.is_orthogonal) {
            orthoBadge.innerText = 'Orthogonal';
            orthoBadge.className = 'ortho-badge ortho-true';
        } else {
            orthoBadge.innerText = 'Not Orthogonal';
            orthoBadge.className = 'ortho-badge ortho-false';
        }

        // Update Charts
        signalsChart.data.labels = data.time.map(t => t.toFixed(3));
        signalsChart.data.datasets[0].data = data.signal1;
        signalsChart.data.datasets[1].data = data.signal2;
        signalsChart.update();

        projectionChart.data.labels = data.time.map(t => t.toFixed(3));
        projectionChart.data.datasets[0].data = data.projection;
        projectionChart.update();

    } catch (err) {
        console.error("Error fetching data:", err);
    }
}

// Initial fetch
fetchData();
