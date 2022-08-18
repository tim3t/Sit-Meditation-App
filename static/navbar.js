function navbarResponse() {
	let x = document.getElementById('topNav');
	if (x.className === 'topnav') {
		x.className += ' responsive';
	}
	else {
		x.className = 'topnav';
	}
}
