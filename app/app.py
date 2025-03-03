from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

# Home route to render the HTML page
@app.route("/")
def home():
    return render_template("index.html")  # Ensure index.html is in the "templates" folder

# API route to fetch movie details
@app.route("/movie", methods=["GET"])
def get_movie():
    # Get the movie name from the query parameters
    movie_name = request.args.get("name")
    if not movie_name:
        return jsonify({"error": "Movie name is required"}), 400

    try:
        # TMDB API details
        api_key = "0d1c38a77122f7212cc19086b9fbbdfa"  # Replace with your API key
        tmdb_url = f"https://api.themoviedb.org/3/search/movie"
        params = {
            "api_key": api_key,
            "query": movie_name
        }

        # Make a GET request to the TMDB API
        response = requests.get(tmdb_url, params=params)
        response.raise_for_status()  # Raise exception for HTTP errors

        data = response.json()

        # Check if the results list is not empty
        if "results" in data and data["results"]:
            movie = data["results"][0]  # Get the first result
            # Build the response object with necessary details
            result = {
                "title": movie.get("title", "N/A"),
                "release_date": movie.get("release_date", "N/A"),
                "poster": f"https://image.tmdb.org/t/p/w500{movie['poster_path']}" if movie.get("poster_path") else None,
                "overview": movie.get("overview", "No overview available")
            }
            return jsonify(result)

        # If no results are found
        return jsonify({"error": "No movie found"}), 404

    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Error fetching data: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
