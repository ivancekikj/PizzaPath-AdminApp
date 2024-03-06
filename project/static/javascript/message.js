setTimeout(() => {
    const element = document.querySelector(".message"); 
    document.querySelector("#messages").removeChild(element);
}, 5000);