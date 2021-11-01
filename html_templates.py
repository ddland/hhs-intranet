from string import Template #safe option 

template_card = Template("""
<a class="card" href="$url" target="_blank">
    <figure class="card__thumbnail">
        <img alt="$img" src="afbeeldingen/$img">
    </figure>
    <div class="text">$text</div>
</a>
"""
)

template_card_form = Template("""
<div class="card">
    <a href="$url" target="_blank">
    <figure class="card__thumbnail">
        <img alt="$img" src="afbeeldingen/$img">
    </figure>
    </a>
    <div class="formtext">$text</div> 
</div>
"""
)

template_footer = Template("""
</body>
</html>
"""
)

template_header = Template("""<!DOCTYPE html>
<html lang="nl">
<head>
<meta charset="utf-8">
<title> Intranet HHS ($user) </title>
<link rel="icon" 
      type="image/png" 
      href="favicon.ico">
<style>
.card-container {
    display: grid;
    padding: 1rem;
    grid-template-columns: repeat(12, 1fr);
    grid-template-rows: repeat($maxrows,1fr);
    grid-auto-flow: column;
    grid-gap: 1rem;
}

@media(max-width: 1333px) {
.card-container {
    grid-template-columns: repeat(8, 1fr);
    grid-template-rows: repeat($maxrows2,1fr);
    }
}

@media(max-width: 950px) {
.card-container {
    grid-template-columns: repeat(6, 1fr);
    grid-template-rows: repeat($maxrows4,1fr);
    }
}

@media(max-width: 555px) {
.card-container {
    grid-template-columns: repeat(2, 1fr);
    grid-template-rows: repeat($maxrows8,1fr);
    }
}

.card {
    display: grid;
}
.card .button {
    align-self: end;
}

html {
    font-size: 16px;
    font-family: 'Open Sans', 'Helvetica Neue', 'Arial', sans-serif;
}

body {
    background-color: #efefef;
}
* {
    box-sizing: border-box;
}
.card {
    box-shadow: 0px 1px 5px #555;
    background-color: white;
}

.text {
    display: block; 
    background-color: $backgroundcolor;
    padding: 0px 5px 0px 5px;
    min-width: 8em;
    word-wrap: break-word;
    color: white;
    width: 100%;
    text-decoration: none;
    text-align: center;
    transition: .3s ease-out;
}

form input {
    width: 100%;
    }

.formtext {
    display: block;
    background-color: $backgroundcolor;
    padding: 0px;
}

figure{
    width: 100%;
    padding: 0em;
    border: 0em;
    margin: 0em;
}

img {
    max-width: 100%;
    padding: 0em;
    border: 0em;
}


</style>
</head>
<body translate="no">
<div style="color:$backgroundcolor;text-align:center;" >Intranet links voor: $user</div>
<div class="card-container"> 
""")


