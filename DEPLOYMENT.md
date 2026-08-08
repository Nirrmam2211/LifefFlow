# Railway Deployment Guide

This project is ready to deploy on Railway as a Python web service.

## What Railway uses

- `railway.toml` defines the production start command.
- `wsgi.py` gives Railway a clean WSGI entrypoint.
- `backend/app.py` listens on Railway's `PORT` and can read Railway MySQL variables directly.

## Deploy steps

1. Push this repository to GitHub.
2. In Railway, create a new project and deploy from the GitHub repo.
3. Add a Railway MySQL database service to the same project.
4. Link the app service to the database service, or set the database variables on the app service.
5. Import `database/schema.sql` into the Railway MySQL database before the first launch.
6. Make sure these variables are present on the app service:
   - `SECRET_KEY`
   - `JWT_SECRET_KEY`
   - `DB_HOST` or Railway's `MYSQLHOST`
   - `DB_USER` or Railway's `MYSQLUSER`
   - `DB_PASSWORD` or Railway's `MYSQLPASSWORD`
   - `DB_NAME` or Railway's `MYSQLDATABASE`
   - `DB_PORT` or Railway's `MYSQLPORT`
7. Deploy the service.
8. Open the generated Railway domain and sign in.

## Notes

- The app root redirects to `/login`, so Railway's health check is configured there.
- If you want to use Railway's database variables directly, no manual mapping is needed because the app now falls back to `MYSQL*` values automatically.
