// document.addEventListener("DOMContentLoaded", function () {

//     const timers = document.querySelectorAll(".timer");

//     timers.forEach(function (timer) {

//         let workedSeconds = parseInt(timer.dataset.worked || "0");
//         let running = timer.dataset.running === "true";
//         let startedAt = timer.dataset.start;

//         if (!running || !startedAt) {
//             return;
//         }

//         const startTime = new Date(startedAt);

//         function updateTimer() {
//             const now = new Date();
//             const elapsed = Math.floor((now - startTime) / 1000);
//             const total = workedSeconds + elapsed;

//             const hours = Math.floor(total / 3600);
//             const minutes = Math.floor((total % 3600) / 60);
//             const seconds = total % 60;

//             timer.textContent =
//                 String(hours).padStart(2, "0") + ":" +
//                 String(minutes).padStart(2, "0") + ":" +
//                 String(seconds).padStart(2, "0");
//         }

//         updateTimer();
//         setInterval(updateTimer, 1000);
//     });

// });


//  new

document.addEventListener("DOMContentLoaded", () => {

    const timers = document.querySelectorAll(".timer");

    function formatTime(totalSeconds) {
        const hours = Math.floor(totalSeconds / 3600);
        const minutes = Math.floor((totalSeconds % 3600) / 60);
        const seconds = totalSeconds % 60;

        return (
            String(hours).padStart(2, "0") +
            ":" +
            String(minutes).padStart(2, "0") +
            ":" +
            String(seconds).padStart(2, "0")
        );
    }

    timers.forEach((timer) => {

        let workedSeconds = parseInt(
            timer.dataset.worked || "0",
            10
        );

        const isRunning =
            timer.dataset.running === "true";

        const startTimeString =
            timer.dataset.start;

        timer.textContent = formatTime(workedSeconds);

        if (!isRunning || !startTimeString) {
            return;
        }

        const startTime =
            new Date(startTimeString);

        function update() {

            const now = new Date();

            const elapsedSeconds = Math.floor(
                (now.getTime() - startTime.getTime()) / 1000
            );

            const totalSeconds =
                workedSeconds + elapsedSeconds;

            timer.textContent =
                formatTime(totalSeconds);
        }

        update();

        setInterval(update, 1000);

    });

});