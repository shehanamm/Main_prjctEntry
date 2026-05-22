
function updateCartQty(button, amount) {
    // Locate the wrapper block and find the attached numerical field
    const wrapper = button.parentElement;
    const qtyInput = wrapper.querySelector('.input-quantity-field');
    
    // Parse the current number safely, fallback to 1 if it breaks
    let currentQty = parseInt(qtyInput.value) || 1;
    
    // Process calculation
    let newQty = currentQty + amount;
    
    // Strict guardrail: Prevent submission if user drops below 1
    if (newQty >= 1) {
        qtyInput.value = newQty;
        // Submits the individual form row data instantly to Django
        wrapper.parentElement.submit();
    }
}