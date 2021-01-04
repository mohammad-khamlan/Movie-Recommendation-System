function getDiv(movies_ids) {
    clean();
    console.log(movies_ids);
    var div = document.getElementById('answer');
    var the_list = document.getElementById('list-movies');

    div.style.visibility = 'visible';

    var movie = document.createTextNode('rush hour');

    var result_movies = movies_ids;

    for (var i = 0; i < result_movies.length ; i++) {
        var node = document.createElement('li');
        node.style.color = 'black';
        node.style.marginBottom = '2rem';
        node.style.marginTop = '1rem';
        node.style.fontFamily = 'sans-serif';
        node.style.fontSize = '1.2rem';

        var movie = document.createTextNode(result_movies[i]);
        node.appendChild(movie);
        the_list.appendChild(node);
    }

}

function clean() {
    document.getElementById('userID').value = '';
    document.getElementById('answer').style.visibility = 'hidden';
    document.getElementById('list-movies').innerHTML = '';
}
