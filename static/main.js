$(document).ready(function() {
    $('#upload-form').submit(function(e) {
        e.preventDefault();

        var formData = new FormData(this);
        var waitMessage = $('<p>').text('Please wait...');  // Create a wait message element

        var resultsContainer = $('#results-container');
        resultsContainer.empty();
        resultsContainer.append(waitMessage);  // Display the wait message

        $.ajax({
            type: 'POST',
            url: '/upload',
            data: formData,
            contentType: false,
            cache: false,
            processData: false,
            success: function(response) {
                showResults(response);
            },
            error: function() {
                alert('An error occurred while processing the file.');
                resultsContainer.empty();  // Clear the results container if there is an error
            },
            complete: function() {
                waitMessage.remove();  // Remove the wait message after the results are obtained
            }
        });
    });

    function showResults(results) {
        var resultsContainer = $('#results-container');
        resultsContainer.empty();
    
        if (results.words.length > 0) {
            var table = $('<table>');
            var thead = $('<thead>').append('<tr><th>Phrase</th><th>Similarity Score (%)</th><th>Search Results</th></tr>');
            var tbody = $('<tbody>');
    
            for (var i = 0; i < results.words.length; i++) {
                var phrase = results.words[i];
                var similarityScore = results.similarity_score.toFixed(2) + '%'; // Append '%' to the similarity score
                var searchResults = results.search_results;
    
                var tr = $('<tr>');
                var phraseTd = $('<td>').text(phrase);
                var scoreTd = $('<td>').text(similarityScore);
    
                var ul = $('<ul>');
    
                for (var j = 0; j < searchResults.length; j++) {
                    var url = searchResults[j];
                    var li = $('<li>').append($('<a>').attr('href', url).attr('target', '_blank').text(url));
                    ul.append(li);
                }
    
                var searchResultsTd = $('<td>').append(ul);
    
                tr.append(phraseTd, scoreTd, searchResultsTd);
                tbody.append(tr);
            }
    
            table.append(thead, tbody);
            resultsContainer.append(table);
        } else {
            resultsContainer.text('No results found.');
        }
    }
    
});
