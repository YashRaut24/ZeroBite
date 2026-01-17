// State management
let ingredients = [];
let pantryItems = [];
const API_URL = 'http://127.0.0.1:8000/plan'; // Use 127.0.0.1 instead of localhost

// Add ingredient
function addIngredient() {
    const name = document.getElementById('ingredientName').value.trim();
    const expiryDays = parseInt(document.getElementById('expiryDays').value);

    // Validation
    if (!name) {
        showError('Please enter an ingredient name');
        return;
    }

    if (isNaN(expiryDays) || expiryDays < 0) {
        showError('Please enter a valid number of days');
        return;
    }

    // Add to state
    ingredients.push({ name, expiry_days: expiryDays });

    // Clear inputs
    document.getElementById('ingredientName').value = '';
    document.getElementById('expiryDays').value = '';

    // Render list
    renderIngredients();
    clearError();
}

// Add pantry item
function addPantryItem() {
    const item = document.getElementById('pantryItem').value.trim();

    // Validation
    if (!item) {
        showError('Please enter a pantry item');
        return;
    }

    // Add to state
    pantryItems.push(item);

    // Clear input
    document.getElementById('pantryItem').value = '';

    // Render list
    renderPantry();
    clearError();
}

// Render ingredients list
function renderIngredients() {
    const listDiv = document.getElementById('ingredientsList');

    if (ingredients.length === 0) {
        listDiv.innerHTML = '<div class="empty-message">No ingredients added yet</div>';
        return;
    }

    listDiv.innerHTML = ingredients
        .map((ing, index) => `
            <div class="item">
                <div class="item-text">
                    <div class="item-name">${escapeHtml(ing.name)}</div>
                    <div class="item-subtext">Expires in ${ing.expiry_days} day(s)</div>
                </div>
                <button class="item-remove" onclick="removeIngredient(${index})">Remove</button>
            </div>
        `)
        .join('');
}

// Render pantry list
function renderPantry() {
    const listDiv = document.getElementById('pantryList');

    if (pantryItems.length === 0) {
        listDiv.innerHTML = '<div class="empty-message">No pantry items added yet</div>';
        return;
    }

    listDiv.innerHTML = pantryItems
        .map((item, index) => `
            <div class="item">
                <div class="item-text">
                    <div class="item-name">${escapeHtml(item)}</div>
                </div>
                <button class="item-remove" onclick="removePantryItem(${index})">Remove</button>
            </div>
        `)
        .join('');
}

// Remove ingredient
function removeIngredient(index) {
    ingredients.splice(index, 1);
    renderIngredients();
}

// Remove pantry item
function removePantryItem(index) {
    pantryItems.splice(index, 1);
    renderPantry();
}

// Generate plan
async function generatePlan() {
    // Validation
    if (ingredients.length === 0) {
        showError('Please add at least one ingredient');
        return;
    }

    if (pantryItems.length === 0) {
        showError('Please add at least one pantry item');
        return;
    }

    // Hide previous results
    document.getElementById('results').classList.add('hidden');

    // Show loading
    document.getElementById('loading').classList.remove('hidden');
    document.getElementById('generateBtn').disabled = true;
    clearError();

    try {
        // Prepare payload
        const payload = {
            ingredients: ingredients,
            pantry: pantryItems
        };

        // API call
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });

        // Handle response
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'API request failed');
        }

        const result = await response.json();

        // Display results
        displayResults(result);

        // Hide loading
        document.getElementById('loading').classList.add('hidden');
        document.getElementById('generateBtn').disabled = false;

    } catch (error) {
        console.error('Error:', error);
        showError(`Error: ${error.message}`);
        document.getElementById('loading').classList.add('hidden');
        document.getElementById('generateBtn').disabled = false;
    }
}

// Display results
function displayResults(data) {
    // Show results section
    document.getElementById('results').classList.remove('hidden');

    // Set content
    document.getElementById('expiryAnalysis').textContent = data.expiry_analysis || 'No analysis available';
    document.getElementById('mealPlan').textContent = data.meal_plan || 'No meal plan available';
    document.getElementById('auditReport').textContent = data.audit_report || 'No audit report available';

    // Scroll to results
    setTimeout(() => {
        document.getElementById('results').scrollIntoView({ behavior: 'smooth' });
    }, 100);
}

// Reset plan
function resetPlan() {
    ingredients = [];
    pantryItems = [];
    document.getElementById('ingredientName').value = '';
    document.getElementById('expiryDays').value = '';
    document.getElementById('pantryItem').value = '';
    document.getElementById('results').classList.add('hidden');
    renderIngredients();
    renderPantry();
    clearError();
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// Error handling
function showError(message) {
    const errorDiv = document.getElementById('error');
    errorDiv.textContent = message;
    errorDiv.classList.remove('hidden');
}

function clearError() {
    const errorDiv = document.getElementById('error');
    errorDiv.classList.add('hidden');
    errorDiv.textContent = '';
}

// Escape HTML to prevent XSS
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Allow Enter key to add items
document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('ingredientName').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') addIngredient();
    });

    document.getElementById('expiryDays').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') addIngredient();
    });

    document.getElementById('pantryItem').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') addPantryItem();
    });

    // Initial render
    renderIngredients();
    renderPantry();
});
