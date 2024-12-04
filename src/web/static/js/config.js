// Save configuration
async function saveConfig() {
    const exchangeConfig = getFormData('exchangeConfig');
    const tradingConfig = getFormData('tradingConfig');
    const riskConfig = getFormData('riskConfig');

    const config = {
        ...exchangeConfig,
        ...tradingConfig,
        ...riskConfig
    };

    try {
        const response = await fetch('/api/config', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(config),
        });

        if (response.ok) {
            alert('Configuration saved successfully!');
            loadConfig();  // Reload config
        } else {
            alert('Error saving configuration');
        }
    } catch (error) {
        alert(`Error: ${error.message}`);
    }
}

// Load configuration
async function loadConfig() {
    try {
        const response = await fetch('/api/config');
        const config = await response.json();
        
        // Update form fields
        populateForm('exchangeConfig', config);
        populateForm('tradingConfig', config);
        populateForm('riskConfig', config);
    } catch (error) {
        console.error('Error loading configuration:', error);
    }
}

// Helper function to get form data
function getFormData(formId) {
    const form = document.getElementById(formId);
    const formData = new FormData(form);
    const data = {};
    
    for (let [key, value] of formData.entries()) {
        data[key] = value;
    }
    
    return data;
}

// Helper function to populate form
function populateForm(formId, data) {
    const form = document.getElementById(formId);
    
    for (let key in data) {
        const input = form.elements[key];
        if (input) {
            input.value = data[key];
        }
    }
}

// Initialize
document.addEventListener('DOMContentLoaded', loadConfig);
