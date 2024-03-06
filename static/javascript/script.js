setTimeout(() => {
    const element = document.querySelector(".message"); 
    document.querySelector("#messages").removeChild(element);
}, 5000);

const foodNames = document.querySelectorAll(".food-name");
const foodPrices = document.querySelectorAll(".food-price");
const foodButtons = document.querySelectorAll(".food-button");

foodButtons.forEach(button => {
    button.addEventListener("click", addFood);
});

document.querySelector("table").addEventListener("click", removeFood);

function addFood(e) {
    let row = document.createElement("tr");
    row.innerHTML = `
        <td class="name">${e.target.parentElement.querySelector("h4").innerText}</td>
        <td class="price"><span>${e.target.parentElement.querySelector("div span").innerText}</span>.00 den</td>
        <td class="remove"><button>Remove</button></td>
    `;
    document.querySelector("table").appendChild(row);
    e.target.disabled = true;
    updatePrice(e.target.parentElement.querySelector("div span").innerText, "+");
}

function removeFood(e) {
    if (e.target.parentElement.className == "remove") {
        e.target.parentNode.parentNode.remove();
        document.querySelector(`.${e.target.parentNode.parentNode.firstElementChild.innerText}`).disabled = false;
        updatePrice(e.target.parentElement.parentElement.querySelector(".price span").innerText, "-");
    }
}

function updatePrice(price, op) {
    let totalPrice = document.querySelector("#total-price span");
    if (op == "+") {
        totalPrice.innerText = Number(price) + Number(totalPrice.innerText);
    } else {
        totalPrice.innerText = Number(totalPrice.innerText) - Number(price);
    }
}