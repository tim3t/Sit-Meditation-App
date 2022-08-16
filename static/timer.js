// This code was modified from an original primer on Javascript timers found at https://contactmentor.com/build-30-minutes-countdown-timer-js-sound/

const countContainer = document.querySelectorAll('.count-digit');
const startAction = document.getElementById('start-timer');
const stopAction = document.getElementById('stop-timer');
const resetAction = document.getElementById('reset-timer');
const timerPicker = document.getElementById('timer_picker');
const form = document.getElementById('timer_form');

let countDownTime = 30 * 60;
let timerID;
let isStopped = true;
const timeoutAudio = document.getElementById('alarm_audio');

const findTimeString = () => {
	let minutes = String(Math.trunc(countDownTime / 60));
	let seconds = String(countDownTime % 60);
	if (minutes.length === 1) {
		minutes = '0' + minutes;
	}
	if (seconds.length === 1) {
		seconds = '0' + seconds;
	}
	return minutes + seconds;
};

const startTimer = () => {
	if (isStopped) {
		isStopped = false;
		timerID = setInterval(runCountDown, 1000);
	}
};

const stopTimer = () => {
	isStopped = true;
	if (timerID) {
		clearInterval(timerID);
	}
};

const resetTimer = () => {
	stopTimer();
	countDownTime = countDownTime;
	renderTime();
};

timeoutAudio.src = 'https://soundbible.com/grab.php?id=1531&type=mp3';
timeoutAudio.load();

startAction.onclick = startTimer;
resetAction.onclick = resetTimer;
stopAction.onclick = stopTimer;

const renderTime = () => {
	const time = findTimeString();
	countContainer.forEach((count, index) => {
		count.innerHTML = time.charAt(index);
	});
};

const runCountDown = () => {
	countDownTime -= 1;
	renderTime();

	if (countDownTime === 0) {
		stopTimer();
		// Play alarm on timeout
		timeoutAudio.play();
		countDownTime = defaultValue;
	}
};
