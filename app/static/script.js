function searchMovie() {
    const movieName = document.getElementById("movieName").value;
    if (!movieName) {
        alert("Please enter a movie name!");
        return;
    }

    fetch(`/movie?name=${encodeURIComponent(movieName)}`)
        .then(response => {
            if (!response.ok) {
                throw new Error("Error fetching movie details");
            }
            return response.json();
        })
        .then(data => {
            const result = document.getElementById("result");
            if (data.error) {
                result.innerHTML = `<p class="error">Error: ${data.error}</p>`;
            } else {
                result.innerHTML = `
                    <div class="movie-details">
                        <img src="${data.poster}" alt="${data.title}" class="movie-poster">
                        <div class="movie-info">
                            <h2>${data.title}</h2>
                            <p><strong>Release Date:</strong> ${data.release_date}</p>
                            <p><strong>Overview:</strong> ${data.overview}</p>
                        </div>
                    </div>
                `;
            }
        })
        .catch(error => {
            console.error("Error fetching movie details:", error);
            const result = document.getElementById("result");
            result.innerHTML = `<p class="error">An error occurred while fetching movie details.</p>`;
        });
}
