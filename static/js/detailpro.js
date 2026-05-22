 function showQuantityControls() {
    // Hide the initial "Add to Cart" button layout
    document.getElementById('initial-add-state').style.display = 'none';
    
    // Reveal the quantity buttons and confirm button
    document.getElementById('quantity-adjust-state').style.display = 'block';
}

function updateQuantity(amount) {
    const quantityInput = document.getElementById('quantity-field');
    let currentQty = parseInt(quantityInput.value) || 1;
    let newQty = currentQty + amount;
    
    // Allows increment and decrement, but prevents dropping below 1
    if (newQty >= 1) {
        quantityInput.value = newQty;
    }
}