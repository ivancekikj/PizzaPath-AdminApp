document.addEventListener("DOMContentLoaded", () => {
    const isWorkingDayCheckbox = document.querySelector("#id_is_working_day");
    const startTimeInput = document.querySelector("#id_start_time");
    const endTimeInput = document.querySelector("#id_end_time");

    function validate() {
        if (isWorkingDayCheckbox.checked) {
            startTimeInput.disabled = false;
            endTimeInput.disabled = false;
            startTimeInput.nextElementSibling.style.display = "inline-block";
            endTimeInput.nextElementSibling.style.display = "inline-block";
        } else {
            startTimeInput.value = "";
            endTimeInput.value = "";
            startTimeInput.disabled = true;
            endTimeInput.disabled = true;
            startTimeInput.nextElementSibling.style.display = "none";
            endTimeInput.nextElementSibling.style.display = "none";
        }
    }

    if (isWorkingDayCheckbox) {
        setTimeout(() => {
            validate();
            isWorkingDayCheckbox.addEventListener("change", validate);
        }, 50);
    }
});