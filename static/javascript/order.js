class Food {
    constructor(name, price) {
        this.name = name;
        this.price = Number(price);
    }
}

const fullPrice = document.querySelector("#total-price span");

class UI {
    static addFood(food, target) {
        let row = document.createElement("tr");

        function createOptions() {
            let result = ``;
            for (let x = 1; x <= 15; x++) {
                result += `<option value="${x}">${x}</option>`;
            }
            return result;
        }

        row.innerHTML = `
            <td class="name">${food.name}</td>
            <td class="quantity">
                <select data-currentvalue="1">
                    ${createOptions()}
                </select>
            </td>
            <td class="price">
                <span>${food.price}</span>.00 den
            </td>
            <td class="remove">
                <button>Remove</button>
            </td>
        `;

        document.querySelector("table").appendChild(row);
        target.disabled = true;
        fullPrice.innerText = Number(fullPrice.innerText) + food.price; 
    }

    static removeFood(target) {
        if (target.parentElement.className == "remove") {
            target.parentElement.parentElement.remove();
            let price = target.parentElement.previousElementSibling.querySelector("span"),
            quantity = target.parentElement.parentElement.querySelector("select").value;
            fullPrice.innerText = Number(fullPrice.innerText) - Number(quantity) * Number(price.innerText);
            document.querySelector(`.${target.parentElement.parentElement.firstElementChild.innerText.split(" ")[0]}`).disabled = false;
        }
    }

    static updatePrice(target) {
        if (target.parentElement.className == "quantity") {
            let value = Number(target.value),
            currentValue = Number(target.dataset.currentvalue),
            price = Number(target.parentElement.nextElementSibling.querySelector("span").innerText);
            if (value > currentValue) {
                fullPrice.innerText = Number(fullPrice.innerText) + price * (value - currentValue);
            } else {
                fullPrice.innerText = Number(fullPrice.innerText) - price * (currentValue - value);
            }
            target.dataset.currentvalue = value;
        }
    }

    static submitOrder(target) {
        if (target.id == "submit-order") {
            const table = document.querySelector("#orders-table");
            data = []
            table.forEach(row => {
                data.push(
                    {
                        name: `${row.queryselector(".name").innerText}`,
                        quantity: `${row.queryselector(".quantity").innerText}`
                    }
                );
            });
            const xhr = new XMLHttpRequest();
            xhr.open(`${window.location.href}`, "POST", true);
            xhr.send(JSON.stringify(data));
        }
    }
}

document.querySelectorAll(".food-button").forEach(button => {
    button.addEventListener("click", e => {
        const name = e.target.parentElement.querySelector("h4").innerText,
        price = e.target.parentElement.querySelector("div span").innerText,
        food = new Food(name, price);
        UI.addFood(food, e.target);
    });
});

const table = document.querySelector("table");

table.addEventListener("click", e => {
    UI.removeFood(e.target);
});

table.addEventListener("change", e => {
    UI.updatePrice(e.target);
});

document.querySelector("#submit-order").addEventListener("click", e => {
    UI.submitOrder(e.target);
});