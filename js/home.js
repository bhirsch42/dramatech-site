window.onload = function() {

// * * * * * * * * * * *
// Homepage articles
// * * * * * * * * * * *

var duration = 500;
var oldLeft = 0
var articleOpen = false;
var oldScroll = 0

$( window ).resize(function() {
	var $articles = $('.article')
	if ($(window).width() < 400) {
		$articles.each(function() {
			$(this).css({
				'width': "100%",
				'height': "400px",
				"margin-left":"0px",
				"margin-right":"0px",
				"border-radius":"5px",
				"left": oldLeft,
				"scrollTop": "0"
			}, duration)
		})
	}
	else {
		$articles.each(function() {
			$(this).css({
				'width': "300px",
				'height': "400px",
				"margin":"20px",
				"border-radius":"5px",
				"left": oldLeft,
				"scrollTop": "0"
			}, duration)
		})
	}
})

$('a.expand-article').click(function() {
	if (articleOpen) {
		return
	}
	articleOpen = true;
	var id = this.id
	var $article = $('div.article#' + id)
	var $smallArticle = $article.find(".article-small")
	var $bigArticle = $article.find(".article-big")
	var thisTop = $article.offset().top - 20
	oldLeft = $article.offset().left - 20
	// hide all other articles
	// fix all articles absolutely
	var $articles = $('.article')
	var lefts = []
	var tops = []
	$articles.each(function(index) {
		lefts[index] = $(this).offset().left - 20
		tops[index] = $(this).offset().top - 20
	})
	$articles.each(function(index) {
		$(this).css({
			"position": "absolute",
			"left": lefts[index],
			"top": tops[index]
		})
	})
	$articles.each(function(index) {
		if (this.id != id) {
			$(this).fadeTo("fast", 0)
			$(this).css({
				"z-index":-1
			})
		}
	})

	// expand this article
	oldScroll = $(window).scrollTop()
	$('html, body').animate({
		scrollTop: $("#" + id).offset().top,
	}, duration, function() {
		// $('html, body').css({
		// 	"overflow": "hidden"
		// })
});
	// var totalHeight = $bigArticle.outerHeight(true)
	var curHeight = $article.height();
	$article.css('height', 'auto');
	var autoHeight = $article.height();
	if ($(window).height() > autoHeight) {
		autoHeight = $(window).height()
	}

	if ($(window).width() < 400) {
		$article.height(curHeight).animate({
			'width': "100%",
			'height': "100%",
			"border-radius":"0",
			// "left": "0",
			"margin-left": "0",
			"margin-right": "0",
			"z-index": 100
		}, duration, function() {
			$article.css({
				"overflow-y": "scroll"
			})
			$('html').css({
				// scrollTop: $("#" + id).offset().top,
				"overflow": "hidden"
			})
		})
	} else {
		$article.height(curHeight).animate({
			'width': "100%",
			'height': "100%",
			"border-radius":"0",
			"left": "0",
			"margin-left": "0",
			"margin-right": "0",
			"z-index": 100
		}, duration, function() {
			$article.css({
				"overflow-y": "scroll"
			})
			$('html').css({
				// scrollTop: $("#" + id).offset().top,
				"overflow": "hidden"
			})
		})
	}
	// layer the buttons properly

	$smallArticle.fadeTo("fast", 0, function(){
		$smallArticle.css({
			"position": "absolute"
		})
	})
	$bigArticle.fadeTo("slow", 1)
	$smallArticle.css({
		"z-index": 99
	})
	$bigArticle.css({
		"z-index": 100
	})
})

$('a.contract-article').click(function() {
	var id = this.id
	var $article = $('div.article#' + id)
	var $smallArticle = $article.find(".article-small")
	var $bigArticle = $article.find(".article-big")

	// contract this article
	$article.css({
		"overflow": "hidden"
	})
	$('html').css({
		"overflow-y": "scroll"
	})
	if ($(window).width() < 400) {
		$article.animate({
			// 'width': "300px",
			'height': "400px",
			// "margin":"20px",
			"border-radius":"5px",
			"left": oldLeft,
			"scrollTop": "0"
		}, duration)
	}
	else {
		$article.animate({
			'width': "300px",
			'height': "400px",
			"margin":"20px",
			"border-radius":"5px",
			"left": oldLeft,
			"scrollTop": "0"
		}, duration)
	}
	$smallArticle.fadeTo("slow", 1)
	$bigArticle.fadeTo("fast", 0)

	// show all other articles
	var $articles = $('.article')
	$articles.each(function(index) {
		if (id != this.id) {
			$(this).fadeTo("slow", 1)
		}
	})
	$('div.article').promise().done(function() {
		$articles.each(function(index) {
			$(this).css({
				"position": "initial",
				"z-index": "initial"
			})
		})
	})
	$smallArticle.css({
		"z-index": 100,
		"position": "relative"
	})
	$bigArticle.css({
		"z-index": 99
	})

	$('html, body').animate({
		scrollTop: oldScroll
	}, duration);

	articleOpen = false
})

}