package main

const VIEW_TEMPLATE = `<head>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/github-markdown-css/3.0.1/github-markdown.css">
<style>
	.w800 {
		max-width: 60em;
		margin: 0 auto;
	}

	* {
		font-size: 1.1em;
	}
</style>
<title>%s</title>
</head>

<body class="markdown-body w800">
<a href="/">HOME</a>
<script>
    document.write('<a href="' + document.referrer + '">Go Back</a>');
</script>
<br>

<h1>%s</h1>
<div>%s</div>

</body>`

const DIR_CONTENTS_TEMPLATE = `<h2>Dirs</h2>
<ul>
%s
</ul>
<h2>Notes</h2>
<ul>
%s
</ul>
<footer>
<a href="/">HOME</a>
<script>
    document.write('<a href="' + document.referrer + '">Go Back</a>');
	</script>
</footer>
`
