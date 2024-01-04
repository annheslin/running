// call the functions 

document.addEventListener('DOMContentLoaded', function() {

	// on click update table to filter on just the selected borough
	 // Add an event listener to each borough button
    const buttons = document.querySelectorAll('button');
    buttons.forEach(button => {
        button.addEventListener('click', function () {
            const borough = this.textContent.trim(); // Get the borough text
            
            // Call a function to filter the table rows
            filterTableRows(borough);
        });
    });


});


// defined functions 
function filterTableRows(borough) {
    // Get all table rows
    const rows = document.querySelectorAll('tbody tr');

    // Iterate through each row and toggle visibility based on the selected borough
    rows.forEach(row => {
        const boroughColumn = row.querySelector('td:first-child').textContent.trim();

        // Toggle visibility based on whether the borough matches the selected borough
        row.style.display = (boroughColumn === borough) ? 'table-row' : 'none';
    });
}