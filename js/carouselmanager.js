window.onload = function() {

// * * * * * * * * * * * * * *
// slide preview updater
// * * * * * * * * * * * * * *
function urlExists(url, callback) {
	$.ajax({
		type: 'HEAD',
		async: false,
		url: url,
		success: function(){
			callback(true);
		},
		error: function() {
			callback(false);
		}
	});
}

$('input:text[name=image-url]').keyup(function() {
	var url = $(this).val()
	urlExists(url, function(exists){
		$image = $('img.template')
		if (exists) {
			$image.show()
			$image.attr('src', url)
		} else {
			$image.hide()
		}
	});
	console.log($('img.template'))
})

$('.create-new-slide[name=button-url]').keyup(function() {
	var url = $(this).val()
	$button = $('a.button-template')
	$button.attr('href', url)
	console.log('hi')
})

$('.create-new-slide').each(function() {
	$(this).keyup(function() {
		$('.template[name=' + $(this).attr('name') + ']').html($(this).val())
	})
})

$('.create-new-slide[name=button-text]').keyup(function() {
	content = $(this).val()
	if (content.length > 0) {
		$('.button-template').show()
	} else {
		$('.button-template').hide()
	}
})

$('.button-template').hide()
$('img.template').hide()

}