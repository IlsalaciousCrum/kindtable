$(document).ready(function() {
	'use strict';
	var timezone = (Intl.DateTimeFormat().resolvedOptions().timeZone);
	var form = document.forms['login-form'];
	form.elements['timezone'].value = timezone;
});