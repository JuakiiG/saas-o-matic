// SPEC-04, 2.9: the URLs the application calls live here, not spread over the code.
export const environment = {
  // Where `uv run uvicorn --factory app.main:create_app` listens by default.
  apiBaseUrl: 'http://127.0.0.1:8000',
};
