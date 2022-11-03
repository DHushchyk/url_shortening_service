$(document).ready(function () {
	BindLinks();
});

let linkArray = [];
let $crf_token = $('[name="csrfmiddlewaretoken"]').attr('value');

function BindLinks() {
	$.ajax({
		method: "GET",
		url: "https://url-shortener-dh.herokuapp.com/api/links/",
		success: function (response) {
			linkArray = response
			buildTable(linkArray)
		}
	})
}

	function buildTable(data) {
		let table = document.getElementById("Table")

		for (let i = 0; i < data.length; i++) {
			let row = `<tr>
						<td>${data[i].id}</td>
						<td>${data[i].original_url}</td>
						<td>${data[i].short_url}</td>
						<td><a href="${data[i].redirect_link}">${data[i].redirect_link}</a></td>
				  </tr>`
			table.innerHTML += row
		}
	}


$('#btnSubmit').click(function () {
	let originalURL = $('#txtOriginalURL').val();
	$.ajax({
		method: "POST",
		dataType: "json",
		data: {
			"original_url": originalURL,
		},
		headers:{"X-CSRFToken": $crf_token},
		url: "https://url-shortener-dh.herokuapp.com/api/links/",
		success: function (result) {
			location.reload()
		},
		error: function (xhr) {
			let err_msg = ''
			for (let prop in xhr.responseJSON) {
				err_msg += prop + ': ' + xhr.responseJSON[prop] + '\n';
			}
			alert(err_msg);
		}
	});
});