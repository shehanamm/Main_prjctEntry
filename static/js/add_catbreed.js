const category = document.getElementById("category");
const breed = document.getElementById("breed");


// Store all breed options
const allBreeds = Array.from(breed.options);


category.addEventListener("change", function () {

    let categoryId = this.value;

    // Clear dropdown
    breed.innerHTML = '<option value="">Select Breed</option>';

    // Filter breeds
    allBreeds.forEach(function(option) {

        let breedCategory = option.getAttribute("data-category");

        if (breedCategory === categoryId) {

            breed.appendChild(option);

        }

    });

});