# YouTube Video Fetcher API
## Project Goal
The goal of this project is to create an API that fetches the latest YouTube videos for a given tag or search query, stores the relevant information in a database, and provides a paginated response sorted in reverse chronological order of their publishing date-time.

## API Endpoints
### Get All Videos:
URL: /videos/
Method: GET
Description: Returns all stored videos sorted by publishing datetime.

### Get Paginated Videos:
URL: /get-videos/
Method: GET
Description: Paginated response for stored videos, sorted by publishing datetime.

### Filter and Sort Videos:
URL: /filter-videos/
Method: GET
Description: Allows filtering and sorting of videos based on specified parameters. Supports query parameters:
field (default: published_at): Field to filter/sort on.
order (default: desc): Sorting order (asc for ascending, desc for descending).

### Delete All Videos:
URL: /delete-all-videos/
Method: DELETE
Description: Deletes all videos from the database.

## Project Setup
1. Ensure you have Docker and Docker Compose installed on your system.
2. Git clone repository using git clone https://github.com/adii21-Ux/Vidfetch
3. Create .env file in root directory of project and add api key
`YOUTUBE_DATA_API_KEYS = 'api-key1, api-key2, ...'`
4. Run docker using
`docker-compose up --build`
5. Access api at `http://0.0.0.0:8000/api/`
