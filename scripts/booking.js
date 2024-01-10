const servicePrices = {
    "wig_fixing": {
        "name": "Wig Fixing",
        "price": "100"
    },
    "wig_sewing": {
        "name": "Wig Sewing",
        "price": "100"
    },
    "braides": {
        "name": "Braides",
        "price": "100"
    },
    "bridal_styling": {
        "name": "Bridal Styling",
        "price": "100"
    },
    "hair_coloring": {
        "name": "Hair Coloring",
        "price": "100"
    },
}

const state = {
    "regular": "0.00",
    "express": "100.00"
}

const service = document.querySelector("#service");
const stateRadios = document.querySelectorAll('input[name="state"]');

const bookBtn = document.querySelector("#book_btn");

const price = document.querySelector("#price");

stateRadios.forEach(radio => {
    radio.addEventListener("change", function () {
        selectedService = service.value
        const serviceName = servicePrices[selectedService].name;
        const servicePrice = servicePrices[selectedService].price;
        if (radio.checked) {
            statePrice = state[radio.value]
            price.value = ""; //refresh
            price.value = `
            ${serviceName} GHC${servicePrice}
            Charges GHC${statePrice}
            `
        }
    });
});
